from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from backbone_server.event_set.edit import EventSetEdit
from backbone_server.event_set.fetch import EventSetFetch

from swagger_server.models.event_set import EventSet

import psycopg2

import logging

class EventSetDelete():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def delete(self, event_set_name):

        with self._connection:
            with self._connection.cursor() as cursor:

                return self.run_command(cursor, event_set_name)

    def run_command(self, cursor, event_set_name):

        event_set_id = EventSetFetch.fetch_event_set_id(cursor,event_set_name)

        args = (event_set_id,)

        stmt = '''DELETE FROM event_set_members WHERE event_set_id = %s'''
        cursor.execute(stmt, args)

        stmt = '''DELETE FROM event_set_notes WHERE event_set_id = %s'''
        cursor.execute(stmt, args)

        stmt = '''DELETE FROM event_sets WHERE id = %s'''
        cursor.execute(stmt, args)

        return None

