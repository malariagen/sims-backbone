from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from backbone_server.event_set.edit import EventSetEdit
from backbone_server.event_set.fetch import EventSetFetch

from swagger_server.models.event_set import EventSet

import mysql.connector
from mysql.connector import errorcode
import psycopg2

import logging
import uuid

class EventSetPost():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def post(self, event_set_id, event_set):

        resp = None
        with self._connection:
            with self._connection.cursor() as cursor:

                stmt = '''INSERT INTO event_sets (id) VALUES (%s)'''
                args = (event_set_id,)

                try:
                    cursor.execute(stmt, args)

                    EventSetEdit.add_sampling_events(cursor, event_set_id, event_set.sampling_events)
                    EventSetEdit.add_notes(cursor, event_set_id, event_set.notes)

                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_DUP_ENTRY:
                        raise DuplicateKeyException("Error inserting event set {}".format(event_set_id)) from err
                    else:
                        self._logger.fatal(repr(error))
                except psycopg2.IntegrityError as err:
                    raise DuplicateKeyException("Error inserting event set {}".format(event_set_id)) from err
                except DuplicateKeyException as err:
                    raise err

                resp = EventSetFetch.fetch(cursor, event_set_id)

        return resp



