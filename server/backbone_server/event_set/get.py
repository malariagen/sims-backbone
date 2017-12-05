from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.event_set.fetch import EventSetFetch

import logging

class EventSetGetById():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, event_set_id):

        with self._connection:
            with self._connection.cursor() as cursor:

                event_set = EventSetFetch.fetch(cursor, event_set_id)

        if not event_set:
            raise MissingKeyException("No event_set {}".format(event_set_id))

        return event_set
