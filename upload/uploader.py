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

class Uploader():

    _location_cache = {}
    _sample_cache = {}

    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(__name__)

    def load_data_file(self, data_def, filename):

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
                            date_format = '%Y-%m-%d'
                            try:
                                if not (data_value == '' or data_value == 'NULL'):
                                    if 'date_format' in defn:
                                        try:
                                            date_format = defn['date_format']
                                            data_value = datetime.datetime(*(time.strptime(data_value, date_format))[:6])
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

                location_id = self.process_location(values, '')
                proxy_location_id = self.process_location(values, 'proxy_')

                self.process_sample(values, location_id, proxy_location_id)

    def process_location(self, values, prefix):

        if prefix + 'location_name' not in values:
            #print("No {}location name: {}".format(prefix, values))
            return None

        if not values[prefix + 'location_name']:
            print("No location name: {}".format(values))
            return None

        api_instance = swagger_client.LocationApi()
        curated_name = None
        curation_method = None
        latitude = None
        longitude = None
        resolution = None
        country = None
        try:
            latitude = round(float(Decimal(values[prefix + 'latitude'])),7)
            longitude = round(float(Decimal(values[prefix + 'longitude'])),7)
        except:
            pass

        if prefix + 'resolution' in values:
            resolution = values[prefix + 'resolution']

        if prefix + 'country' in values:
            country = values[prefix + 'country']

        loc = swagger_client.Location(None, values[prefix + 'location_name'], latitude,
                                      longitude,
                                      resolution, curated_name, curation_method,
                                      country)

        if loc.to_str() in self._location_cache:
            return self._location_cache[loc.to_str()]

        try:
            looked_up = api_instance.download_partner_location(loc.partner_name)
            looked_up = api_instance.download_location(looked_up.locations[0].location_id)
            loc.location_id = looked_up.location_id
            if not looked_up == loc:
                if looked_up.latitude == loc.latitude and looked_up.longitude == loc.longitude:
                    print("non-matching metadata \n{}\nparsed\n{}\nlooked_up\n{}".format(prefix, loc, looked_up))
                else:
                    #Assume if null then it's a look up key
                    if loc.latitude and loc.longitude:
                        print("Duplicate non-matching partner_name\n{}\n{}".format(loc, looked_up))
            #Location cache never has location id in key
            loc.location_id = None
            self._location_cache[loc.to_str()]=looked_up.location_id
        except:
            try:
                created = api_instance.create_location(loc)
                self._location_cache[loc.to_str()]=created.location_id
            except ApiException as err:
                print("Error creating location {} {}".format(loc, err))
                return None

        return self._location_cache[loc.to_str()]

    def process_sample(self, values, location_id, proxy_location_id):
        api_instance = swagger_client.SampleApi()

        doc = None
        study_id = None
        if 'doc' in values:
            if isinstance(values['doc'], datetime.datetime):
                doc = values['doc']
        if 'study_id' in values:
            study_id = values['study_id']

        samp = swagger_client.Sample(None, study_id = study_id, doc = doc, location_id =
                                     location_id, proxy_location_id = proxy_location_id)
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

        existing_sample_id = None
        if 'unique_id' in values:
            if values['unique_id'] in self._sample_cache:
                existing_sample_id = self._sample_cache[values['unique_id']]

        if not existing_sample_id:
            if len(idents) > 0:
                samp.identifiers = idents
                new_ident_value = False
                for ident in idents:
                    try:
                        if new_ident.identifier_type == 'partner_id':
                            #Not safe as partner id's can be the same across studies
                            continue
                        found = api_instance.download_sample_by_identifier(ident.identifier_type,
                                                               ident.identifier_value)
                        existing_sample_id = found.sample_id
#                        print ("found: {}".format(samp))
                    except:
    #                    print("Not found")
                        pass

        if existing_sample_id:
            existing = api_instance.download_sample(existing_sample_id)
            for new_ident in idents:
                found = False
                for existing_ident in existing.identifiers:
                    if existing_ident == new_ident:
                        found = True
                if not found:
                    new_ident_value = True
#                    print("Adding {} to {}".format(new_ident, existing))
                    existing.identifiers.append(new_ident)

            existing.study_id = study_id
            existing.doc = doc
            existing.location_id = location_id
            existing.proxy_location_id = proxy_location_id
            if new_ident_value:
                api_instance.update_sample(existing.sample_id, existing)
        else:
            if len(idents) == 0:
                return

            try:
                created = api_instance.create_sample(samp)
            except:
                self._logger.error("Error inserting {}".format(samp))
                sys.exit(1)

            if 'unique_id' in values:
                self._sample_cache[values['unique_id']] = created.sample_id

if __name__ == '__main__':
    sd = Uploader()
    with open(sys.argv[2]) as json_file:
        json_data = json.load(json_file)
        sd.load_data_file(json_data, sys.argv[1])

    #print(repr(sd.fetch_entity_by_source('test',1)))
