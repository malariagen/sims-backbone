from swagger_server.models.location import Location
from swagger_server.models.identifier import Identifier
from swagger_server.models.taxonomy import Taxonomy
from swagger_server.models.sampling_event import SamplingEvent
from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

from backbone_server.location.fetch import LocationFetch

class SamplingEventFetch():


    @staticmethod
    def fetch_identifiers(cursor, sampling_event_id):

        stmt = '''SELECT identifier_type, identifier_value, identifier_source FROM identifiers
        WHERE sampling_event_id = %s
                ORDER BY identifier_type, identifier_value, identifier_source'''

        cursor.execute(stmt, (sampling_event_id,))

        identifiers = []
        for (name, value, source) in cursor:
            ident = Identifier(name, value, source)
            identifiers.append(ident)

        if len(identifiers) == 0:
            identifiers = None

        return identifiers

    @staticmethod
    def fetch_event_sets(cursor, sampling_event_id):

        stmt = '''select event_set_name FROM event_set_members 
        JOIN event_sets ON event_set_id = event_sets.id 
        WHERE sampling_event_id = %s'''

        cursor.execute(stmt, (sampling_event_id,))

        identifiers = []
        for (name,) in cursor:
            identifiers.append(name)

        if len(identifiers) == 0:
            identifiers = None

        return identifiers


    @staticmethod
    def fetch_taxonomies(cursor, study_id, partner_species):

        ret = None

        if not study_id:
            return None

        if not partner_species:
            return None

        stmt = '''select DISTINCT taxonomy_id FROM taxonomy_identifiers ti
                    JOIN partner_species_identifiers psi ON ti.partner_species_id=psi.id
                    JOIN studies s ON psi.study_id=s.id
                    WHERE partner_species = %s AND s.study_name = %s'''

        cursor.execute(stmt, (partner_species, study_id))

        partner_taxonomies = []
        for (taxa_id,) in cursor:
            taxa = Taxonomy(taxa_id)
            partner_taxonomies.append(taxa)

        if len(partner_taxonomies) == 0:
            partner_taxonomies = None

        return partner_taxonomies

    @staticmethod
    def fetch(cursor, sampling_event_id, locations=None):

        if not sampling_event_id:
            return None

        stmt = '''SELECT sampling_events.id, studies.study_name AS study_id, doc, doc_accuracy,
                            partner_species, partner_species_id, location_id, proxy_location_id
        FROM sampling_events
        LEFT JOIN studies ON studies.id = sampling_events.study_id
        LEFT JOIN partner_species_identifiers ON partner_species_identifiers.id = sampling_events.partner_species_id
        WHERE sampling_events.id = %s'''
        cursor.execute( stmt, (sampling_event_id,))

        sampling_event = None

        for (sampling_event_id, study_id, doc, doc_accuracy, partner_species, partner_species_id, location_id, proxy_location_id) in cursor:
            sampling_event = SamplingEvent(str(sampling_event_id), study_name = study_id, 
                                   doc = doc, doc_accuracy = doc_accuracy,
                                   partner_species = partner_species)
            if location_id:
                sampling_event.location_id = str(location_id)
                sampling_event.public_location_id = str(location_id)
            if proxy_location_id:
                sampling_event.proxy_location_id = str(proxy_location_id)
                sampling_event.public_location_id = str(proxy_location_id)

        if not sampling_event:
            return sampling_event

        sampling_event.identifiers = SamplingEventFetch.fetch_identifiers(cursor, sampling_event_id)

        sampling_event.partner_taxonomies = SamplingEventFetch.fetch_taxonomies(cursor, study_id,
                                                                        partner_species)

        sampling_event.event_sets = SamplingEventFetch.fetch_event_sets(cursor, sampling_event_id)

        if sampling_event.location_id:
            location = LocationFetch.fetch(cursor, sampling_event.location_id)
            if locations is not None:
                if sampling_event.location_id not in locations:
                    locations[sampling_event.location_id] = location
            else:
                sampling_event.location = location
        if sampling_event.proxy_location_id:
            proxy_location = LocationFetch.fetch(cursor, sampling_event.proxy_location_id)
            if locations is not None:
                if sampling_event.proxy_location_id not in locations:
                    locations[sampling_event.proxy_location_id] = proxy_location
            else:
                sampling_event.proxy_location = proxy_location

        return sampling_event

    @staticmethod
    def load_sampling_events(cursor, all_identifiers=True):

        sampling_events = []
        location_list = []

        for (sampling_event_id, study_id, doc, doc_accuracy, partner_species, partner_species_id,
             location_id, latitude, longitude, accuracy,
             curated_name, curation_method, country, notes,
             partner_name, proxy_location_id, proxy_latitude, proxy_longitude, proxy_accuracy,
             proxy_curated_name, proxy_curation_method,
             proxy_country, proxy_notes, proxy_partner_name) in cursor:
            sampling_event = SamplingEvent(str(sampling_event_id), study_name=study_id,
                                   doc=doc, doc_accuracy=doc_accuracy,
                                   partner_species=partner_species)
            if location_id:
                sampling_event.location_id = str(location_id)
                sampling_event.public_location_id = str(location_id)
                if not str(location_id) in location_list:
                    location_list.append(str(location_id))
            if proxy_location_id:
                sampling_event.proxy_location_id = str(proxy_location_id)
                sampling_event.public_location_id = str(proxy_location_id)
                if not str(proxy_location_id) in location_list:
                    location_list.append(str(proxy_location_id))

            sampling_events.append(sampling_event)

        for sampling_event in sampling_events:
            sampling_event.identifiers = SamplingEventFetch.fetch_identifiers(cursor,
                                                                              sampling_event.sampling_event_id)
            sampling_event.partner_taxonomies = SamplingEventFetch.fetch_taxonomies(cursor,
                                                                                    sampling_event.study_name,
                                                                        sampling_event.partner_species)

        locations = {}

        for location_id in location_list:
                location = LocationFetch.fetch(cursor, location_id)
                locations[location_id] = location

        return sampling_events, locations
