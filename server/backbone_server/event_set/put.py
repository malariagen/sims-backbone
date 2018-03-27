from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from backbone_server.event_set.edit import EventSetEdit
from backbone_server.event_set.fetch import EventSetFetch

from swagger_server.models.event_set import EventSet

import mysql.connector
from mysql.connector import errorcode
import psycopg2

import logging

class EventSetPut():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def put(self, event_set_name, event_set):

        ret = None
        with self._connection:
            with self._connection.cursor() as cursor:

                event_set_id = EventSetFetch.fetch_event_set_id(cursor,event_set_name)

                args = (event_set_id,)

                try:

                    #Allows the possibility of editing the metadata without the events
                    if event_set.members and len(event_set.members.sampling_events) > 0:
                        stmt = '''DELETE FROM event_set_members WHERE event_set_id = %s'''
                        cursor.execute(stmt, args)

                        EventSetEdit.add_sampling_events(cursor, event_set_id,
                                                         event_set.members.sampling_events)

                    stmt = '''DELETE FROM event_set_notes WHERE event_set_id = %s'''
                    cursor.execute(stmt, args)

                    EventSetEdit.add_notes(cursor, event_set_id, event_set.notes)

                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_DUP_ENTRY:
                        raise DuplicateKeyException("Error updating event set {} {}".format(event_set_id, event_set)) from err
                    else:
                        self._logger.fatal(repr(error))
                except psycopg2.IntegrityError as err:
                    raise DuplicateKeyException("Error updating event set {} {}".format(event_set_id, event_set)) from err
                except DuplicateKeyException as err:
                    raise err

                ret = EventSetFetch.fetch(cursor, event_set_id, None, None)


        return ret

