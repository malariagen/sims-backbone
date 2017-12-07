from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from backbone_server.event_set.edit import EventSetEdit
from backbone_server.event_set.fetch import EventSetFetch

import mysql.connector
from mysql.connector import errorcode
import psycopg2

import logging

class EventSetDeleteNote():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def delete(self, event_set_name, note_name):

        with self._connection:
            with self._connection.cursor() as cursor:

                event_set_id = EventSetFetch.fetch_event_set_id(cursor,event_set_name)

                try:

                    stmt = '''DELETE FROM event_set_notes WHERE event_set_id = %s AND note_name = %s'''
                    cursor.execute(stmt, (event_set_id, note.note_name))

                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_DUP_ENTRY:
                        raise DuplicateKeyException("Error deleting event set note {} {}".format(event_set_id, note_name)) from err
                    else:
                        self._logger.fatal(repr(error))
                except psycopg2.IntegrityError as err:
                    raise DuplicateKeyException("Error deleting event set note {} {}".format(event_set_id, note_name)) from err
                except DuplicateKeyException as err:
                    raise err


        return EventSetFetch.fetch(event_set_id)

