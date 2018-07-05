import sys
from copy import deepcopy

import logging

import swagger_client
from swagger_client.rest import ApiException

from base_entity import BaseEntity

class OriginalSampleProcessor(BaseEntity):

    _original_sample_cache = {}

    def __init__(self, dao, event_set):
        super().__init__(dao, event_set)
        self._logger = logging.getLogger(__name__)


    def create_original_sample_from_values(self, values):
        study_id = None
        if 'study_id' in values:
            study_id = values['study_id']

        o_sample = swagger_client.OriginalSample(None, study_name=study_id)

        idents = []
        if 'sample_roma_id' in values:
            idents.append(swagger_client.Attr ('roma_id', values['sample_roma_id'],
                                                     self._event_set))
        if 'sample_partner_id' in values and values['sample_partner_id']:
            idents.append(swagger_client.Attr ('partner_id', values['sample_partner_id'],
                                                     self._event_set))
        if 'sample_partner_id_1' in values and values['sample_partner_id_1']:
            idents.append(swagger_client.Attr ('partner_id', values['sample_partner_id_1'],
                                                     self._event_set))
        if 'sample_oxford_id' in values and values['sample_oxford_id']:
            idents.append(swagger_client.Attr ('oxford_id', values['sample_oxford_id'],
                                                     self._event_set))
        if 'sample_lims_id' in values and values['sample_lims_id']:
            idents.append(swagger_client.Attr ('sanger_lims_id', values['sample_lims_id'],
                                                     self._event_set))
        if 'sample_alternate_oxford_id' in values and len(values['sample_alternate_oxford_id']) > 0:
            idents.append(swagger_client.Attr ('alt_oxford_id',
                                                     values['sample_alternate_oxford_id'],
                                                     self._event_set))
        if 'sample_source_id' in values and values['sample_source_id'] and values['sample_source_type']:
            idents.append(swagger_client.Attr (values['sample_source_type'],
                                                     values['sample_source_id'],
                                                     self._event_set))
        if 'sample_source_id1' in values and values['sample_source_id1'] and values['sample_source_type1']:
            idents.append(swagger_client.Attr (values['sample_source_type1'],
                                                     values['sample_source_id1'],
                                                     self._event_set))
        if 'sample_source_id2' in values and values['sample_source_id2'] and values['sample_source_type2']:
            idents.append(swagger_client.Attr (values['sample_source_type2'],
                                                     values['sample_source_id2'],
                                                     self._event_set))

        if 'days_in_culture' in values:
            o_sample.days_in_culture = int(float(values['days_in_culture']))

        o_sample.attrs = idents

        return o_sample

    def lookup_original_sample(self, samp, values):

        existing = None

        if 'unique_os_id' in values:
            if values['unique_os_id'] in self._original_sample_cache:
                existing_sample_id = self._original_sample_cache[values['unique_os_id']]
                existing = self._dao.download_original_sample(existing_sample_id)
                return existing

        #print ("not in cache: {}".format(samp))
        if len(samp.attrs) > 0:
            #print("Checking attrs {}".format(samp.attrs))
            for ident in samp.attrs:
                try:
                    #print("Looking for {} {}".format(ident.attr_type, ident.attr_value))
                    if ident.attr_type == 'individual_id':
                        #individual_id is used for grouping
                        # and is not a unique ident
                        continue

                    found_events = self._dao.download_original_samples_by_attr(ident.attr_type,
                                                                                       ident.attr_value)

                    for found in found_events.original_samples:
                        if ident.attr_type == 'partner_id':
                            #Partner ids within 1087 are not unique
                            if samp.study_name[:4] == '1087':
                                continue
                            if 'sample_lims_id' in values and values['sample_lims_id']:
                                #Partner id is not the only id
                                if len(samp.attrs) > 2:
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
                        if existing and existing.original_sample_id != found.original_sample_id:
                            msg = ("Merging into {} using {}"
                                            .format(existing.sampling_event_id,
                                                               ident.attr_type), values)
                            #print(msg)
                            found = self.merge_original_samples(existing, found, values)
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

    def process_original_sample(self, values, samp, existing):

        ret = None

        #print('process_sampling event {} {} {} {} {}'.format(values, location_name, location, proxy_location_name, proxy_location))

        if 'sample_lims_id' in values and values['sample_lims_id']:
            if not existing:
                self.report("Could not find not adding ", values)
                return None

        if existing:

            ret = self.merge_original_samples(existing, samp, values)

        else:
            #print("Creating {}".format(samp))
            if len(samp.attrs) == 0:
                return None

            try:
                created = self._dao.create_original_sample(samp)

                ret = created

            except ApiException as err:
                print("Error adding sample {} {}".format(samp, err))
                self._logger.error("Error inserting {}".format(samp))
                sys.exit(1)

            if 'unique_os_id' in values:
                self._original_sample_cache[values['unique_os_id']] = created.original_sample_id

        return ret

    def merge_original_samples(self, existing, parsed, values):

        if not parsed:
            return existing

        if parsed.original_sample_id:
            #print('Merging via service {} {}'.format(existing, parsed))
            try:

                ret = self._dao.merge_original_samples(existing.original_sample_id,
                                                   parsed.original_sample_id)

            except ApiException as err:
                msg = "Error updating merged original sample {} {} {} {}".format(values, parsed, existing, err)
                print(msg)
                self._logger.error(msg)
                sys.exit(1)

            return ret

        existing, changed = self.merge_original_sample_objects(existing, parsed,
                                                              values)
        ret = existing

        if changed:

            #print("Updating {} to {}".format(parsed, existing))
            try:
                existing = self._dao.update_original_sample(existing.original_sample_id, existing)
            except ApiException as err:
                msg = "Error updating merged original sample {} {} {} {}".format(values, parsed, existing, err)
                print(msg)
                self._logger.error(msg)
                sys.exit(1)

        else:
            #self.report("Merge os didn't change anything {} {}".format(existing, parsed), None)
            pass

        return existing

    def merge_original_sample_objects(self, existing, samp, values):

        #print('Merging original samples {} {} {}'.format(existing, samp, values))
        orig = deepcopy(existing)
        new_ident_value = False

        change_reasons = []

        for new_ident in samp.attrs:
            found = False
            for existing_ident in existing.attrs:
                #Depending on the DAO used the attr can have a different type
                #so can't use ==
                if existing_ident.attr_source == new_ident.attr_source and \
                   existing_ident.attr_type == new_ident.attr_type and \
                   existing_ident.attr_value == new_ident.attr_value and \
                   existing_ident.study_name == new_ident.study_name:
                    found = True
            if not found:
                new_ident_value = True
                change_reasons.append("Adding ident {}".format(new_ident))
                existing.attrs.append(new_ident)

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

        if samp.sampling_event_id != existing.sampling_event_id:
            #print(existing)
            #print(samp)
            if existing.sampling_event_id:
                se_existing = self._dao.download_sampling_event(existing.sampling_event_id)
                if samp.sampling_event_id:
                    se_samp = self._dao.download_sampling_event(samp.sampling_event_id)
                    se = self.sampling_event_processor.merge_events(se_samp, se_existing, values)
                    #print(se)
            else:
                existing.sampling_event_id = samp.sampling_event_id
            new_ident_value = True
            change_reasons.append('Set SamplingEvent')

        #print('\n'.join(change_reasons))

        return existing, new_ident_value
