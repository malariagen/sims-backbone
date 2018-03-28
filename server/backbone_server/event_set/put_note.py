from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from backbone_server.event_set.edit import EventSetEdit
from backbone_server.event_set.fetch import EventSetFetch

import psycopg2

import logging

class EventSetPutNote():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def put(self, event_set_name, note_id, note):

        ret = None

        with self._connection:
            with self._connection.cursor() as cursor:

                event_set_id = EventSetFetch.fetch_event_set_id(cursor,event_set_name)

                stmt = '''UPDATE event_set_notes SET note_text = %s, note_name = %s WHERE event_set_id = %s AND note_name = %s'''

                try:
                    cursor.execute(stmt, (note.note_text, note.note_name, event_set_id, note_id))
                except psycopg2.IntegrityError as err:
                    raise DuplicateKeyException("Error updating event set note id from {} to {} in {}".format(note_id, note.note_name, event_set_id )) from err

                if cursor.rowcount != 1:
                    raise MissingKeyException('No note {} in event set {}'.format(note.note_name,
                                                                                  event_set_name))

                ret = EventSetFetch.fetch(cursor, event_set_id, 0, 0)

        return ret

