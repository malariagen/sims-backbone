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

class Uploader():

    _location_cache = {}

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
                            date_format = data.default_date_format
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

                    values[name] = data_value.strip()

                self.process_location(values)

    def process_location(self, values):
        api_instance = swagger_client.LocationApi()
        curated_name = None
        curation_method = None
        latitude = None
        longitude = None
        resolution = None
        try:
            latitude = float(Decimal(values['latitude']))
            longitude = float(Decimal(values['longitude']))
        except:
            pass

        if 'resolution' in values:
            resolution = values['resolution']

        loc = swagger_client.Location(None, values['name'], latitude,
                                      longitude,
                                      resolution, curated_name, curation_method,
                                      values['country'])

        if loc.to_str() in self._location_cache:
            return
        else:
            self._location_cache[loc.to_str()]=loc

        #print(repr(loc))
        try:
            looked_up = api_instance.download_partner_location(loc.partner_name)
            loc.location_id = looked_up.location_id
            looked_up = api_instance.download_location(loc.location_id)
            if not looked_up == loc:
                print("Duplicate non-matching partner_name\n{}\n{}".format(loc, looked_up))
        except:
            try:
                created = api_instance.create_location(loc)
            except ApiException as err:
                print("Error creating {} {}".format(loc, err))


if __name__ == '__main__':
    sd = Uploader()
    with open(sys.argv[2]) as json_file:
        json_data = json.load(json_file)
        sd.load_data_file(json_data, sys.argv[1])

    #print(repr(sd.fetch_entity_by_source('test',1)))
