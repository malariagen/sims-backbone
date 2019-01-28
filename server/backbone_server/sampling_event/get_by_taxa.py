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

                fields = '''SELECT sampling_events.id'''
                query_body = ''' FROM sampling_events
                LEFT JOIN original_samples os ON os.sampling_event_id = sampling_events.id
                LEFT JOIN taxonomy_identifiers ti ON ti.partner_species_id = os.partner_species_id
                LEFT JOIN studies ON studies.id = os.study_id
                WHERE ti.taxonomy_id = %s'''
                args = (taxa_id,)

                count_args = args
                count_query = 'SELECT COUNT(sampling_events.id) ' + query_body

                query_body = query_body + ''' ORDER BY doc, study_code, id'''

                if not (start is None and count is None):
                    query_body = query_body + ' LIMIT %s OFFSET %s'
                    args = args + (count, start)

                sampling_events = SamplingEvents(sampling_events=[], count=0)

                stmt = fields + query_body

                cursor.execute(stmt, args)

                samp_ids = []
                for samp_id in cursor:
                    samp_ids.append(samp_id)

                locations = {}
                sampling_events.sampling_events = []
                for samp_id in samp_ids:
                    event = SamplingEventFetch.fetch(cursor, samp_id, locations)
                    sampling_events.sampling_events.append(event)
                sampling_events.locations = locations

                if not (start is None and count is None):
                    cursor.execute(count_query, count_args)
                    sampling_events.count = cursor.fetchone()[0]
                else:
                    sampling_events.count = len(sampling_events.sampling_events)

                sampling_events.attr_types = []

                col_query = '''select distinct attr_type from sampling_event_attrs sea
                JOIN attrs a ON a.id=sea.attr_id
                JOIN sampling_events se ON se.id = sea.sampling_event_id
                JOIN original_samples os ON os.sampling_event_id = se.id
                LEFT JOIN taxonomy_identifiers ti ON ti.partner_species_id = os.partner_species_id
                WHERE ti.taxonomy_id = %s'''

                cursor.execute(col_query, (taxa_id,))
                for (attr_type,) in cursor:
                    sampling_events.attr_types.append(attr_type)

        return sampling_events
