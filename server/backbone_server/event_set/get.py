from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.event_set.fetch import EventSetFetch

import logging

class EventSetGetById():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, event_set_name, studies, start, count):

        with self._connection:
            with self._connection.cursor() as cursor:

                event_set_id = EventSetFetch.fetch_event_set_id(cursor, event_set_name)

                event_set = EventSetFetch.fetch(cursor, event_set_id, studies, start,
                                                count)

        return event_set
