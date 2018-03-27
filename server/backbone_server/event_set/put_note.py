from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from backbone_server.event_set.edit import EventSetEdit
from backbone_server.event_set.fetch import EventSetFetch

import psycopg2

import logging

class EventSetPutNote():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def put(self, event_set_name, note):

        ret = None

        with self._connection:
            with self._connection.cursor() as cursor:

                event_set_id = EventSetFetch.fetch_event_set_id(cursor,event_set_name)

                try:
                    stmt = '''UPDATE event_set_notes SET note_text = %s WHERE event_set_id = %s AND note_name = %s'''

                    cursor.execute(stmt, (note.note_text, event_set_id, note.note_name))

                except psycopg2.IntegrityError as err:
                    raise DuplicateKeyException("Error updating event set note {} {}".format(event_set_id, note_name)) from err
                except DuplicateKeyException as err:
                    raise err


                ret = EventSetFetch.fetch(cursor, event_set_id, 0, 0)

        return ret

