from swagger_server.models.sampling_event import SamplingEvent
from swagger_server.models.sampling_events import SamplingEvents
from swagger_server.models.location import Location
from swagger_server.models.attr import Attr
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.location.fetch import LocationFetch
from backbone_server.sampling_event.fetch import SamplingEventFetch

from backbone_server.sampling_event.edit import SamplingEventEdit

import logging

class SamplingEventsGetByTaxa():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, taxa_id, start, count):
        with self._connection:
            with self._connection.cursor() as cursor:

                stmt = '''SELECT id FROM taxonomies WHERE id = %s'''
                cursor.execute(stmt, (taxa_id, ))
                vtaxa_id = None
                for tid in cursor:
                    vtaxa_id = tid

                if not vtaxa_id:
                    raise MissingKeyException("No taxa {}".format(taxa_id))

                fields = '''SELECT id, study_id, doc, doc_accuracy,
                                partner_species, v_sampling_events.partner_species_id,
                                location_id, latitude, longitude, accuracy, curated_name, curation_method, country, notes, partner_name,
                                proxy_location_id, proxy_latitude, proxy_longitude, proxy_accuracy,
                                proxy_curated_name, proxy_curation_method, proxy_country, proxy_notes,
                                proxy_partner_name'''
                query_body = ''' FROM v_sampling_events
                        LEFT JOIN taxonomy_identifiers ti ON ti.partner_species_id = v_sampling_events.partner_species_id
                        WHERE ti.taxonomy_id = %s'''
                args = (taxa_id,)

                count_args = args
                count_query = 'SELECT COUNT(id) ' + query_body

                query_body = query_body + ''' ORDER BY doc, study_id, id'''

                if not (start is None and count is None):
                    query_body = query_body + ' LIMIT %s OFFSET %s'
                    args = args + (count, start)

                sampling_events = SamplingEvents(sampling_events=[], count=0)

                stmt = fields + query_body

                cursor.execute(stmt, args)

                sampling_events.sampling_events, sampling_events.locations = SamplingEventFetch.load_sampling_events(cursor, True)

                if not (start is None and count is None):
                    cursor.execute(count_query, count_args)
                    sampling_events.count = cursor.fetchone()[0]
                else:
                    sampling_events.count = len(sampling_events.sampling_events)

        return sampling_events
