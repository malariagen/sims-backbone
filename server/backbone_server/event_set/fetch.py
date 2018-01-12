from swagger_server.models.sampling_event import SamplingEvent
from swagger_server.models.event_set_note import EventSetNote
from swagger_server.models.event_set import EventSet

from swagger_server.models.location import Location
from swagger_server.models.identifier import Identifier

from backbone_server.sampling_event.fetch import SamplingEventFetch

from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

from backbone_server.location.fetch import LocationFetch

class EventSetFetch():

    @staticmethod
    def fetch_event_set_id(cursor, event_set_name):

        stmt = '''SELECT id FROM event_sets WHERE event_set_name = %s'''

        cursor.execute( stmt, (event_set_name,))

        res = cursor.fetchone()

        if not res:
            raise MissingKeyException("No such event set {}".format(event_set_name))

        return res[0]

    @staticmethod
    def fetch(cursor, event_set_id):

        if not event_set_id:
            return None

        stmt = '''SELECT event_set_name FROM event_sets WHERE id = %s'''

        cursor.execute(stmt, (event_set_id,))

        res = cursor.fetchone()

        event_set = EventSet(res[0])

        stmt = '''SELECT id, study_id, doc, doc_accuracy,
                        partner_species, partner_species_id,
                        location_id, latitude, longitude, accuracy, curated_name, curation_method, country, notes, partner_name, 
                        proxy_location_id, proxy_latitude, proxy_longitude, proxy_accuracy,
                        proxy_curated_name, proxy_curation_method, proxy_country, proxy_notes,
                        proxy_partner_name FROM v_sampling_events
                        JOIN event_set_members esm ON esm.sampling_event_id = v_sampling_events.id
                        WHERE esm.event_set_id = %s'''

        cursor.execute(stmt, (event_set_id,))

        sample = None
        samples = []
        for (sample_id, study_id, doc, doc_accuracy, partner_species, partner_species_id,
             location_id, latitude, longitude, accuracy,
             curated_name, curation_method, country, notes,
             partner_name, proxy_location_id, proxy_latitude, proxy_longitude, proxy_accuracy,
             proxy_curated_name, proxy_curation_method,
             proxy_country, proxy_notes, proxy_partner_name) in cursor:
            sample = SamplingEvent(sample_id, study_id=study_id,
                                   doc=doc, doc_accuracy=doc_accuracy,
                                   partner_species=partner_species)
            sample.location_id = location_id
            sample.proxy_location_id = proxy_location_id
            if location_id:
                location = Location(location_id,
                                    latitude, longitude, accuracy,
                                    curated_name, curation_method, country, notes)
                #This will only return the identifier for the event study
                if partner_name:
                    ident = Identifier(identifier_type='partner_name',
                                       identifier_value=partner_name,
                                       study_name=study_id)
                    location.identifiers = [ident]
                sample.location = location
            if proxy_location_id:
                location = Location(proxy_location_id,
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

            samples.append(sample)

        for sample in samples:
            sample.identifiers = SamplingEventFetch.fetch_identifiers(cursor, sample.sampling_event_id)

        event_set.sampling_events = samples

        stmt = '''SELECT note_name, note_text FROM event_set_notes WHERE event_set_id = %s'''

        cursor.execute(stmt, (event_set_id,))

        event_set.notes = []
        for (name, value) in cursor:
            note = EventSetNote(name, value)
            event_set.notes.append(note)

        if len(event_set.notes) == 0:
            event_set.notes = None

        return event_set

