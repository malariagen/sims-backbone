import sys
from copy import deepcopy

import logging

import swagger_client
from swagger_client.rest import ApiException

from base_entity import BaseEntity

class DerivedSampleProcessor(BaseEntity):

    _derived_sample_cache = {}

    def __init__(self, dao, event_set):
        super().__init__(dao, event_set)
        self._logger = logging.getLogger(__name__)
        self._dao = dao
        self._event_set = event_set

    def create_derived_sample_from_values(self, values):

        d_sample = swagger_client.DerivedSample(None)

        idents = []
        if 'derived_sample_id' in values:
            idents.append(swagger_client.Attr('derived_sample_id', values['derived_sample_id'],
                                              self._event_set))

        if 'derived_sample_source' in values:
            idents.append(swagger_client.Attr('derived_sample_source',
                                              values['derived_sample_source'],
                                              self._event_set))

        if 'sanger_sample_id' in values:
            idents.append(swagger_client.Attr('sanger_sample_id',
                                              values['sanger_sample_id'],
                                              self._event_set))

        if 'dna_prep' in values:
            d_sample.dna_prep = values['dna_prep']

        d_sample.attrs = idents

        return d_sample

    def lookup_derived_sample(self, samp, values):

        existing = None

        if 'unique_ds_id' in values:
            if values['unique_ds_id'] in self._derived_sample_cache:
                existing_sample_id = self._derived_sample_cache[values['unique_ds_id']]
                existing = self._dao.download_derived_sample(existing_sample_id)
                return existing

        #print ("not in cache: {}".format(samp))
        if len(samp.attrs) > 0:
            #print("Checking attrs {}".format(samp.attrs))
            for ident in samp.attrs:
                try:
                    #print("Looking for {} {}".format(ident.attr_type, ident.attr_value))

                    found_events = self._dao.download_derived_samples_by_attr(ident.attr_type,
                                                                              ident.attr_value)

                    for found in found_events.derived_samples:
                        #Only here if found - otherwise 404 exception
                        if existing and existing.derived_sample_id != found.derived_sample_id:
                            msg = ("Merging into {} using {}"
                                   .format(existing.sampling_event_id,
                                           ident.attr_type), values)
                            print(msg)
                            found = self.merge_derived_samples(existing, found, values)
                        existing = found
                        #print ("found: {} {}".format(samp, found))
                except ApiException as err:
                    #self._logger.debug("Error looking for {}".format(ident))
                    #print("Not found")
                        pass

        #if not existing:
        #    print('Not found {}'.format(samp))
        return existing

    def process_derived_sample(self, samp, existing, original_sample, values):

        #print('process_sampling event {} {} {} {} {}'.format(values, location_name, location, proxy_location_name, proxy_location))

        if existing:
            ret = self.merge_derived_samples(existing, samp, values)
        else:
            #print("Creating {}".format(samp))
            if len(samp.attrs) == 0:
                return None

            try:
                samp.original_sample_id = original_sample.original_sample_id
                created = self._dao.create_derived_sample(samp)

                ret = created

            except ApiException as err:
                print("Error adding sample {} {}".format(samp, err))
                self._logger.error("Error inserting {}".format(samp))
                sys.exit(1)

            if 'unique_ds_id' in values:
                self._derived_sample_cache[values['unique_ds_id']] = created.derived_sample_id

        return ret

    def merge_derived_samples(self, existing, parsed, values):

        if not parsed:
            return existing

        if parsed.derived_sample_id:
            #print('Merging via service {} {}'.format(existing, parsed))
            try:

                ret = self._dao.merge_derived_samples(existing.derived_sample_id,
                                                      parsed.derived_sample_id)

            except ApiException as err:
                msg = "Error updating merged derived sample {} {} {} {}".format(values, parsed, existing, err)
                print(msg)
                self._logger.error(msg)
                sys.exit(1)

            return ret

        existing, changed = self.merge_derived_sample_objects(existing, parsed,
                                                              values)
        ret = existing

        if changed:

            #print("Updating {} to {}".format(parsed, existing))
            try:
                existing = self._dao.update_derived_sample(existing.derived_sample_id, existing)
            except ApiException as err:
                msg = "Error updating merged derived sample {} {} {} {}".format(values, parsed, existing, err)
                print(msg)
                self._logger.error(msg)
                sys.exit(1)

        else:
            #self.report("Merge os didn't change anything {} {}".format(existing, parsed), None)
            pass

        return existing

    def merge_derived_sample_objects(self, existing, samp, values):

        orig = deepcopy(existing)
        changed = False

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
                changed = True
                change_reasons.append("Adding ident {}".format(new_ident))
                existing.attrs.append(new_ident)

        if samp.original_sample_id != existing.original_sample_id:
            #print(existing)
            #print(samp)
            if existing.original_sample_id:
                se_existing = self._dao.download_original_sample(existing.original_sample_id)
                if samp.original_sample_id:
                    se_samp = self._dao.download_original_sample(samp.original_sample_id)
                    #se = self.merge_original_samples(se_samp, se_existing, values)
                    print('Need to merge original samples? {} {} {}'.format(se_samp, se_existing,
                                                                         values))
                    #print(se)
            else:
                existing.original_sample_id = samp.original_sample_id
            changed = True
            change_reasons.append('Set SamplingEvent')

        #print('\n'.join(change_reasons))

        return existing, changed

