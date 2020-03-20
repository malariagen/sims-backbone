from __future__ import print_function
import json
import csv
import re
import time
import datetime
import logging
import sys

import openapi_client
from openapi_client.rest import ApiException

from decimal import *

from copy import deepcopy

from pprint import pprint
from pprint import pformat

import os
import requests

from remote_backbone_dao import RemoteBackboneDAO
from local_backbone_dao import LocalBackboneDAO

from base_entity import BaseEntity
from sampling_event import SamplingEventProcessor
from original_sample import OriginalSampleProcessor
from derivative_sample import DerivativeSampleProcessor
from release import ReleaseProcessor
from assay_data import AssayDataProcessor
from individual import IndividualProcessor

class Uploader():

    _data_file = None

    _event_set = None

    _dao = None

    _config_file = None

    def __init__(self, config_file):
        self._logger = logging.getLogger(__name__)

        self._dao = RemoteBackboneDAO()

        if os.getenv('LOCAL_TEST'):
            self._dao = LocalBackboneDAO('upload_test',
                                         ['cn=editor,ou=sims,ou=projects,ou=groups,dc=malariagen,dc=net',
                                          'cn=all_studies,ou=sims,ou=projects,ou=groups,dc=malariagen,dc=net'])

        if config_file:
            self._config_file = config_file

            try:
                with open(config_file) as json_file:
                    args = json.load(json_file)
                    if 'debug' in args:
                        if args['debug']:
                            log_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
                            log_file = 'uploader_{}.log'.format(log_time)
                            print("Debugging to {}".format(log_file))
                            logging.basicConfig(level=logging.DEBUG, filename=log_file)
                    if 'dao_type' in args:
                        if args['dao_type'] == 'local':
                            if 'database' in args:
                                os.environ['POSTGRES_DB'] = args['database']
                            self._logger.debug('Using database {}'.format(os.getenv('POSTGRES_DB','backbone_service')))
                            self._dao = LocalBackboneDAO(args['username'], args['auths'])
            except FileNotFoundError as fnfe:
                print('No config file found: {}'.format(config_file))
                pass
        else:
            print('No config file specified')

        self._dao.setup(config_file)

    @property
    def message_buffer(self):
        return BaseEntity.message_buffer

    @property
    def use_message_buffer(self):
        return BaseEntity.use_message_buffer

    @use_message_buffer.setter
    def use_message_buffer(self, use_buffer):
        BaseEntity.set_use_message_buffer(use_buffer)

    def setup(self, filename):

        self._data_file = os.path.basename(filename)

        self._event_set = os.path.basename(filename).split('.')[0]

        event_set_id = self._event_set # str | ID of eventSet to create

        self.se_processor = SamplingEventProcessor(self._dao, self._event_set)
        self.os_processor = OriginalSampleProcessor(self._dao, self._event_set)
        self.os_processor.sampling_event_processor = self.se_processor
        self.ds_processor = DerivativeSampleProcessor(self._dao, self._event_set)
        self.ad_processor = AssayDataProcessor(self._dao, self._event_set)
        self.i_processor = IndividualProcessor(self._dao, self._event_set)
        self.r_processor = ReleaseProcessor(self._dao, self._event_set)

        api_response = self._dao.create_event_set(event_set_id)

    def load_data_file(self, data_def, filename, release=None):

        self.setup(filename)

        input_stream = open(filename)

        if self._logger.isEnabledFor(logging.DEBUG):
            import cProfile
            profile = cProfile.Profile()
            profile.enable()

        ret = self.load_data(data_def, input_stream, True, False, release)

        if self._logger.isEnabledFor(logging.DEBUG):
            profile.disable()
            #profile.print_stats()
            import io,pstats
            s = io.StringIO()
            sortby = 'cumulative'
            ps = pstats.Stats(profile, stream=s).sort_stats(sortby)
            ps.print_stats(.1)
            self._logger.debug(s.getvalue())
            profile.dump_stats('upload_source_stats.cprof')


        return ret


    def parse_date(self, defn, date_value):

        accuracy = None
        data_value = date_value.split(' ')[0]
        try:
            if 'date_format' in defn:
                date_format = defn['date_format']
            else:
                date_format = '%Y-%m-%d'
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
                        try:
                            date_format = '%d %b %Y'
                            data_value = datetime.datetime(*(time.strptime(date_value, date_format))[:6]).date()
                        except ValueError as dpe:
                            date_format = '%Y'
                            data_value = datetime.datetime(*(time.strptime(data_value[:4], date_format))[:6]).date()
                            accuracy = 'year'
