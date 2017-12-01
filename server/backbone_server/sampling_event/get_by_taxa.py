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

                stmt = '''SELECT DISTINCT samples.id FROM samples
                LEFT JOIN taxonomy_identifiers ti ON ti.partner_species_id = samples.partner_species_id
                WHERE ti.taxonomy_id = %s'''

                cursor.execute(stmt, (taxa_id, ))

                samples = SamplingEvents([], 0)
                event_ids = []

                for sample_id in cursor:
                    event_ids.append(sample_id)

                for sample_id in event_ids:
                    sample = SamplingEventFetch.fetch(cursor, sample_id)
                    samples.sampling_events.append(sample)
                    samples.count = samples.count + 1


        return samples
