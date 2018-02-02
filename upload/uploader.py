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

    _event_set = None

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



    def setup(self, filename):

        self._data_file = os.path.basename(filename)

        self._event_set = os.path.basename(filename).split('.')[0]

        configuration = swagger_client.Configuration()
        configuration.access_token = self._auth_token

        api_instance = swagger_client.EventSetApi(swagger_client.ApiClient(configuration))
        event_set_id = self._event_set # str | ID of eventSet to create

        try:
            # creates an eventSet
            api_response = api_instance.create_event_set(event_set_id)
        except ApiException as e:
            if e.status != 422: #Already exists
                print("Exception when calling EventSetApi->create_event_set: %s\n" % e)

    def load_data_file(self, data_def, filename):

        self.setup(filename)

        input_stream = open(filename)

        return self.load_data(data_def, input_stream, True, False)


    def parse_date(self, defn, data_value):

        accuracy = None
        data_value = data_value.split(' ')[0]
        if 'date_format' in defn:
            try:
                date_format = '%Y-%m-%d'
                date_format = defn['date_format']
                data_value = datetime.datetime(*(time.strptime(data_value, date_format))[:6]).date()
            except ValueError as dpe:
                try:
                    date_format = '%d/%m/%Y'
                    data_value = datetime.datetime(*(time.strptime(data_value, date_format))[:6]).date()
                except ValueError as dpe:
                    try:
                        date_format = '%d-%b-%Y'
                        data_value = datetime.datetime(*(time.strptime(data_value, date_format))[:6]).date()
                    except ValueError as dpe:
                        try:
                            date_format = '%d/%m/%y'
                            data_value = datetime.datetime(*(time.strptime(data_value, date_format))[:6]).date()
                        except ValueError as dpe:
                            date_format = '%Y'
                            data_value = datetime.datetime(*(time.strptime(data_value[:4], date_format))[:6]).date()
                            accuracy = 'year'
#          else:
            #To make sure that the default conversion works
  #              data.typed_data_value

        return data_value, accuracy

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
                    if data_value == '\\N':
                        continue
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
                            if not (data_value == '' or
                                    data_value == 'NULL' or
                                    data_value == '-' or
                                    data_value == 'None'):
                                try:
                                    data_value, values[name + '_accuracy'] = self.parse_date(defn, data_value)
                                except ValueError as dpe:
                                    print("Failed to parse date '{}'".format(data_value))
                                    continue
                            else:
                                #Skip this property
                                continue

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

                self.process_item(values)


    def process_item(self, values):

        if 'study_id' not in values:
            values['study_id'] = '0000-Unknown'

        location_name, location = self.process_location(values, '')
        proxy_location_name, proxy_location = self.process_location(values, 'proxy_')

        return self.process_sampling_event(values, location_name, location, proxy_location_name, proxy_location)

    def add_location_identifier(self, looked_up, study_id, partner_name):

        if not looked_up:
            return

        found = False
        if looked_up.identifiers and study_id:
            for ident in looked_up.identifiers:
