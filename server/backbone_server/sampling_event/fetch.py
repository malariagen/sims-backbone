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

        stmt = '''SELECT identifier_type, identifier_value, identifier_source FROM identifiers WHERE sample_id = %s'''

        cursor.execute(stmt, (sampling_event_id,))

        identifiers = []
        for (name, value, source) in cursor:
            ident = Identifier(name, value, source)
            identifiers.append(ident)

        if len(identifiers) == 0:
            identifiers = None

        return identifiers


    @staticmethod
    def fetch(cursor, sampling_event_id):

        if not sampling_event_id:
            return None

        stmt = '''SELECT samples.id, studies.study_name AS study_id, doc, doc_accuracy,
                            partner_species, partner_species_id, location_id, proxy_location_id
        FROM samples
        LEFT JOIN studies ON studies.id = samples.study_id
        LEFT JOIN partner_species_identifiers ON partner_species_identifiers.id = samples.partner_species_id
        WHERE samples.id = %s'''
        cursor.execute( stmt, (sampling_event_id,))

        sample = None

        for (sample_id, study_id, doc, doc_accuracy, partner_species, partner_species_id, location_id, proxy_location_id) in cursor:
            sample = SamplingEvent(str(sample_id), study_id = study_id, 
                                   doc = doc, doc_accuracy = doc_accuracy,
                                   partner_species = partner_species)
            sample.location_id = str(location_id)
            sample.proxy_location_id = str(proxy_location_id)
            if location_id:
                location = LocationFetch.fetch(cursor, location_id)
                sample.location = location
                sample.public_location_id = str(location_id)
                sample.public_location = location
            if proxy_location_id:
                proxy_location = LocationFetch.fetch(cursor, proxy_location_id)
                sample.proxy_location = proxy_location
                sample.public_location_id = str(proxy_location_id)
                sample.public_location = proxy_location

        if not sample:
            return sample


        sample.identifiers = SamplingEventFetch.fetch_identifiers(cursor, sampling_event_id)

        if sample.study_id:

            stmt = '''select taxonomy_id FROM taxonomy_identifiers WHERE partner_species_id = %s'''

            cursor.execute(stmt, (partner_species_id,))

            sample.partner_taxonomies = []
            for (taxa_id) in cursor:
                taxa = Taxonomy(taxa_id)
                sample.partner_taxonomies.append(taxa)

            if len(sample.partner_taxonomies) == 0:
                sample.partner_taxonomies = None

        return sample

    @staticmethod
    def load_sampling_events(cursor, all_identifiers=False):

        samples = []
        for (sample_id, study_id, doc, doc_accuracy, partner_species, partner_species_id,
             location_id, latitude, longitude, accuracy,
             curated_name, curation_method, country, notes,
             partner_name, proxy_location_id, proxy_latitude, proxy_longitude, proxy_accuracy,
             proxy_curated_name, proxy_curation_method,
             proxy_country, proxy_notes, proxy_partner_name) in cursor:
            sample = SamplingEvent(str(sample_id), study_id=study_id,
                                   doc=doc, doc_accuracy=doc_accuracy,
                                   partner_species=partner_species)
            sample.location_id = str(location_id)
            sample.proxy_location_id = str(proxy_location_id)
            if location_id:
                location = Location(str(location_id),
                                    latitude, longitude, accuracy,
                                    curated_name, curation_method, country, notes)
                #This will only return the identifier for the event study
                if partner_name:
                    ident = Identifier(identifier_type='partner_name',
                                       identifier_value=partner_name,
                                       study_name=study_id)
                    location.identifiers = [ident]
                sample.location = location
                sample.public_location_id = str(location_id)
                sample.public_location = location
            if proxy_location_id:
                location = Location(str(proxy_location_id),
                                    proxy_latitude, proxy_longitude,
                                    proxy_accuracy,
                                    proxy_curated_name, proxy_curation_method, proxy_country,
                                    proxy_notes)
                #This will only return the identifier for the event study
                if proxy_partner_name:
                    ident = Identifier(identifier_type='partner_name',
                                       identifier_value=proxy_partner_name,
                                       study_name=study_id)
                    location.identifiers = [ident]
                sample.proxy_location = location
                sample.public_location_id = str(proxy_location_id)
                sample.public_location =location

            samples.append(sample)

        for sample in samples:
            sample.identifiers = SamplingEventFetch.fetch_identifiers(cursor, sample.sampling_event_id)

        return samples
