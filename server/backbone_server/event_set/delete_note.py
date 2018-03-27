from backbone_server.errors.missing_key_exception import MissingKeyException

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

        ret = None

        with self._connection:
            with self._connection.cursor() as cursor:

                event_set_id = EventSetFetch.fetch_event_set_id(cursor,event_set_name)

                stmt = '''SELECT note_name FROM event_set_notes WHERE event_set_id = %s AND note_name = %s'''

                cursor.execute( stmt, (event_set_id, note_name))

                res = cursor.fetchone()

                if not res:
                    raise MissingKeyException("No such event set note {} {}".format(event_set_name,
                                                                                   note_name))

                try:

                    stmt = '''DELETE FROM event_set_notes WHERE event_set_id = %s AND note_name = %s'''
                    cursor.execute(stmt, (event_set_id, note_name))

                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_DUP_ENTRY:
                        raise MissingKeyException("Error deleting event set note {} {}".format(event_set_id, note_name)) from err
                    else:
                        self._logger.fatal(repr(error))
                except psycopg2.IntegrityError as err:
                    raise MissingKeyException("Error deleting event set note {} {}".format(event_set_id, note_name)) from err
                except MissingKeyException as err:
                    raise err

                ret = EventSetFetch.fetch(cursor, event_set_id, 0, 0)


        return ret

