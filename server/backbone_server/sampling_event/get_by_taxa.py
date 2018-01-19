from swagger_server.models.sampling_event import SamplingEvent
from swagger_server.models.sampling_events import SamplingEvents
from swagger_server.models.location import Location
from swagger_server.models.identifier import Identifier
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.location.fetch import LocationFetch
from backbone_server.sampling_event.fetch import SamplingEventFetch

from backbone_server.sampling_event.edit import SamplingEventEdit

import logging

class SamplingEventsGetByTaxa():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, taxa_id):
        with self._connection:
            with self._connection.cursor() as cursor:

                stmt = '''SELECT id FROM taxonomies WHERE id = %s'''
                cursor.execute(stmt, (taxa_id, ))
                vtaxa_id = None
                for tid in cursor:
                    vtaxa_id = tid

                if not vtaxa_id:
                    raise MissingKeyException("No taxa {}".format(taxa_id))

                samples = SamplingEvents([], 0)

                stmt = '''SELECT id, study_id, doc, doc_accuracy,
                                partner_species, v_sampling_events.partner_species_id,
                                location_id, latitude, longitude, accuracy, curated_name, curation_method, country, notes, partner_name,
                                proxy_location_id, proxy_latitude, proxy_longitude, proxy_accuracy,
                                proxy_curated_name, proxy_curation_method, proxy_country, proxy_notes,
                                proxy_partner_name FROM v_sampling_events
                        LEFT JOIN taxonomy_identifiers ti ON ti.partner_species_id = v_sampling_events.partner_species_id
                        WHERE ti.taxonomy_id = %s'''

                cursor.execute(stmt, (taxa_id,))

                samples.sampling_events = SamplingEventFetch.load_sampling_events(cursor, True)
                samples.count = len(samples.sampling_events)


        return samples
