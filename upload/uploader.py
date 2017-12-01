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

class Uploader():

    _location_cache = {}
    _sample_cache = {}

    _auth_token = None

    _data_file = None

    def __init__(self, config_file):
        super().__init__()
        self._logger = logging.getLogger(__name__)
        # Configure OAuth2 access token for authorization: OauthSecurity
        self._auth_token = self.get_access_token(config_file)

    def get_access_token(self, config_file):

        with open(config_file) as json_file:
            args = json.load(json_file)
            r = requests.get(os.getenv('TOKEN_URL'), args, headers = { 'service': 'http://localhost/full-map' })
            at = r.text.split('=')
            token = at[1].split('&')[0]
            return(token)

    def load_data_file(self, data_def, filename):

        self._data_file = filename
        input_stream = open(filename)

        return self.load_data(data_def, input_stream, True, False)

#https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html
    def load_data(self, data_def, input_stream, skip_header, update_only):

        processed = 0

        with input_stream as csvfile:
            data_reader = csv.reader(csvfile, delimiter='\t')

            if skip_header:
                next(data_reader)

            for row in data_reader:
                entity_id = None
                values = {}
                prop_by_column = {}
                processed = processed + 1
                for name, defn in data_def['values'].items():
                    identity = False
                    #print(repr(defn))
                    #print(repr(row))
                    data_value = row[defn['column']]
                    #Convert data value - make sure you set data_value
                    try:
                        if 'regex' in defn:
                            re_match = re.search(defn['regex'], data_value)
                            if re_match:
                                #print("Groupdict:" + repr(re_match.groupdict()))
                                try:
                                    data_value = re_match.group(1)
                                except IndexError as iere:
                                        raise InvalidDataValueException("Failed to parse {} using {}"
                                                                        .format(data_value, defn['regex'])) from iere
                                #print("Transformed value is:" + data_value + " from " + row[defn['column']])
                                #print(repr(re_match.groupdict()))
                                #if row[defn['column']] != "" and data_value == "":
                                #    print("Empty match: {} {}".format(defn['regex'], row[defn['column']]))
                            #else:
                            #    print("No match: {} {}".format(defn['regex'], data_value))
                        if defn['type'] == 'datetime':
                            try:
                                if not (data_value == '' or data_value == 'NULL' or data_value == '-'):
                                    if 'date_format' in defn:
                                        try:
                                            date_format = '%Y-%m-%d'
                                            date_format = defn['date_format']
                                            data_value = datetime.datetime(*(time.strptime(data_value, date_format))[:6]).date()
                                        except ValueError as dpe:
                                            try:
                                                date_format = '%Y'
                                                data_value = datetime.datetime(*(time.strptime(data_value, date_format))[:6]).date()
                                                values[name + '_accuracy'] = 'year'
                                            except ValueError as dpe:
                                                raise InvalidDateFormatException("Failed to parse date '{}' using {}".format(data_value, date_format)) from dpe
                          #          else:
                                        #To make sure that the default conversion works
                          #              data.typed_data_value
                                else:
                                    #Skip this property
                                    continue
                            except (InvalidDataValueException,InvalidDateFormatException) as idfe:

                                self._connection.rollback()

                                self._cursor.close()
                                self._connection.close()
                                raise
                        if 'replace' in defn:
                            for subs in defn['replace']:
                                data_value = re.sub("^" + subs[0] + "$", subs[1], data_value)
                                #print("Transformed value is:" + data_value + " from " + row[defn['column']])

                    except IndexError:
                        self._logger.critical(repr(defn))
                        self._logger.critical(repr(row))
                        raise

                    if defn['type'] == 'string':
                        values[name] = data_value.strip()
                    else:
                        values[name] = data_value

                if 'study_id' not in values:
                    values['study_id'] = '0000-Unknown'

                location_name, location = self.process_location(values, '')
                proxy_location_name, proxy_location = self.process_location(values, 'proxy_')

                self.process_sampling_event(values, location_name, location, proxy_location_name, proxy_location)

    def add_location_identifier(self, looked_up, study_id, partner_name):

        if not looked_up:
            return

        found = False
        if looked_up.identifiers and study_id:
            for ident in looked_up.identifiers:
                if ident.study_name[:4] == study_id[:4] and \
                    ident.identifier_value == partner_name:
                    found = True

        if not found:
            #print("adding identifier1 {}".format(looked_up))
            if not looked_up.identifiers:
                looked_up.identifiers = []
            #print("values: {} {}".format(study_id, partner_name))
            if study_id and partner_name:
                # Configure OAuth2 access token for authorization: OauthSecurity
                configuration = swagger_client.Configuration()
                configuration.access_token = self._auth_token

                api_instance = swagger_client.LocationApi(swagger_client.ApiClient(configuration))