#          else:
            #To make sure that the default conversion works
  #              data.typed_data_value

        return data_value, accuracy

    def load_data(self, data_def, input_stream, skip_header, update_only,
                  release=None):

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
                #Ensure columns are processed in order - see also doc_accuracy comment below
                #For more predictable behaviour
                for name, defn in sorted(data_def['values'].items(), key=lambda x: x[1]['column']):
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
                                # print("Groupdict:" + repr(re_match.groupdict()))
                                try:
                                    data_value = re_match.group(1)
                                except IndexError as iere:
                                        raise InvalidDataValueException("Failed to parse {} using {}"
                                                                        .format(data_value, defn['regex'])) from iere
                                # print("Transformed value is:" + data_value + " from " + row[defn['column']])
                                # print(repr(re_match.groupdict()))
                                # if row[defn['column']] != "" and data_value == "":
                                #     print("Empty match: {} {}".format(defn['regex'], row[defn['column']]))
                            else:
                                # print("No match: {} {}".format(defn, data_value))
                                data_value = None
                        if defn['type'] == 'datetime':
                            if not (data_value == '' or
                                    data_value == 'NULL' or
                                    data_value == '-' or
                                    data_value == 'None'):
                                try:
                                    data_value, values[name + '_accuracy'] = self.parse_date(defn, data_value)
                                except ValueError as dpe:
                                    self.se_processor.report("Failed to parse date '{}'".format(data_value),
                                                                                   values)
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
                        #Ignore empty values
                        #This can be important e.g. if date is parsed and set doc_accuracy to year
                        #and doc_accuracy accuracy defined column is empty
                        if data_value and data_value.strip():
                            values[name] = data_value.strip()
                        #else:
                        #    print('Ignoring {} {} {}'.format(name, data_value, values))
                    else:
                        values[name] = data_value

                if release:
                    values['release'] = release
                self.process_item(values)


    def process_item(self, values):

        #Reset connections for each item
        #Have had problems with pool.join blocking in ApiClient for
        #larger input files
        self._dao.setup(self._config_file)

        if 'study_id' not in values:
            values['study_id'] = '0000-Unknown'

        o_sample = self.os_processor.create_original_sample_from_values(values)

        o_existing = self.os_processor.lookup_original_sample(o_sample, values)

        if o_existing and values['study_id'][:4] == '0000':
            values['study_id'] = o_existing.study_name


        samp = self.se_processor.create_sampling_event_from_values(values)

        #print(values)
        #print(samp)

        proxy_location_name, proxy_location = self.se_processor.process_location(values, 'proxy_')
        location_name, location = self.se_processor.process_location(values,
                                                                     '',
                                                                     proxy_location)

        #print(location)
        existing = self.se_processor.lookup_sampling_event(o_existing, samp, location, proxy_location, values)

        if location:
            samp.location_id = location.location_id

        if proxy_location:
            if location:
                samp.proxy_location_id = location.proxy_location_id
            else:
                self.se_processor.report(f"Proxy location without location", values)

        #print('SAMP')
        #print(samp)

        indiv = self.i_processor.create_individual_from_values(values)
        existing_indiv = None
        if existing and existing.individual_id:
            existing_indiv = self._dao.download_individual(existing.individual_id)
        else:
            existing_indiv = self.i_processor.lookup_individual(indiv, values)

        individual = self.i_processor.process_individual(values, indiv,
                                                         existing_indiv)
        if individual:
            samp.individual_id = individual.individual_id
        sampling_event = self.se_processor.process_sampling_event(values, samp, existing)

        if sampling_event:
            o_sample.sampling_event_id = sampling_event.sampling_event_id

        original_sample = self.os_processor.process_original_sample(values, o_sample, o_existing)


        d_sample = self.ds_processor.create_derivative_sample_from_values(values,
                                                                          original_sample)

        dsamp = self.ds_processor.lookup_derivative_sample(d_sample, values)

        if not original_sample:
            if dsamp:
                # Might have the values to lookup the derivative sample but not
                # the original sample so handle that here
                print(f'Using derivative sample to find original sample {values}')
                original_sample = self.os_processor.process_original_sample(values, o_sample, dsamp.original_sample)
            else:
                # Because derivative samples must have an original sample
                d_sample = None

        derivative_sample = self.ds_processor.process_derivative_sample(d_sample, dsamp, original_sample, values)

        ad_sample = self.ad_processor.create_assay_datum_from_values(values,
                                                                     derivative_sample)

        adsamp = self.ad_processor.lookup_assay_datum(ad_sample, values)

        self.ad_processor.process_assay_datum(ad_sample, adsamp, derivative_sample, values)

        r_sample = self.ds_processor.create_derivative_sample_from_values(values,
                                                                          original_sample)

        rsamp = self.r_processor.lookup_release_item(r_sample, values)

        self.r_processor.process_release_item(r_sample, rsamp, original_sample, values)
        #print(existing)
        #print(sampling_event)
        #print(values)
        #print(sampling_event)
        #print(original_sample)
        #print(o_sample)
        #print(o_existing)
        return sampling_event


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file")
    parser.add_argument("data_config")
    parser.add_argument("config")
    parser.add_argument('--release')
    args = parser.parse_args()
    print(args)
    sd = Uploader(args.config)
    with open(args.data_config) as json_file:
        json_data = json.load(json_file)
        sd.load_data_file(json_data, args.data_file, args.release)

    #print(repr(sd.fetch_entity_by_source('test',1)))
