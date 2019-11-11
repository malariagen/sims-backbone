import logging

import psycopg2

from backbone_server.event_set.edit import EventSetEdit
from backbone_server.event_set.fetch import EventSetFetch

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

class EventSetPostNote():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def post(self, event_set_name, note_id, note, studies):

        ret = None
        with self._connection:
            with self._connection.cursor() as cursor:

                event_set_id = EventSetFetch.fetch_event_set_id(cursor, event_set_name)

                try:

                    EventSetEdit.add_note(cursor, event_set_id, note)

                except psycopg2.IntegrityError as err:
                    raise DuplicateKeyException("Error inserting event set note {} {}".format(event_set_id, note)) from err

        return ret
