from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from backbone_server.event_set.edit import EventSetEdit
from backbone_server.event_set.fetch import EventSetFetch

from swagger_server.models.event_set import EventSet

import mysql.connector
from mysql.connector import errorcode
import psycopg2

import logging

class EventSetDelete():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def delete(self, event_set_id):

        with self._connection:
            with self._connection.cursor() as cursor:

                args = (event_set_id,)

                try:
                    stmt = '''DELETE FROM event_set_members WHERE event_set_id = %s'''
                    cursor.execute(stmt, args)

                    stmt = '''DELETE FROM event_set_notes WHERE event_set_id = %s'''
                    cursor.execute(stmt, args)

                    stmt = '''DELETE FROM event_sets WHERE id = %s'''
                    cursor.execute(stmt, args)

                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_DUP_ENTRY:
                        raise DuplicateKeyException("Error deleting event set {}".format(event_set_id)) from err
                    else:
                        self._logger.fatal(repr(error))
                except psycopg2.IntegrityError as err:
                    raise DuplicateKeyException("Error deleting event set {}".format(event_set_id)) from err
                except DuplicateKeyException as err:
                    raise err


        return None

