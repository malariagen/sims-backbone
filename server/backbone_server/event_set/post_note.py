from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.event_set.edit import EventSetEdit
from backbone_server.event_set.fetch import EventSetFetch

import mysql.connector
from mysql.connector import errorcode
import psycopg2

import logging

class EventSetPostNote():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def post(self, event_set_name, note_id, note):

        ret = None
        with self._connection:
            with self._connection.cursor() as cursor:

                event_set_id = EventSetFetch.fetch_event_set_id(cursor,event_set_name)

                try:

                    EventSetEdit.add_note(cursor, event_set_id, note)

                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_DUP_ENTRY:
                        raise DuplicateKeyException("Error inserting event set note {} {}".format(event_set_id, note)) from err
                    else:
                        self._logger.fatal(repr(error))
                except psycopg2.IntegrityError as err:
                    if err.pgcode == 23503:
                        raise MissingKeyException("Error inserting event set note {} {}".format(event_set_id, note)) from err
                    else:
                        raise DuplicateKeyException("Error inserting event set note {} {}".format(event_set_id, note)) from err
                except DuplicateKeyException as err:
                    raise err

        return ret

