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

from copy import deepcopy

from pprint import pprint
from pprint import pformat

import os
import requests

from remote_backbone_dao import RemoteBackboneDAO
from local_backbone_dao import LocalBackboneDAO

class Uploader():

    _location_cache = {}
    _sample_cache = {}

    _data_file = None

    _event_set = None

    _message_buffer = []

    _dao = None

    _config_file = None

    def __init__(self, config_file):
        self._logger = logging.getLogger(__name__)

        self._dao = RemoteBackboneDAO()

        self._config_file = config_file

        try:
            with open(config_file) as json_file:
                args = json.load(json_file)
                if 'dao_type' in args:
                    if args['dao_type'] == 'local':
                        if 'database' in args:
                            os.environ['DATABASE'] = args['database']
                        print('Using database {}'.format(os.getenv('DATABASE','backbone_service')))
                        self._dao = LocalBackboneDAO()
                if 'debug' in args:
                    if args['debug']:
                        log_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
                        log_file = 'uploader_{}.log'.format(log_time)
                        print("Debugging to {}".format(log_file))
                        logging.basicConfig(level=logging.DEBUG, filename=log_file)
        except FileNotFoundError as fnfe:
            print('No config file found: {}'.format(config_file))
            pass

        self._dao.setup(config_file)

        self._use_message_buffer = False

    @property
    def message_buffer(self):
        return self._message_buffer

    @property
    def use_message_buffer(self):
        return self._use_message_buffer

    @use_message_buffer.setter
    def use_message_buffer(self, use_buffer):
        self._use_message_buffer = use_buffer


    def setup(self, filename):

        self._data_file = os.path.basename(filename)

        self._event_set = os.path.basename(filename).split('.')[0]

        event_set_id = self._event_set # str | ID of eventSet to create

        api_response = self._dao.create_event_set(event_set_id)

    def report(self, message, values):

        if values:
            msg = "{}\t{}".format(message, sorted(values.items(), key=lambda x: x))
        else:
            msg = message

        if self.use_message_buffer:
            self._message_buffer.append(msg)
        else:
            print(msg)

    def report_conflict(self, sampling_event, report_type, old_val, new_val, message, values):

        old_value = old_val
        new_value = new_val

        if report_type == "Location":
            old_value = pformat(old_val.to_dict(), width=1000, compact=True)
            new_value = pformat(new_val.to_dict(), width=1000, compact=True)

        if report_type == "Location name":
            if old_val:
                old_value = pformat(old_val.to_dict(), width=1000, compact=True)
            if new_val:
                new_value = pformat(new_val.to_dict(), width=1000, compact=True)

        if report_type == "Country":
            loc = None
            if sampling_event:
                if 'proxy' in message:
                    loc = sampling_event.proxy_location
                else:
                    loc = sampling_event.location
            if loc:
                message = message + ' ' + pformat(loc.to_dict(), width=1000, compact=True)

        event_id = ''
        study_name = ''

        if sampling_event:
            event_id = sampling_event.sampling_event_id
            study_name = sampling_event.study_name

        msg = "Conflicting {} value\t{}\t{}\t{}\t{}\t{}".format(report_type, message,
                                                                event_id, study_name,
                                                                old_value, new_value)
        self.report(msg, values)


    def load_data_file(self, data_def, filename):

        self.setup(filename)

        input_stream = open(filename)

        if self._logger.isEnabledFor(logging.DEBUG):
            import cProfile
            profile = cProfile.Profile()
            profile.enable()

        ret = self.load_data(data_def, input_stream, True, False)

        if self._logger.isEnabledFor(logging.DEBUG):
            profile.disable()
            #profile.print_stats()
            import io,pstats
            s = io.StringIO()
            sortby = 'cumulative'
            ps = pstats.Stats(profile, stream=s).sort_stats(sortby)
            ps.print_stats(.1,'uploader')
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
                                    self.report("Failed to parse date '{}'".format(data_value),
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

                self.process_item(values)


    def add_locations_from_values(self, existing, sampling_event, values):

        if existing and values['study_id'][:4] == '0000':
            values['study_id'] = existing.study_name

        location_name, location = self.process_location(values, '', existing)
        proxy_location_name, proxy_location = self.process_location(values, 'proxy_', existing)

        if location:
            sampling_event.location_id = location.location_id
        if proxy_location:
            sampling_event.proxy_location_id = proxy_location.location_id

        sampling_event.location = location
        sampling_event.proxy_location = proxy_location


    def process_item(self, values):

        #Reset connections for each item
        #Have had problems with pool.join blocking in ApiClient for
        #larger input files
        self._dao.setup(self._config_file)

        if 'study_id' not in values:
            values['study_id'] = '0000-Unknown'


        samp = self.create_sampling_event_from_values(values)

        #print(samp)

        existing = self.lookup_sampling_event(samp, values)

        self.add_locations_from_values(existing, samp, values)

        return self.process_sampling_event(values, samp, existing)

    """
        returns true if the identifier is already in, or successfully added to, the location
    """
    def add_location_identifier(self, sampling_event, study_id, looked_up, ident_type, partner_name, values):

        if not looked_up:
            return False

        ret = False

        found = False
        if looked_up.identifiers and study_id:
            for ident in looked_up.identifiers:
#                print(ident)
#                print(study_id)
                if ident.study_name[:4] == study_id[:4] and \
                    ident.identifier_value == partner_name:
                    found = True

        if not found:
            existing_location = deepcopy(looked_up)
            #print("adding identifier1 {}".format(looked_up))
            if not looked_up.identifiers:
                looked_up.identifiers = []
            #print("values: {} {}".format(study_id, partner_name))
            if study_id and partner_name:
#                print("adding identifier {}".format(looked_up.identifiers))
                new_ident = swagger_client.Identifier( identifier_type = 'partner_name', 
                                                      identifier_value = partner_name,
                                                      identifier_source = self._event_set, 
                                                      study_name = study_id)
                #print("adding identifier2 {}".format(new_ident))
                looked_up.identifiers.append(new_ident)
                #print("adding identifier3 {}".format(looked_up))
                try:
                    updated = self._dao.update_location(looked_up.location_id, looked_up)
                    ret = True
                except ApiException as err:
                    #print("Error adding location identifier {} {}".format(looked_up, err))
                    message = 'duplicate location:{}:{}'.format(ident_type,partner_name)
                    try:
                        conflict = self._dao.download_partner_location(partner_name)
                        if conflict and conflict.locations:
                            conflict_loc = self._dao.download_location(conflict.locations[0].location_id)
                            conflict_loc = self._dao.download_gps_location(looked_up.latitude,
                                                                              looked_up.longitude)
                            self.report_conflict(sampling_event, "Location name", existing_location,
                                                 conflict_loc, message, values)
                        else:
                            self.report('No conflict on error: {}'.format(partner_name), values)
                    except ApiException as err:
                        try:
                            conflict_loc = self._dao.download_gps_location(looked_up.latitude,
                                                                              looked_up.longitude)
                            for cname in conflict_loc.identifiers:
                                if cname.study_name[:4] == study_id[:4]:
                                    message = message + ':' + cname.identifier_value
                            self.report_conflict(sampling_event, "Location name", looked_up,
                                                 conflict_loc, message, values)
                        except ApiException as err:
                            print(err)
        else:
            ret = True

        return ret

    def update_country(self, country, looked_up):

        ret = looked_up
        #print(country)
        #print(looked_up)
        if country:
            update_country = False
            if looked_up.country:
                if looked_up.country != country:
                    #print("Country confict {} {}".format(country, looked_up))
                    raise Exception("Country conflict not updating {} {}".format(country, looked_up))
            else:
                looked_up.country = country
                update_country = True
            if update_country:
                updated = self._dao.update_location(looked_up.location_id, looked_up)
                ret = updated

        return ret

    def create_location_from_values(self, values, prefix):

        if prefix + 'location_name' not in values:
            #print("No {}location name: {}".format(prefix, values))
            return None, None

        partner_name = values[prefix + 'location_name']

        if not partner_name:
            self.report("No location name: ",values)
            return None, None

        #Will have been set to 0000 if not present
        if 'study_id' in values:
            study_id = values['study_id'][:4]

        loc = swagger_client.Location(None)

        loc.identifiers = [
            swagger_client.Identifier(identifier_type='partner_name',
                                      identifier_value=partner_name,
                                      identifier_source=self._event_set, study_name=study_id)
        ]

        try:
            if prefix + 'latitude' in values and values[prefix + 'latitude']:
                loc.latitude = round(float(Decimal(values[prefix + 'latitude'])),7)
            if prefix + 'longitude' in values and values[prefix + 'longitude']:
                loc.longitude = round(float(Decimal(values[prefix + 'longitude'])),7)
        except Exception as excp:
            print(excp)
            pass

        if prefix + 'resolution' in values:
            loc.accuracy = values[prefix + 'resolution']

        if prefix + 'country' in values:
            loc.country = values[prefix + 'country']


        if 'description' in values:
            loc.notes = self._data_file + ' ' + values['description']
        else:
            loc.notes = self._data_file

        #print(values)
        #print(loc)

        return partner_name, loc

    def lookup_location(self, existing_event, study_id, loc, partner_name, values):

        looked_up = None
        conflict = False

        try:
            looked_up = self._dao.download_gps_location(str(loc.latitude), str(loc.longitude))
            looked_up = self._dao.download_location(looked_up.location_id)
        except Exception as err:
            #print(repr(err))
            #print("Failed to find location {}".format(loc))
            pass

        if not looked_up and not partner_name == "##Unknown":
            try:
                named_locations = self._dao.download_partner_location(partner_name)
                for named_loc in named_locations.locations:
                    for ident in named_loc.identifiers:
                        if ident.study_name[:4] == study_id[:4]:
                            if loc.latitude and loc.longitude:
                                self.report_conflict(existing_event, "Location name", loc,
                                                     named_loc, partner_name, values)
                                conflict = True
                            else:
                                looked_up = named_loc
            except ApiException as err:
                #Can't be found by name either
                pass

        return looked_up, conflict

    def process_location(self, values, prefix, existing_event):

        partner_name, loc = self.create_location_from_values(values, prefix)

        if loc is None:
            return None, None

        study_id = None

        if existing_event:
            study_id = existing_event.study_name
        else:
            if 'study_id' in values:
                study_id = values['study_id'][:4]

        existing_location = None
        if prefix == 'proxy_':
            if existing_event and existing_event.proxy_location:
                existing_location = deepcopy(existing_event.proxy_location)
        else:
            if existing_event and existing_event.location:
                existing_location = deepcopy(existing_event.location)

        if existing_location:
            orig = deepcopy(existing_location)
            orig.location_id = None
            if orig == loc:
                return partner_name, existing_location

        looked_up, conflict = self.lookup_location(existing_event, study_id, loc, partner_name, values)

        ret = None

        if looked_up is not None:
            try:
                #print("Found location {}".format(looked_up))
                loc.location_id = looked_up.location_id
                added_id = self.add_location_identifier(existing_event, study_id, looked_up, prefix, partner_name, values)

                if added_id:
                    try:

                        loc.location_id = None
                        try:
                            ret = self.update_country(loc.country, looked_up)
                        except Exception as err:
                            self.report_conflict(existing_event, 'Country', looked_up.country,
                                                     loc.country, 'not updated', values)
                    except Exception as err:
                        #Either a duplicate or country conflict
                        self.report(err, values)

            except Exception as err:
                print(repr(err))
                #print("Failed to find location {}".format(loc))
        elif not conflict:

            try:
                created = self._dao.create_location(loc)
                ret = created
            #    print("Created location {}".format(created))
            except ApiException as err:
                if err.status == 422:
                    self.report_conflict(existing_event, "Location name", None,
                                         loc, '', values)
                else:
                    self.report("Error creating location {} {}".format(loc, err), values)
                return None, None

        return partner_name, ret

    def create_sampling_event_from_values(self, values):

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

        samp = swagger_client.SamplingEvent(None, study_name = study_id, doc = doc)


        if 'species' in values and values['species'] and len(values['species']) > 0:
            samp.partner_species = values['species']

        if doc_accuracy:
            samp.doc_accuracy = doc_accuracy

        idents = []
        if 'sample_roma_id' in values:
            idents.append(swagger_client.Identifier ('roma_id', values['sample_roma_id'],
                                                     self._event_set))
        if 'sample_partner_id' in values and values['sample_partner_id']:
            idents.append(swagger_client.Identifier ('partner_id', values['sample_partner_id'],
                                                     self._event_set))
        if 'sample_partner_id_1' in values and values['sample_partner_id_1']:
            idents.append(swagger_client.Identifier ('partner_id', values['sample_partner_id_1'],
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

        samp.identifiers = idents

        #print(values)
        #print(samp)
        return samp

    def merge_events(self, existing, found, values):

        existing, changed = self.merge_sampling_event_objects(existing, found,
                                                              values)
        ret = existing

        if changed:

            for event_set in found.event_sets:
                self._dao.create_event_set_item(event_set, existing.sampling_event_id)

            self._dao.delete_sampling_event(found.sampling_event_id)

            #print("Updating {} to {}".format(orig, existing))
            existing = self._dao.update_sampling_event(existing.sampling_event_id, existing)
        else:
            self.report("Merge didn't change anything {} {}".format(existing, found), None)

        return existing

    def lookup_sampling_event(self, samp, values):

        existing = None

        if 'unique_id' in values:
            if values['unique_id'] in self._sample_cache:
                existing_sample_id = self._sample_cache[values['unique_id']]
                existing = self._dao.download_sampling_event(existing_sample_id)
                return existing

        #print ("not in cache: {}".format(samp))
        if len(samp.identifiers) > 0:
            #print("Checking identifiers {}".format(samp.identifiers))
            for ident in samp.identifiers:
                try:
                    #print("Looking for {} {}".format(ident.identifier_type, ident.identifier_value))

                    found_events = self._dao.download_sampling_events_by_identifier(ident.identifier_type,
                                                                                       ident.identifier_value)

                    for found in found_events.sampling_events:
                        if ident.identifier_type == 'partner_id':
                            #Partner ids within 1087 are not unique
                            if samp.study_name[:4] == '1087':
                                continue
                            if 'sample_lims_id' in values and values['sample_lims_id']:
                                #Partner id is not the only id
                                if len(samp.identifiers) > 2:
                                    continue
                                #Probably still not safe even though at this point it's a unique partner_id
                                continue
                            else:
                                #Not safe as partner id's can be the same across studies
                                #unless check study id as well
                                #print('Checking study ids {} {} {}'.format(samp.study_name,
                                #                                           found.study_name, ident))
                                if samp.study_name:
                                    if samp.study_name[:4] == '0000':
                                        continue
                                    if found.study_name[:4] != samp.study_name[:4]:
                                        continue
                                else:
                                    continue


                        #Only here if found - otherwise 404 exception
                        if existing and existing.sampling_event_id != found.sampling_event_id:
                            #self.report("Merging into {} using {}"
                            #                .format(existing.sampling_event_id,
                            #                                   ident.identifier_type), values)
                            found = self.merge_events(existing, found, values)
                        existing = found
                        if samp.study_name[:4] == '0000':
                            samp.study_name = existing.study_name
                        #print ("found: {} {}".format(samp, found))
                except ApiException as err:
                    #self._logger.debug("Error looking for {}".format(ident))
                    #print("Not found")
                        pass

        #if not existing:
        #    print('Not found {}'.format(samp))
        return existing

    def set_additional_event(self, sampling_event_id, study_id):

        if study_id[:4] == '0000' or study_id[:4] == '1089':
            return

        event_set_id = 'Additional events: {}'.format(study_id)

        api_response = self._dao.create_event_set(event_set_id)

        self._dao.create_event_set_item(event_set_id, sampling_event_id)


    def merge_sampling_event_objects(self, existing, samp, values):

        orig = deepcopy(existing)
        new_ident_value = False

        change_reasons = []

        for new_ident in samp.identifiers:
            found = False
            for existing_ident in existing.identifiers:
                #Depending on the DAO used the identifier can have a different type
                #so can't use ==
                if existing_ident.identifier_source == new_ident.identifier_source and \
                   existing_ident.identifier_type == new_ident.identifier_type and \
                   existing_ident.identifier_value == new_ident.identifier_value and \
                   existing_ident.study_name == new_ident.study_name:
                    found = True
            if not found:
                new_ident_value = True
                change_reasons.append("Adding ident {}".format(new_ident))
                existing.identifiers.append(new_ident)

#        print("existing {} {}".format(existing, study_id))
        if samp.study_name:
            if existing.study_name:
                if samp.study_name != existing.study_name:
                    if samp.study_name[:4] == existing.study_name[:4]:
                        #print("#Short and full study ids used {} {} {}".format(values, study_id, existing.study_name))
                        pass
                    else:
                        if not (existing.study_name[:4] == '0000' or samp.study_name[:4] == '0000'):
                            self.report_conflict(existing,"Study",
                                                 existing.study_name, samp.study_name,
                                                 "", values)

                        if not samp.study_name[:4] == '0000':
                            if ((int(samp.study_name[:4]) < int(existing.study_name[:4]) or
                                 existing.study_name[:4] == '0000') and
                                (samp.study_name[:4] != '1089')):
                                self.set_additional_event(existing.sampling_event_id,
                                                          existing.study_name)
                                existing.study_name = samp.study_name
                                new_ident_value = True
                                change_reasons.append('Updated study')
                            else:
                                if not (samp.study_name[:4] == '0000' or samp.study_name[:4] == '1089'):
                                    self.set_additional_event(existing.sampling_event_id,
                                                              samp.study_name)
            else:
                existing.study_name = samp.study_name
                new_ident_value = True
                change_reasons.append('Set study')
        else:
            if existing.study_name:
#                    print("Adding loc ident {} {}".format(location_name, existing.study_name))
                self.add_location_identifier(existing, existing.study_name, location, '', location_name,
                                             values)
                self.add_location_identifier(existing, existing.study_name, proxy_location, 'proxy_',
                                         proxy_location_name, values)

        if samp.doc:
            if existing.doc:
                if samp.doc != existing.doc:
                    update_doc = True
                    if samp.doc_accuracy and samp.doc_accuracy == 'year':
                        if not existing.doc_accuracy:
                            update_doc = False
                        if existing.doc_accuracy and existing.doc_accuracy != 'year':
                            update_doc = False

                    if update_doc:
                        msg = ""
                        if samp.doc_accuracy:
                            existing.doc_accuracy = samp.doc_accuracy
                            msg = "Accuracy updated"
                        else:
                            if existing.doc_accuracy:
                                existing._doc_accuracy = None
                                msg = "Accuracy cleared"

                        self.report_conflict(existing, "DOC",
                                             existing.doc, samp.doc,
                                             msg, values)
                        existing.doc = samp.doc

                        new_ident_value = True
                        change_reasons.append('Updated date')
                    else:
                        msg = "Not updated"
                        self.report_conflict(existing, "DOC",
                                             existing.doc, samp.doc,
                                             msg, values)
            else:
                existing.doc = samp.doc
                new_ident_value = True
                change_reasons.append('Set date')

        if samp.location:
            if existing.location:
                if samp.location.location_id != existing.location_id:
                    location = samp.location
                    msg = 'Location'
                    self.report_conflict(existing, "Location",
                                         existing.location, samp.location,
                                         msg, values)
                    existing.location_id = location.location_id
                    new_ident_value = True
                    change_reasons.append('Updated location')
            else:
                existing.location_id = samp.location.location_id
                new_ident_value = True
                change_reasons.append('Set location')

        if samp.proxy_location:
            if existing.proxy_location:
                if samp.proxy_location.location_id != existing.proxy_location_id:
                    proxy_location = samp.proxy_location
                    msg = 'Proxy Location'
                    self.report_conflict(existing, "Location",
                                         existing.proxy_location, samp.proxy_location,
                                         msg, values)
                    existing.proxy_location_id = proxy_location.location_id
                    new_ident_value = True
                    change_reasons.append('updated proxy location')
            else:
                existing.proxy_location_id = samp.proxy_location.location_id
                new_ident_value = True
                change_reasons.append('Set proxy location')

        if samp.partner_species:
            if existing.partner_species:
                if existing.partner_species != samp.partner_species:
                    fuzzyMatch = False
                    if existing.partner_species == 'Plasmodium falciparum/vivax mixture':
                        if samp.partner_species == 'Plasmodium vivax':
                            fuzzyMatch = True
                        if samp.partner_species == 'Plasmodium falciparum':
                            fuzzyMatch = True

                    if existing.partner_species == 'Plasmodium falciparum':
                        if samp.partner_species == 'P. falciparum':
                            fuzzyMatch = True

                    if not fuzzyMatch:
                        msg = "Not updated"
                        self.report_conflict(existing, "Species",
                                             existing.partner_species, samp.partner_species,
                                             msg, values)

            else:
                existing.partner_species = samp.partner_species
                new_ident_value = True
                change_reasons.append('Set species')

        #print('\n'.join(change_reasons))

        return existing, new_ident_value

    def process_sampling_event(self, values, samp, existing):

        #print('process_sampling event {} {} {} {} {}'.format(values, location_name, location, proxy_location_name, proxy_location))

        if 'sample_lims_id' in values and values['sample_lims_id']:
            if not existing:
                self.report("Could not find not adding ", values)
                return None

        if existing:

            #print("existing pre merge")
            #print(existing)
            existing, changed = self.merge_sampling_event_objects(existing, samp,
                                                                 values)
            #print("existing post merge")
            #print(existing)
            ret = existing

            if changed:
                #Make sure no implied edit - location should have been updated before here
                existing.location = None
                existing.proxy_location = None
                #print("Updating {} to {}".format(orig, existing))
                ret = self._dao.update_sampling_event(existing.sampling_event_id, existing)

            if not existing.event_sets or self._event_set not in existing.event_sets:
                self._dao.create_event_set_item(self._event_set, existing.sampling_event_id)

        else:
            #print("Creating {}".format(samp))
            if len(samp.identifiers) == 0:
                return None

            #Make sure no implied edit - location should have been updated before here
            samp.location = None
            samp.proxy_location = None

            try:
                created = self._dao.create_sampling_event(samp)

                ret = created

                self._dao.create_event_set_item(self._event_set, created.sampling_event_id)

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