#                print("adding identifier {}".format(looked_up.identifiers))
                new_ident = swagger_client.Identifier('partner_name', partner_name, study_id)
                #print("adding identifier2 {}".format(new_ident))
                looked_up.identifiers.append(new_ident)
                #print("adding identifier3 {}".format(looked_up))
                try:
                    updated = api_instance.update_location(looked_up.location_id, looked_up)
                except ApiException as err:
                    #print("Error adding location identifier {} {}".format(looked_up, err))
                    message = 'duplicate location\t' + study_id + '\t' + partner_name + '\t' + \
                                str(looked_up.latitude) + '\t' + str(looked_up.longitude)
                    try:
                        conflict = api_instance.download_partner_location(partner_name)
                        if conflict and conflict.locations:
                            conflict_loc = api_instance.download_location(conflict.locations[0].location_id)
                            conflict_loc = api_instance.download_gps_location(str(looked_up.latitude),
                                                                              str(looked_up.longitude))
                            print("Probable conflict with {}".format(conflict_loc))
                            message = message + '\t' + str(conflict_loc.latitude) + '\t' + str(conflict_loc.longitude)
                    except ApiException as err:
                        try:
                            conflict_loc = api_instance.download_gps_location(str(looked_up.latitude),
                                                                              str(looked_up.longitude))
                            for cname in conflict_loc.identifiers:
                                if cname.study_name[:4] == study_id[:4]:
                                    message = message + '\t' + cname.identifier_value
                        except ApiException as err:
                            print(err)
                    print(message)
        #else:
        #    print("identifier exists")

    def process_location(self, values, prefix):

        if prefix + 'location_name' not in values:
            #print("No {}location name: {}".format(prefix, values))
            return None, None

        if not values[prefix + 'location_name']:
            print("No location name: {}".format(values))
            return None, None

        if prefix + 'latitude' not in values:
            return None, None

        if not values[prefix + 'latitude']:
            return None, None

        # Configure OAuth2 access token for authorization: OauthSecurity
        configuration = swagger_client.Configuration()
        configuration.access_token = self._auth_token

        api_instance = swagger_client.LocationApi(swagger_client.ApiClient(configuration))
        curated_name = None
        curation_method = None
        latitude = None
        longitude = None
        resolution = None
        country = None
        study_id = None
        try:
            latitude = round(float(Decimal(values[prefix + 'latitude'])),7)
            longitude = round(float(Decimal(values[prefix + 'longitude'])),7)
        except:
            pass

        if prefix + 'resolution' in values:
            resolution = values[prefix + 'resolution']

        if prefix + 'country' in values:
            country = values[prefix + 'country']
        if 'study_id' in values:
            study_id = values['study_id'][:4]
        partner_name = values[prefix + 'location_name']
        loc = swagger_client.Location(None, latitude,
                                      longitude,
                                      resolution, curated_name, curation_method,
                                      country)
        if study_id and partner_name:
            loc.identifiers = [
                swagger_client.Identifier('partner_name', partner_name, study_id)
            ]


        if 'description' in values:
            loc.notes = self._data_file + ' ' + values['description']
        else:
            loc.notes = self._data_file

        ret = None
        try:
            looked_up = api_instance.download_gps_location(str(latitude), str(longitude))
            looked_up = api_instance.download_location(looked_up.location_id)
            #print("Found location {}".format(looked_up))
            loc.location_id = looked_up.location_id
            self.add_location_identifier(looked_up, study_id, partner_name)

            loc.location_id = None
            ret = looked_up
        except Exception as err:
            #print(repr(err))
            #print("Failed to find location {}".format(loc))
            try:
                created = api_instance.create_location(loc)
                ret = created
            #    print("Created location {}".format(created))
            except ApiException as err:
                if err.status == 422:
                    named_locations = api_instance.download_partner_location(partner_name)
                    for named_loc in named_locations.locations:
                        for ident in named_loc.identifiers:
                            if ident.study_name[:4] == study_id[:4]:
                                print("Location name conflict\t{}\t{}\t{}\t{}\t{}\t{}\t{}".
                                      format(study_id,partner_name,named_loc.latitude,named_loc.longitude,
                                            latitude, longitude, values))
                else:
                    print("Error creating location {} {}".format(loc, err))
                return None, None

        #print("Returing location {}".format(ret))
        return partner_name, ret

    def process_sampling_event(self, values, location_name, location, proxy_location_name, proxy_location):

        # Configure OAuth2 access token for authorization: OauthSecurity
        configuration = swagger_client.Configuration()
        configuration.access_token = self._auth_token

        # create an instance of the API class
        api_instance = swagger_client.SamplingEventApi(swagger_client.ApiClient(configuration))

        doc = None
        study_id = None
        if 'doc' in values:
            if isinstance(values['doc'], datetime.date):
                doc = values['doc']
        else:
            if 'year' in values:
                if isinstance(values['year'], datetime.date):
                    doc = values['year']

            if 'year_accuracy' in values:
                samp.doc_accuracy = values['year_accuracy']

        if 'study_id' in values:
            study_id = values['study_id']

        lid = None
        plid = None

        if location:
            lid = location.location_id
        if proxy_location:
            plid = proxy_location.location_id

        samp = swagger_client.SamplingEvent(None, study_id = study_id, doc = doc, location_id =
                                     lid, proxy_location_id = plid)

        idents = []
        if 'sample_roma_id' in values:
            idents.append(swagger_client.Identifier ('roma_id',
                                                     urllib.parse.quote(values['sample_roma_id'],
                                                                        safe='')))
        if 'sample_partner_id' in values:
            idents.append(swagger_client.Identifier ('partner_id',
                                                     urllib.parse.quote(values['sample_partner_id'],
                                                                       safe='')))
        if 'sample_oxford_id' in values:
            idents.append(swagger_client.Identifier ('oxford_id',
                                                     urllib.parse.quote(values['sample_oxford_id'],
                                                                       safe='')))
        if 'sample_alternate_oxford_id' in values and len(values['sample_alternate_oxford_id']) > 0:
            idents.append(swagger_client.Identifier ('alt_oxford_id',
                                                     urllib.parse.quote(values['sample_alternate_oxford_id'],
                                                                        safe='')))
        if 'species' in values and len(values['species']) > 0:
            samp.partner_species = values['species']

        existing_sample_id = None
        if 'unique_id' in values:
            if values['unique_id'] in self._sample_cache:
                existing_sample_id = self._sample_cache[values['unique_id']]

        if not existing_sample_id:
            #print ("not in cache: {}".format(samp))
            if len(idents) > 0:
                #print("Checking identifiers {}".format(idents))
                samp.identifiers = idents
                new_ident_value = False
                for ident in idents:
                    try:
                        if ident.identifier_type == 'partner_id':
                            #Not safe as partner id's can be the same across studies
                            continue
                        #print("Looking for {} {}".format(ident.identifier_type, ident.identifier_value))

                        found = api_instance.download_sampling_event_by_identifier(ident.identifier_type,
                                                               ident.identifier_value)
                        existing_sample_id = found.sampling_event_id
                        #print ("found: {}".format(samp))
                    except ApiException as err:
                        #self._logger.debug("Error looking for {}".format(ident))
                        #print("Not found")
                        pass

        #print("Existing {}".format(existing_sample_id))
        if existing_sample_id:
            existing = api_instance.download_sampling_event(existing_sample_id)
            orig = deepcopy(existing)
            for new_ident in idents:
                found = False
                for existing_ident in existing.identifiers:
                    if existing_ident == new_ident:
                        found = True
                if not found:
                    new_ident_value = True
                    #print("Adding {} to {}".format(new_ident, existing))
                    existing.identifiers.append(new_ident)

    #        print("existing {} {}".format(existing, study_id))
            if study_id:
                if existing.study_id:
                    if study_id != existing.study_id:
                        if study_id[:4] == existing.study_id[:4]:
                            #print("#Short and full study ids used {} {} {}".format(values, study_id, existing.study_id))
                            pass
                        else:
                            if not (existing.study_id[:4] == '0000' or study_id[:4] == '0000'):
                                print("Conflicting study_id value {} {} {}".format(values, study_id, existing.study_id))
                        if not study_id[:4] == '0000':
                            existing.study_id = study_id
                            new_ident_value = True
                else:
                    existing.study_id = study_id
                    new_ident_value = True
            else:
                if existing.study_id:
    #                print("Adding loc ident {} {}".format(location_name, existing.study_id))
                    self.add_location_identifier(location, existing.study_id, location_name)
                    self.add_location_identifier(proxy_location, existing.study_id, proxy_location_name)

            if doc:
                if existing.doc:
                    if doc != existing.doc:
                        print("Conflicting doc value {} {}\n{}".format(values, doc, existing.doc))
                        existing.doc = doc
                        new_ident_value = True
                else:
                    existing.doc = doc
                    new_ident_value = True
            if location:
                if existing.location:
                    if location.location_id != existing.location_id:
                        print("Conflicting location value {}\n{}\n{}".format(values, location, existing.location))
                        existing.location_id = location.location_id
                        new_ident_value = True
                else:
                    existing.location_id = location.location_id
                    new_ident_value = True
            if proxy_location:
                if existing.proxy_location:
                    if proxy_location.location_id != existing.proxy_location_id:
                        print("Conflicting proxy location value {}\n{}\n{}".format(values, proxy_location, existing.proxy_location))
                        existing.proxy_location_id = proxy_location.location_id
                        new_ident_value = True
                else:
                    existing.proxy_location_id = proxy_location.location_id
                    new_ident_value = True
            if new_ident_value:
                #print("Updating {} to {}".format(orig, existing))
                api_instance.update_sampling_event(existing.sampling_event_id, existing)
        else:
            #print("Creating {}".format(samp))
            if len(idents) == 0:
                return

            try:
                created = api_instance.create_sampling_event(samp)
            except ApiException as err:
                print("Error adding sample {} {}".format(samp, err))
                self._logger.error("Error inserting {}".format(samp))
                sys.exit(1)

            if 'unique_id' in values:
                self._sample_cache[values['unique_id']] = created.sampling_event_id

if __name__ == '__main__':
    sd = Uploader(sys.argv[3])
    with open(sys.argv[2]) as json_file:
        json_data = json.load(json_file)
        sd.load_data_file(json_data, sys.argv[1])

    #print(repr(sd.fetch_entity_by_source('test',1)))
