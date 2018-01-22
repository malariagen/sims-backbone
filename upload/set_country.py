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

import os
import requests

import upload_ssr

class SetCountry(upload_ssr.Upload_SSR):


    _country_cache = {}
    _country_location_cache = {}


    def load_location_cache(self):

        skip_header = True

        input_stream = open('country_locations.csv')

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
                    found = api_instance.download_sampling_event_by_identifier(id_type,
                                                               urllib.parse.quote_plus(id_value))
                except ApiException as e:
                    print("Exception when looking for event {} {} \n".format(id_column, e))
                    continue

                self.set_country(found, country_value)

    def set_country(self, found, country_value):

        configuration = swagger_client.Configuration()
        configuration.access_token = self._auth_token

        api_instance = swagger_client.SamplingEventApi(swagger_client.ApiClient(configuration))

        if country_value not in self._country_cache:
            try:
                metadata_api_instance = swagger_client.MetadataApi(swagger_client.ApiClient(configuration))
                metadata = metadata_api_instance.get_country_metadata(country_value)
                self._country_cache[country_value] = metadata
            except ApiException as e:
                print("Exception when looking up country {} {}".format(country_value, found))

        if found.location:
            try:
                found.location = self.update_country(self._country_cache[country_value].alpha3, found.location)
            except Exception:
                print("Country update failed for {}".format(found))
        else:
            if country_value in self._country_location_cache:
                cached_country = self._country_location_cache[country_value]
                location = None
                try:
                    if 'location' in cached_country:
                        location = cached_country['location']
                        found.location = self.update_country(self._country_cache[country_value].alpha3, location)
                    else:
                        location_api_instance = swagger_client.LocationApi(swagger_client.ApiClient(configuration))

                        location = None
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
                            location = location_api_instance.create_location(loc)
                        cached_country['location'] = location
                        self._country_location_cache[country_value]['location'] = location

                    found.location_id = location.location_id
                    found = api_instance.update_sampling_event(found.sampling_event_id, found)

                except Exception:
                    print("Country update failed for {}".format(found))
            else:
                print("Unknown country {}".format(country_value))

        return found


    def process_item(self, values):

        item = super().process_item(values)

        item = self.set_country(item, values['iso2'])

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