#                print(ident)
#                print(study_id)
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
                new_ident = swagger_client.Identifier( identifier_type = 'partner_name', 
                                                      identifier_value = partner_name,
                                                      identifier_source = self._event_set, 
                                                      study_name = study_id)
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
                            message = message + '\t' + str(conflict_loc.latitude) + '\t' + str(conflict_loc.longitude)
                            message = message + "Probable conflict with {}".format(conflict_loc)
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

    def update_country(self, country, looked_up):

        ret = looked_up
        #print(country)
        #print(looked_up)
        if country:
            update_country = False
            if looked_up.country:
                if looked_up.country != country:
                    print("Country confict {} {}".format(country, looked_up))
                    raise Exception("Country confict {} {}".format(country, looked_up))
            else:
                looked_up.country = country
                update_country = True
            if update_country:
                configuration = swagger_client.Configuration()
                configuration.access_token = self._auth_token

                api_instance = swagger_client.LocationApi(swagger_client.ApiClient(configuration))
                updated = api_instance.update_location(looked_up.location_id, looked_up)
                ret = updated

        return ret

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
                swagger_client.Identifier('partner_name', partner_name, self._event_set, study_id)
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
            ret = self.update_country(country, looked_up)

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
                                print("Location name conflict\t{}\t{}\t{}\t{}\t{}\t{}".
                                      format(study_id,partner_name,named_loc,
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

        es_api_instance = swagger_client.EventSetApi(swagger_client.ApiClient(configuration))

        doc = None
        doc_accuracy = None
        study_id = None
        ret = None

        if 'doc' in values:
            if isinstance(values['doc'], datetime.date):
                doc = values['doc']
        else:
            if 'year' in values:
                if isinstance(values['year'], datetime.date):
                    doc = values['year']
                    values['doc_accuracy'] = 'year'

        if 'doc_accuracy' in values:
            doc_accuracy = values['doc_accuracy']
        if 'study_id' in values:
            study_id = values['study_id']

        lid = None
        plid = None

        if location:
            lid = location.location_id
        if proxy_location:
            plid = proxy_location.location_id

        samp = swagger_client.SamplingEvent(None, study_id = study_id, doc = doc, location_id =
                                     lid, proxy_location_id = plid, doc_accuracy = doc_accuracy)

        idents = []
        if 'sample_roma_id' in values:
            idents.append(swagger_client.Identifier ('roma_id', values['sample_roma_id'],
                                                     self._event_set))
        if 'sample_partner_id' in values and values['sample_partner_id']:
            idents.append(swagger_client.Identifier ('partner_id', values['sample_partner_id'],
                                                     self._event_set))
        if 'sample_oxford_id' in values and values['sample_oxford_id']:
            idents.append(swagger_client.Identifier ('oxford_id', values['sample_oxford_id'],
                                                     self._event_set))
        if 'sample_lims_id' in values and values['sample_lims_id']:
            idents.append(swagger_client.Identifier ('sanger_lims_id', values['sample_lims_id'],
                                                     self._event_set))
        if 'sample_alternate_oxford_id' in values and len(values['sample_alternate_oxford_id']) > 0:
            idents.append(swagger_client.Identifier ('alt_oxford_id',
                                                     values['sample_alternate_oxford_id'],
                                                     self._event_set))
        if 'sample_source_id' in values and values['sample_source_id'] and values['sample_source_type']:
            idents.append(swagger_client.Identifier (values['sample_source_type'],
                                                     values['sample_source_id'],
                                                     self._event_set))
        if 'sample_source_id1' in values and values['sample_source_id1'] and values['sample_source_type1']:
            idents.append(swagger_client.Identifier (values['sample_source_type1'],
                                                     values['sample_source_id1'],
                                                     self._event_set))
        if 'sample_source_id2' in values and values['sample_source_id2'] and values['sample_source_type2']:
            idents.append(swagger_client.Identifier (values['sample_source_type2'],
                                                     values['sample_source_id2'],
                                                     self._event_set))
        if 'species' in values and values['species'] and len(values['species']) > 0:
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
                        #print("Looking for {} {}".format(ident.identifier_type, ident.identifier_value))

                        found = api_instance.download_sampling_event_by_identifier(ident.identifier_type,
                                                               urllib.parse.quote_plus(ident.identifier_value))
                        if ident.identifier_type == 'partner_id':
                            if 'sample_lims_id' in values and values['sample_lims_id']:
                                #Partner id is not the only id
                                if len(idents) > 2:
                                    continue
                                #Probably still not safe even though at this point it's a unique partner_id
                                continue
                            else:
                                #Not safe as partner id's can be the same across studies
                                continue
                        existing_sample_id = found.sampling_event_id
                        #print ("found: {}".format(samp))
                    except ApiException as err:
                        #self._logger.debug("Error looking for {}".format(ident))
                        #print("Not found")
                        pass

        if 'sample_lims_id' in values and values['sample_lims_id']:
            if not existing_sample_id:
                print("Could not find not adding {}".format(values))
                return None

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
#                    print("Adding loc ident {} {}".format(location_name, existing.study_id))
                    self.add_location_identifier(location, existing.study_id, location_name)
                    self.add_location_identifier(proxy_location, existing.study_id, proxy_location_name)

            if doc:
                if existing.doc:
                    if doc != existing.doc:
                        if existing.doc_accuracy == 'year':
                            existing.doc = doc
                            existing.doc_accuracy = doc_accuracy
                            new_ident_value = True
                            print("Conflicting doc value updated {} {} {}".format(values, doc, existing.doc))
                        else:
                            print("Conflicting doc value not updated {} {} {}".format(values, doc, existing.doc))
                else:
                    existing.doc = doc
                    new_ident_value = True
            if location:
                if existing.location:
                    if location.location_id != existing.location_id:
                        print("Conflicting location value {}\t{}\t{}\t{}\t{}\t{}\t{}".format(values, 
                                                                           location.identifiers[0].identifier_value, location.latitude, location.longitude,
                                                                           existing.location.identifiers[0].identifier_value, existing.location.latitude, existing.location.longitude))
                        #existing.location_id = location.location_id
                        #new_ident_value = True
                else:
                    existing.location_id = location.location_id
                    new_ident_value = True
            if samp.partner_species:
                if existing.partner_species:
                    if existing.partner_species != samp.partner_species:
                        fuzzyMatch = False
                        if existing.partner_species == 'Plasmodium falciparum/vivax mixture':
                            if samp.partner_species == 'Plasmodium vivax':
                                fuzzyMatch = True
                            if samp.partner_species == 'Plasmodium falciparum':
                                fuzzyMatch = True

                        if not fuzzyMatch:
                            print("Conflicting partner_species value not updated record {}\t{}\t{}".format(values,
                                                                               samp.partner_species,
                                                                               existing.partner_species))

                else:
                    existing.partner_species = samp.partner_species
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

            ret = existing

            if new_ident_value:
                #print("Updating {} to {}".format(orig, existing))
                ret = api_instance.update_sampling_event(existing.sampling_event_id, existing)

            try:
                es_api_instance.create_event_set_item(self._event_set, existing.sampling_event_id)
            except ApiException as err:
                #Probably because it already exists
                self._logger.debug("Error adding sample {} to event set {} {}".format(existing.sampling_event_id, self._event_set, err))

        else:
            #print("Creating {}".format(samp))
            if len(idents) == 0:
                return None

            try:
                created = api_instance.create_sampling_event(samp)

                ret = created

                try:
                    es_api_instance.create_event_set_item(self._event_set, created.sampling_event_id)
                except ApiException as err:
                    #Probably because it already exists
                    self._logger.debug("Error adding sample {} to event set {} {}".format(created.sampling_event_id, self._event_set, err))

            except ApiException as err:
                print("Error adding sample {} {}".format(samp, err))
                self._logger.error("Error inserting {}".format(samp))
                sys.exit(1)

            if 'unique_id' in values:
                self._sample_cache[values['unique_id']] = created.sampling_event_id

        return ret

if __name__ == '__main__':
    sd = Uploader(sys.argv[3])
    with open(sys.argv[2]) as json_file:
        json_data = json.load(json_file)
        sd.load_data_file(json_data, sys.argv[1])

    #print(repr(sd.fetch_entity_by_source('test',1)))
