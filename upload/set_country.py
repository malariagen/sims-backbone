from __future__ import print_function
import json
import csv
import re
import time
import datetime
import logging
import sys
import swagger_client
from swagger_client.rest import ApiException

from decimal import *

import urllib.parse
from copy import deepcopy

from pprint import pprint
from pprint import pformat

import os
import requests

from original_sample import OriginalSampleProcessor
from sampling_event import SamplingEventProcessor

import upload_ssr

class SetCountry(upload_ssr.Upload_SSR):


    _country_cache = {}
    _country_location_cache = {}
    _country_study_location_cache = {}

    _countries_file = 'country_locations.csv'

    def load_location_cache(self):

        skip_header = True

        input_stream = open(self._countries_file)

        with input_stream as csvfile:
            data_reader = csv.reader(csvfile, delimiter='\t')

            if skip_header:
                next(data_reader)

            for row in data_reader:
                country = {
                    'iso2': row[0],
                    'latitude': row[1],
                    'longitude': row[2],
                    'name': row[3]
                }
                self._country_location_cache[country['iso2']] = country


    def set_countries(self, filename, id_type, id_column, country_column):

        skip_header = True

        input_stream = open(filename)

        with input_stream as csvfile:
            data_reader = csv.reader(csvfile, delimiter='\t')

            if skip_header:
                next(data_reader)

            for row in data_reader:

                id_value = row[id_column]
                country_value = row[country_column]

                values = {
                    'id_value': id_value
                }
                try:
                    found_events = self._dao.download_sampling_events_by_os_attr(id_type,
                                                               urllib.parse.quote_plus(id_value))
                    if found_events:
                        found = found_events.sampling_events[0]

                except AttributeError as e:
                    print(found_events)
                    print(e)
                    continue
                except ApiException as e:
                    print("Exception when looking for event {} {} {} {}\n".format(id_type,
                                                                                  id_value,
                                                                                  id_column, e))
                    continue

                self.set_country(found, country_value, filename, values)

    def find_country_for_study(self, country_value, study, country_ident):

        if study[:4] not in self._country_study_location_cache:
            self._country_study_location_cache[study[:4]] = {}
        elif country_value in self._country_study_location_cache[study[:4]]:
            return self._country_study_location_cache[study[:4]][country_value]

        try:
            named_locations = self._dao.download_partner_location(self._country_cache[country_value].english)

            #print('Locations for {}'.format(self._country_cache[country_value].english))
            #print(named_locations)

            for named_loc in named_locations.locations:
                for ident in named_loc.attrs:
                    if ident.study_name[:4] == study[:4]:
                        self._country_study_location_cache[study[:4]][country_value] = named_loc
                        #print('Found location')
                        return named_loc
        except ApiException as e:
            pass

        #print('location not found for study {}'.format(study))
        location = None

        if country_value in self._country_location_cache:
            cached_country = self._country_location_cache[country_value]

            if 'location' in cached_country:
                location = cached_country['location']
            else:
                try:
                    location = self._dao.download_gps_location(cached_country['latitude'],
                                                                           cached_country['longitude'])
                    location = location.locations[0]
                except ApiException as exp:
                    lat = round(float(Decimal(cached_country['latitude'])), 7)
                    lng = round(float(Decimal(cached_country['longitude'])), 7)
                    loc = swagger_client.Location(None, lat,
                                                  lng,
                                                  accuracy='country',
                                                  country=self._country_cache[country_value].alpha3)
                    loc.attrs = [
                        country_ident
                    ]
                    location = self._dao.create_location(loc)
                cached_country['location'] = location
                self._country_location_cache[country_value]['location'] = location

            if location:
                self._country_study_location_cache[study[:4]][country_value] = location

        else:
            self.os_processor.report("Unknown country {} in study {}".format(country_value, study), None)

        return location

    def set_country(self, found, country_value, filename, values):

        self.os_processor = OriginalSampleProcessor(self._dao, self._event_set)
        self.se_processor = SamplingEventProcessor(self._dao, self._event_set)
        orig = deepcopy(found)

        if country_value not in self._country_cache:
            try:
                metadata = self._dao.get_country_metadata(country_value)
                self._country_cache[country_value] = metadata
            except ApiException as e:
                if country_value != 'nan':
                    self.os_processor.report("Exception when looking up country {} {}".format(country_value,
                                                                                 found), None)
                return found

        ident = swagger_client.Attr('partner_name',
                                          attr_value=self._country_cache[country_value].english,
                                          attr_source='set_country {}'.format(filename),
                                          study_name=found.study_name)


        error = False
        if found.location:
            try:
                found.location = self.se_processor.update_country(self._country_cache[country_value].alpha3, found.location)
            except Exception as cue:
                self.os_processor.report_conflict(found, 'Country', found.location.country,
                                     country_value, 'not updated', values)
                error = True

        if found.proxy_location:
            try:
                found.proxy_location = self.se_processor.update_country(self._country_cache[country_value].alpha3, found.proxy_location)
            except Exception as cue:
                self.os_processor.report_conflict(found, 'Country', found.proxy_location.country,
                                     country_value, 'proxy not updated', values)
                error = True

        if error:
            return found

        if not found.location:

            location = self.find_country_for_study(country_value, found.study_name, ident)

            if location:
                try:

                    found.location_id = location.location_id
                    found.location = None
                    found = self._dao.update_sampling_event(found.sampling_event_id, found)

                except Exception as excp:
                    #print(str(excp), None)
                    self.os_processor.report(str(excp), None)
            else:
                self.os_processor.report("Unknown country {}".format(country_value), None)

        study_ident = False

        if found.location:
            if found.location.attrs:
                for attr in found.location.attrs:
                    if attr.study_name[:4] == found.study_name[:4]:
                        study_ident = True

        if not study_ident:
            if found.location:
                #print("adding study ident for {}".format(found))
                if not error:
                    found.location.attrs.append(ident)
                try:
                    self._dao.update_location(found.location_id, found.location)
                except Exception as excp:
                    #print(str(excp), None)
                    #The location is more specific than the country but does not have a name for
                    #that study - probably because it was unknown when added
                    self.os_processor.report('Unable to add country location attr name for study ',
                                {'attr_source': ident.attr_source,
                                 'identifer_value' : ident.attr_value,
                                 'attr_type': ident.attr_type,
                                 'study_id': found.study_name,
                                 'latitude': found.location.latitude,
                                 'longitude': found.location.longitude,
                                 'sampling_event_id': found.sampling_event_id
                                })

        if found.location and found.proxy_location:
            if found.location.country != found.proxy_location.country:
                self.os_processor.report_conflict(found, 'Country', found.location.country,
                                     found.proxy_location.country,
                                     'location and proxy location country mismatch',
                                     values)
        return found


    def process_item(self, values):

        o_sample = self.os_processor.create_original_sample_from_values(values)

        o_existing = self.os_processor.lookup_original_sample(o_sample, values)

        if o_existing and o_existing.sampling_event_id:
            item = self._dao.download_sampling_event(o_existing.sampling_event_id)
        else:
            self.os_processor.report("original sample not found - probably duplicate key", values)
            return None

        if item:
            item = self.set_country(item, values['iso2'], self._data_file, values)
        else:
            self.os_processor.report("sampling event not found - probably duplicate key", values)

        return item

if __name__ == '__main__':
    sd = SetCountry(sys.argv[1])
    id_type = sys.argv[2]
    input_file = sys.argv[3]
    id_column = int(sys.argv[4])
    country_column = int(sys.argv[5])
    ssr = sys.argv[6]
    sd.load_location_cache()

    sheets = None
    sd.load_data_file(ssr, sheets)

    sd.set_countries(input_file, id_type, id_column, country_column)
