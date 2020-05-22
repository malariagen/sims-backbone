import sys

import logging

import openapi_client
from openapi_client.rest import ApiException

from base_entity import BaseEntity

class OriginalSampleProcessor(BaseEntity):


    def __init__(self, dao, event_set):
        super().__init__(dao, event_set)
        self._logger = logging.getLogger(__name__)
        self._original_sample_cache = {}
        self._studies_cache = {}
        self._lookup_attrs = ['roma_id', 'oxford_id', 'partner_id']
        self.attrs = [
            {
                'from': 'sample_roma_id',
                'to': 'roma_id'
            },
            {
                'from': 'sample_partner_id',
                'to': 'partner_id'
            },
            {
                'from': 'sample_partner_id_1',
                'to': 'partner_id'
            },
            {
                'from': 'sample_oxford_id',
                'to': 'oxford_id'
            },
            {
                'from': 'sample_alternate_oxford_id',
                'to': 'alt_oxford_id'
            }
        ]


    def create_original_sample_from_values(self, values):
        study_id = None
        if 'study_id' in values:
            study_id = values['study_id']

        o_sample = openapi_client.OriginalSample(None, study_name=study_id)

        idents = self.attrs_from_values(values)
        if 'sample_source_id' in values and values['sample_source_id'] and values['sample_source_type']:
            idents.append(openapi_client.Attr(values['sample_source_type'],
                                              values['sample_source_id'],
                                              self._event_set))
        if 'sample_source_id1' in values and values['sample_source_id1'] and values['sample_source_type1']:
            idents.append(openapi_client.Attr(values['sample_source_type1'],
                                              values['sample_source_id1'],
                                              self._event_set))
        if 'sample_source_id2' in values and values['sample_source_id2'] and values['sample_source_type2']:
            idents.append(openapi_client.Attr(values['sample_source_type2'],
                                              values['sample_source_id2'],
                                              self._event_set))

        if 'days_in_culture' in values:
            o_sample.days_in_culture = int(float(values['days_in_culture']))

        if 'species' in values and values['species']:
            o_sample.partner_species = values['species']

        if 'os_acc_date' in values:
            o_sample.acc_date = values['os_acc_date']

        o_sample.attrs = idents

        return o_sample

    def update_attr_cache(self, cache, found):

        for attr in found.attrs:
            if attr.attr_type in cache:
                cache[attr.attr_type][attr.attr_value] = found

    def load_attr_cache(self, study_id, values):

        if study_id and study_id[:4] not in self._studies_cache:
            cache = {
                'roma_id': {},
                'oxford_id': {},
                'unique_os_id': {}
            }
            try:
                # print(f'Downloading os for study {study_id} {self._studies_cache.keys()}')
                found_events = self._dao.download_original_samples_by_study(study_id)
                for found in found_events.original_samples:
                    if found.sampling_event_id:
                        found_sampling_event = found_events.sampling_events[found.sampling_event_id]
                        found.sampling_event = found_sampling_event
                    self.update_attr_cache(cache, found)

                self._studies_cache[study_id[:4]] = cache
            except ApiException as err:
                #self._logger.debug("Error looking for {}".format(ident))
                #print("Not found")
                    pass

    def attr_cache_lookup(self, study_id, existing, values, ident):

        cache = None

        if study_id and study_id[:4] in self._studies_cache:
            cache = self._studies_cache[study_id[:4]]
        if cache and ident.attr_type in cache:
            if ident.attr_value in cache[ident.attr_type]:
                found = cache[ident.attr_type][ident.attr_value]
                if existing and existing.original_sample_id != found.original_sample_id:
                    msg = ("Merging into {} using {}".format(existing.original_sample_id, ident.attr_type), values)
                    #print(msg)
                    found = self.merge_original_samples(existing, found, values)
                existing = found
                        #print ("found: {} {}".format(samp, found))
        return existing

    def lookup_original_sample(self, samp, values):

        existing = None

        if 'unique_os_id' in values:
            if values['unique_os_id'] in self._original_sample_cache:
                existing_sample_id = self._original_sample_cache[values['unique_os_id']]
                existing = self._dao.download_original_sample(existing_sample_id)
                return existing

        study_id = None
        if 'study_id' in values:
            study_id = values['study_id']
            if study_id[:4] == '0000':
                study_id = None

        self.load_attr_cache(study_id, values)

        individual_lookup = False

        #print ("not in cache: {}".format(samp))
        if len(samp.attrs) > 0:
            # print("Checking attrs {}".format(samp.attrs))
            cache = None
            for ident in samp.attrs:

                existing = self.attr_cache_lookup(study_id, existing, values, ident)

                cache_existing = existing
                # print(f'Existing {existing} from cache')
                if not existing:
                    individual_lookup = True

                if individual_lookup or not study_id:
                    try:
                        # print("Looking for {} {}".format(ident.attr_type, ident.attr_value))
                        if ident.attr_type == 'individual_id':
                            #individual_id is used for grouping
                            # and is not a unique ident
                            continue

                        if ident.attr_type not in self._lookup_attrs:
                            continue
                        found_events = self._dao.download_original_samples_by_attr(ident.attr_type,
                                                                                   ident.attr_value)

                        for found in found_events.original_samples:
                            if ident.attr_type == 'partner_id':
                                #Partner ids within 1087 are not unique
                                if samp.study_name[:4] == '1087':
                                    continue
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

                            if existing and existing.original_sample_id != found.original_sample_id:
                                msg = ("Merging into {} using {}"
                                       .format(existing.sampling_event_id,
                                               ident.attr_type), values)
                                # print(msg)
                                found = self.merge_original_samples(existing, found, values)
                            existing = found
                            if samp.study_name[:4] == '0000':
                                samp.study_name = existing.study_name
                            # print ("found: {} {}".format(samp, found))
                    except ApiException as err:
                        #self._logger.debug("Error looking for {}".format(ident))
                        #print("Not found")
                            pass
                # if existing and not cache_existing:
                #     print(f'{values}')
                #     print(cache)
                #     print(self._studies_cache)
                # print(f'Existing {existing} from individual_lookup')

        # if not existing:
        #     print(f'Not found {samp} {values}')
        return existing

    def process_original_sample(self, values, samp, existing):

        ret = None

        #print('process original_sample {} {} {}'.format(values, samp, existing))

        if existing:

            ret = self.merge_original_samples(existing, samp, values)

        else:
            #print("Creating {}".format(samp))
            if len(samp.attrs) == 0:
                return None

            try:

                user = None
                if 'updated_by' in values:
                    user = values['updated_by']
                created = self._dao.create_original_sample(samp, user)

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

        user = None
        if 'updated_by' in values:
            user = values['updated_by']

        if parsed.original_sample_id:
            #print('Merging via service {} {}'.format(existing, parsed))
            ret = existing
            try:

                ret = self._dao.merge_original_samples(existing.original_sample_id,
                                                       parsed.original_sample_id,
                                                       user)

            except ApiException as err:
                msg = "Error updating merged original sample {} {} {} {}".format(values, parsed, existing, err)
                print(msg)
                self._logger.error(msg)
                #sys.exit(1)

            return ret

        existing, changed = self.merge_original_sample_objects(existing, parsed,
                                                               values)
        ret = existing

        if changed:

            # print("Updating {} to {}".format(parsed, existing))
            try:
                existing = self._dao.update_original_sample(existing.original_sample_id,
                                                            existing, user)

                study_id = existing.study_name
                # print(self._studies_cache)
                if study_id[:4] in self._studies_cache:
                    cache = self._studies_cache[study_id[:4]]
                    self.update_attr_cache(cache, existing)

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

        # print('Merging original samples {} {} {}'.format(existing, samp, values))
        new_ident_value = False

        change_reasons = []

        new_ident_value = self.merge_attrs(samp, existing, change_reasons)

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
                    merged_event = self.sampling_event_processor.merge_events(se_existing, se_samp, values)
                    #print(se)
            else:
                existing.sampling_event_id = samp.sampling_event_id
            new_ident_value = True
            change_reasons.append('Set SamplingEvent')

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
        # print('\n'.join(change_reasons))

        return existing, new_ident_value
