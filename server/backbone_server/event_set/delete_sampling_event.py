from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.event_set.edit import EventSetEdit
from backbone_server.event_set.fetch import EventSetFetch

from openapi_server.models.sampling_event import SamplingEvent

import psycopg2

import logging

class EventSetDeleteSamplingEvent():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def delete(self, event_set_name, sampling_event_id):

        resp = None

        with self._connection:
            with self._connection.cursor() as cursor:

                event_set_id = EventSetFetch.fetch_event_set_id(cursor,event_set_name)

                stmt = '''DELETE FROM event_set_members WHERE event_set_id = %s AND sampling_event_id = %s'''
                cursor.execute(stmt, (event_set_id, sampling_event_id))

                if cursor.rowcount != 1:
                    raise MissingKeyException('Sampling event not found in event set {}'.format(event_set_name))

                resp = EventSetFetch.fetch(cursor, event_set_id, 0, 0)

        return resp

