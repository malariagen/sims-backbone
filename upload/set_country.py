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

import upload_ssr

class SetCountry(upload_ssr.Upload_SSR):


    _country_cache = {}
    _country_location_cache = {}
    _country_study_location_cache = {}

    _countries_file = 'country_locations.csv'

    def load_location_cache(self):

        skip_header = True

        input_stream = open(self._countries_file)

        configuration = swagger_client.Configuration()
        configuration.access_token = self._auth_token

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

        configuration = swagger_client.Configuration()
        configuration.access_token = self._auth_token

        api_instance = swagger_client.SamplingEventApi(swagger_client.ApiClient(configuration))

        with input_stream as csvfile:
            data_reader = csv.reader(csvfile, delimiter='\t')

            if skip_header:
                next(data_reader)

            for row in data_reader:

                id_value = row[id_column]
                country_value = row[country_column]

                try:
                    found_events = api_instance.download_sampling_event_by_identifier(id_type,
                                                               urllib.parse.quote_plus(id_value))
                    if found_events:
                        found = found_events.sampling_events[0]

                except ApiException as e:
                    print("Exception when looking for event {} {} \n".format(id_column, e))
                    continue

                self.set_country(found, country_value, filename, None)

    def find_country_for_study(self, country_value, study, country_ident):

        if study[:4] not in self._country_study_location_cache:
            self._country_study_location_cache[study[:4]] = {}
        elif country_value in self._country_study_location_cache[study[:4]]:
            return self._country_study_location_cache[study[:4]][country_value]

        configuration = swagger_client.Configuration()
        configuration.access_token = self._auth_token

        location_api_instance = swagger_client.LocationApi(swagger_client.ApiClient(configuration))

        try:
            named_locations = location_api_instance.download_partner_location(self._country_cache[country_value].english)

            #print('Locations for {}'.format(self._country_cache[country_value].english))
            #print(named_locations)

            for named_loc in named_locations.locations:
                for ident in named_loc.identifiers:
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
                    location = location_api_instance.download_gps_location(cached_country['latitude'],
                                                                           cached_country['longitude'])
                except ApiException as exp:
                    lat = round(float(Decimal(cached_country['latitude'])), 7)
                    lng = round(float(Decimal(cached_country['longitude'])), 7)
                    loc = swagger_client.Location(None, lat,
                                                  lng,
                                                  accuracy='country',
                                                  country=self._country_cache[country_value].alpha3)
                    loc.identifiers = [
                        country_ident
                    ]
                    location = location_api_instance.create_location(loc)
                cached_country['location'] = location
                self._country_location_cache[country_value]['location'] = location

            if location:
                self._country_study_location_cache[study[:4]][country_value] = location

        else:
            self._report("Unknown country {} in study {}".format(country_value, study), None)

        return location

    def set_country(self, found, country_value, filename, values):

        orig = deepcopy(found)

        configuration = swagger_client.Configuration()
        configuration.access_token = self._auth_token

        api_instance = swagger_client.SamplingEventApi(swagger_client.ApiClient(configuration))
        location_api_instance = swagger_client.LocationApi(swagger_client.ApiClient(configuration))

        if country_value not in self._country_cache:
            try:
                metadata_api_instance = swagger_client.MetadataApi(swagger_client.ApiClient(configuration))
                metadata = metadata_api_instance.get_country_metadata(country_value)
                self._country_cache[country_value] = metadata
            except ApiException as e:
                if country_value != 'nan':
                    self.report("Exception when looking up country {} {}".format(country_value,
                                                                                 found), None)
                return found

        ident = swagger_client.Identifier('partner_name',
                                          identifier_value=self._country_cache[country_value].english,
                                          identifier_source='set_country {}'.format(filename),
                                          study_name=found.study_id)

        idents = '\t'.join(pformat(x.to_dict(), width=1000, compact=True) for x in found.identifiers)

        if found.location:
            try:
                found.location = self.update_country(self._country_cache[country_value].alpha3, found.location)
            except Exception as cue:
                msg = "Country conflict not updated {} vs {} in {} for {}".format(country_value,
                                                                      found.location.country, idents,
                                                                      filename)
                #print(orig)
                #print(found)
                self.report(msg, values)

        if found.proxy_location:
            try:
                found.proxy_location = self.update_country(self._country_cache[country_value].alpha3, found.proxy_location)
            except Exception as cue:
                msg = "Country conflict not updated in proxy {} vs {} in {} for {}".format(country_value,
                                                                               found.proxy_location.country,
                                                                               idents,
                                                                               filename)
                self.report(msg, values)

        if not found.location:

            location = self.find_country_for_study(country_value, found.study_id, ident)

            if location:
                try:

                    found.location_id = location.location_id
                    found.location = location
                    found = api_instance.update_sampling_event(found.sampling_event_id, found)

                except Exception as excp:
                    #print(str(excp), None)
                    self.report(str(excp), None)
            else:
                self.report("Unknown country {}".format(country_value), None)

        study_ident = False

        if found.location:
            if found.location.identifiers:
                for identifier in found.location.identifiers:
                    if identifier.study_name[:4] == found.study_id[:4]:
                        study_ident = True

        if not study_ident:
            if found.location:
                #print("adding study ident for {}".format(found))
                found.location.identifiers.append(ident)
                try:
                    location_api_instance.update_location(found.location_id, found.location)
                except Exception as excp:
                    #print(str(excp), None)
                    #The location is more specific than the country but does not have a name for
                    #that study - probably because it was unknown when added
                    self.report('Unable to add country location identifier name for study ', { 'identifier_source': ident.identifier_source,
                                            'identifer_value' : ident.identifier_value,
                                            'identifier_type': ident.identifier_type,
                                            'study_id': found.study_id,
                                            'latitude': found.location.latitude,
                                            'longitude': found.location.longitude,
                                            'sampling_event_id': found.sampling_event_id
                                                                                      })

        if found.location and found.proxy_location:
            if found.location.country != found.proxy_location.country:
                self.report('Country {} != proxy country {} for {}'.format(found.location.country,
                                                                           found.proxy_location.country,
                                                                           idents), None)
        return found


    def process_item(self, values):

        # Configure OAuth2 access token for authorization: OauthSecurity
        configuration = swagger_client.Configuration()
        configuration.access_token = self._auth_token

        location_api_instance = swagger_client.LocationApi(swagger_client.ApiClient(configuration))

        # create an instance of the API class
        api_instance = swagger_client.SamplingEventApi(swagger_client.ApiClient(configuration))

        samp = self.create_sampling_event_from_values(values)

        item = self.lookup_sampling_event(api_instance, samp, values)

        if item:
            item = self.set_country(item, values['iso2'], self._data_file, values)
        else:
            self.report("sampling event not found - probably duplicate key", values)

        return item

if __name__ == '__main__':
    sd = SetCountry(sys.argv[1])
    id_type = sys.argv[2]
    input_file = sys.argv[3]
    id_column = int(sys.argv[4])
    country_column = int(sys.argv[5])
    ssr = sys.argv[6]
    sd.load_location_cache()
    sd.set_countries(input_file, id_type, id_column, country_column)

    sheets = None
    sd.load_data_file(ssr, sheets)

