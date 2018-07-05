
import sys
from copy import deepcopy
import datetime

import logging

from decimal import *

import swagger_client
from swagger_client.rest import ApiException

from base_entity import BaseEntity

class SamplingEventProcessor(BaseEntity):

    _sample_cache = {}

    def __init__(self, dao, event_set):
        super().__init__(dao, event_set)
        self._logger = logging.getLogger(__name__)

    """
        returns true if the attr is already in, or successfully added to, the location
    """
    def add_location_attr(self, study_id, looked_up, ident_type, partner_name, values):

        if not looked_up:
            return False

        ret = False

        found = False
        if looked_up.attrs and study_id:
            for ident in looked_up.attrs:
#                print(ident)
#                print(study_id)
                if ident.study_name[:4] == study_id[:4] and \
                    ident.attr_value == partner_name:
                    found = True

        if not found:
            existing_location = deepcopy(looked_up)
            #print("adding attr1 {}".format(looked_up))
            if not looked_up.attrs:
                looked_up.attrs = []
            #print("values: {} {}".format(study_id, partner_name))
            if study_id and partner_name:
#                print("adding attr {}".format(looked_up.attrs))
                new_ident = swagger_client.Attr( attr_type = 'partner_name', 
                                                      attr_value = partner_name,
                                                      attr_source = self._event_set, 
                                                      study_name = study_id)
                #print("adding attr2 {}".format(new_ident))
                looked_up.attrs.append(new_ident)
                #print("adding attr3 {}".format(looked_up))
                try:
                    updated = self._dao.update_location(looked_up.location_id, looked_up)
                    ret = True
                except ApiException as err:
                    #print("Error adding location attr {} {}".format(looked_up, err))
                    message = 'duplicate location:{}:{}'.format(ident_type,partner_name)
                    try:
                        conflict = self._dao.download_partner_location(partner_name)
                        if conflict and conflict.locations:
                            conflict_loc = self._dao.download_location(conflict.locations[0].location_id)
                            conflict_loc = self._dao.download_gps_location(looked_up.latitude,
                                                                              looked_up.longitude)
                            self.report_conflict(None, "Location name", existing_location,
                                                 conflict_loc, message, values)
                        else:
                            self.report('No conflict on error: {}'.format(partner_name), values)
                    except ApiException as err:
                        try:
                            conflict_loc = self._dao.download_gps_location(looked_up.latitude,
                                                                              looked_up.longitude)
                            for loc in conflict_loc.locations:
                                for cname in loc.attrs:
                                    if cname.study_name[:4] == study_id[:4]:
                                        message = message + ':' + cname.attr_value
                                self.report_conflict(None, "Location name", looked_up,
                                                     loc, message, values)
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

        loc.attrs = [
            swagger_client.Attr(attr_type='partner_name',
                                      attr_value=partner_name,
                                      attr_source=self._event_set, study_name=study_id)
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
            loc.notes = self._event_set + ' ' + values['description']
        else:
            loc.notes = self._event_set

        #print(values)
        #print(loc)

        return partner_name, loc

    def lookup_location(self, study_id, loc, partner_name, values):

        looked_up_location = None
        conflict = False
        looked_up = None

        try:
            looked_up = self._dao.download_gps_location(str(loc.latitude), str(loc.longitude))
        except Exception as err:
            #print(repr(err))
            #print("Failed to find location {}".format(loc))
            return looked_up_location, conflict

        if not looked_up and not partner_name == "##Unknown":
            try:
                named_locations = self._dao.download_partner_location(partner_name)
                for named_loc in named_locations.locations:
                    for ident in named_loc.attrs:
                        if ident.study_name[:4] == study_id[:4]:
                            if loc.latitude and loc.longitude:
                                self.report_conflict(None, "Location name", loc,
                                                     named_loc,
                                                     partner_name, values)
                                conflict = True
                            else:
                                looked_up_location = named_loc
            except ApiException as err:
                #Can't be found by name either
                pass
        elif looked_up.count > 0:
            name_match = False
            for loc in looked_up.locations:
                for ident in loc.attrs:
                    if ident.attr_type == 'partner_name' and \
                       ident.attr_value == partner_name and \
                       ident.study_name[:4] == study_id[:4]:
                        name_match = True
                        looked_up_location = loc
            if not name_match:
                looked_up = None


        return looked_up_location, conflict

    def process_location(self, values, prefix):

        partner_name, loc = self.create_location_from_values(values, prefix)

        if loc is None:
            return None, None

        study_id = None

        if 'study_id' in values:
            study_id = values['study_id'][:4]

        looked_up, conflict = self.lookup_location(study_id, loc, partner_name, values)

        return self.merge_locations(loc, looked_up, study_id, prefix, partner_name, values)

    def merge_locations(self, loc, looked_up, study_id, prefix, partner_name, values):
        ret = None

        if looked_up is not None:
            try:
                #print("Found location {}".format(looked_up))
                loc.location_id = looked_up.location_id
                added_id = self.add_location_attr(study_id, looked_up, prefix, partner_name, values)

                if added_id:
                    try:

                        loc.location_id = None
                        try:
                            ret = self.update_country(loc.country, looked_up)
                        except Exception as err:
                            self.report_conflict(None, 'Country', looked_up.country,
                                                     loc.country, 'not updated', values)
                    except Exception as err:
                        #Either a duplicate or country conflict
                        self.report(err, values)

            except Exception as err:
                print(repr(err))
                #print("Failed to find location {}".format(loc))
#        elif not conflict:
        else:

            try:
                created = self._dao.create_location(loc)
                ret = created
            #    print("Created location {}".format(created))
            except ApiException as err:
                if err.status == 422:
                    self.report_conflict(None, "Location name", None,
                                         loc, 'Error creating location', values)
                else:
                    self.report("Error creating location {} {}".format(loc, err), values)
                return None, None

        return partner_name, ret

    def create_sampling_event_from_values(self, values):

        doc = None
        doc_accuracy = None
        study_id = None
        ret = None

        idents = []
        if 'sample_individual_id' in values:
            idents.append(swagger_client.Attr ('individual_id', values['sample_individual_id'],
                                                     self._event_set))
        if 'roma_pk_id' in values:
            idents.append(swagger_client.Attr ('roma_pk_id', values['roma_pk_id'],
                                                     self._event_set))


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

        samp.attrs = idents
        #print(values)
        #print(samp)
        return samp


    def merge_events(self, existing, found, values):

        if not found:
            return existing

        ret = existing

        try:

            ret = self._dao.merge_sampling_events(existing.sampling_event_id,
                                               found.sampling_event_id)
        except ApiException as err:
            msg = "Error updating merged sampling events {} {} {} {}".format(values, found, existing, err)
            #print(msg)
            self.report_conflict(existing, "SamplingEvent", existing,
                                                 found, err.reason, values)
            self._logger.error(msg)
            #sys.exit(1)

        return ret

#        existing, changed = self.merge_sampling_event_objects(existing, found,
#                                                              values)
#        ret = existing
#
#        if changed:
#
#            for event_set in found.event_sets:
#                self._dao.create_event_set_item(event_set, existing.sampling_event_id)
#
#            self._dao.delete_sampling_event(found.sampling_event_id)
#
#            #print("Updating {} to {}".format(orig, existing))
#            existing = self._dao.update_sampling_event(existing.sampling_event_id, existing)
#        else:
#            pass
#            #self.report("Merge didn't change anything {} {}".format(existing, found), None)
#
#        return existing
#
    def lookup_sampling_event(self, original_sample, samp, loc, proxy_loc, values):

        #print('Looking up sampling event {} {} {}'.format(original_sample, samp, values))

        existing = None

        if 'unique_id' in values:
            if values['unique_id'] in self._sample_cache:
                existing_sample_id = self._sample_cache[values['unique_id']]
                existing = self._dao.download_sampling_event(existing_sample_id)
                return existing

        if 'individual_id' in values:
            try:
                looked_up = self._dao.download_sampling_events_by_attr('individual_id',
                                                                       values['individual_id'])
                if looked_up.count > 0:
                    existing = looked_up.sampling_events[0]
            except ApiException as err:
                #self._logger.debug("Error looking for {}".format(ident))
                #print("Not found")
                pass
            return existing

        if 'roma_pk_id' in values:
            try:
                looked_up = self._dao.download_sampling_events_by_attr('roma_pk_id',
                                                                       values['roma_pk_id'])
                if looked_up.count > 0:
                    existing = looked_up.sampling_events[0]
            except ApiException as err:
                #self._logger.debug("Error looking for {}".format(ident))
                #print("Not found")
                pass
            return existing

        if original_sample and\
           original_sample.sampling_event_id:
            existing = self._dao.download_sampling_event(original_sample.sampling_event_id)
            if existing.location_id:
                if loc:
                    if existing.location_id != loc.location_id:
#                        print('Conflicting location existing != new')
                        existing.location_id = loc.location_id
                        existing.location = loc
#                else:
#                    print('Conflicting location new not set')
            elif loc:
#                print('Conflicting location existing not set')
                existing.location_id = loc.location_id
                existing.location = loc
            if existing.proxy_location_id:
                if proxy_loc:
                    if existing.location_id != proxy_loc.location_id:
#                        print('Conflicting proxy_location existing != new')
                        existing.proxy_location_id = proxy_loc.location_id
                        existing.proxy_location = proxy_loc
#                else:
#                    print('Conflicting proxy_location new not set')
            elif proxy_loc:
                print('Conflicting proxy_location existing not set')
                existing.proxy_location_id = proxy_loc.location_id
                existing.proxy_location = proxy_loc
            return existing

        for location in (loc, proxy_loc):
            if not location:
                continue
            try:
                found_events = self._dao.download_sampling_events_by_location(location.location_id)

                for found in found_events.sampling_events:

                    if samp.doc != found.doc:
                        continue
                    if samp.study_name[:4] != found.study_name[:4]:
                        continue
                    if samp.location_id != found.location_id:
                        continue
                    if proxy_loc:
                        if samp.location_id != found.proxy_location_id:
                            continue
                    if existing and existing.sampling_event_id != found.sampling_event_id:
                        #self.report("Merging into {} using {}"
                        #                .format(existing.sampling_event_id,
                        #                                   ident.attr_type), values)
                        found = self.merge_events(existing, found, values)
                    existing = found
                    if samp.study_name[:4] == '0000':
                        samp.study_name = existing.study_name
                            #print ("found: {} {}".format(samp, found))
            except ApiException as err:
                #self._logger.debug("Error looking for {}".format(ident))
                #print("Not found")
                pass

        return existing

    def merge_sampling_event_objects(self, existing, samp, values):

        orig = deepcopy(existing)
        new_ident_value = False

        change_reasons = []

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
                self.add_location_attr(existing.study_name, location, '', location_name,
                                             values)
                self.add_location_attr(existing.study_name, proxy_location, 'proxy_',
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
