import logging

from openapi_server.models.event_set import EventSet
from openapi_server.models.event_sets import EventSets

class EventSetsGet():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, studies):

        sets = []

        with self._connection:
            with self._connection.cursor() as cursor:

                stmt = '''SELECT event_set_name from event_sets'''

                cursor.execute(stmt)

                for (esid,) in cursor:
                    e = EventSet(esid)
                    sets.append(e)

        event_sets = EventSets()

        event_sets.event_sets = sets

        return event_sets
