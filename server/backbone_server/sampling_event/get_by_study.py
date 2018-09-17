from swagger_server.models.sampling_event import SamplingEvent
from swagger_server.models.sampling_events import SamplingEvents
from swagger_server.models.location import Location
from swagger_server.models.attr import Attr
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.location.fetch import LocationFetch
from backbone_server.sampling_event.fetch import SamplingEventFetch

from backbone_server.sampling_event.edit import SamplingEventEdit

import logging

class SamplingEventsGetByStudy():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, study_name, start, count):
        with self._connection:
            with self._connection.cursor() as cursor:

                study_id = SamplingEventEdit.fetch_study_id(cursor, study_name, False)

                if not study_id:
                    raise MissingKeyException("No study {}".format(study_name))

                fields = '''SELECT v_sampling_events.id, study_id, doc, doc_accuracy,
                                partner_species, v_sampling_events.partner_species_id,
                                location_id, latitude, longitude, accuracy, curated_name, curation_method, country, notes, partner_name,
                                proxy_location_id, proxy_latitude, proxy_longitude, proxy_accuracy,
                                proxy_curated_name, proxy_curation_method, proxy_country, proxy_notes,
                                proxy_partner_name'''
                query_body = ''' FROM v_sampling_events
                        WHERE studies_id = %s'''
                args = (study_id,)

                count_args = args
                count_query = 'SELECT COUNT(v_sampling_events.id) ' + query_body

                query_body = query_body + ''' ORDER BY doc, id'''

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

                sampling_events.attr_types = []

                col_query = '''select distinct attr_type from sampling_event_attrs se
                JOIN attrs a ON se.sampling_event_id=a.id WHERE a.study_id = %s'''

                cursor.execute(col_query, (study_id,))
                for (attr_type,) in cursor:
                    sampling_events.attr_types.append(attr_type)

        return sampling_events
