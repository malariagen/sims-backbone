import logging

from openapi_server.models.event_set import EventSet

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.event_set.fetch import EventSetFetch

class EventSetPost():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def post(self, event_set_name, studies):

        resp = None
        with self._connection:
            with self._connection.cursor() as cursor:

                event_set_id = None
                try:
                    event_set_id = EventSetFetch.fetch_event_set_id(cursor, event_set_name)
                except MissingKeyException as err:
                    pass

                if event_set_id:
                    raise DuplicateKeyException("Error inserting event set already exists {}".format(event_set_name))

                stmt = '''INSERT INTO event_sets (event_set_name) VALUES (%s)'''

                args = (event_set_name,)

                cursor.execute(stmt, args)

                event_set_id = EventSetFetch.fetch_event_set_id(cursor, event_set_name)

                resp = EventSetFetch.fetch(cursor, event_set_id, studies, 0, 0)

        return resp
