
from backbone_server.errors.missing_key_exception import MissingKeyException


import logging

class SamplingEventDelete():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def delete(self, sampling_event_id):

        with self._connection:
            with self._connection.cursor() as cursor:

                stmt = '''UPDATE original_samples SET sampling_event_id = NULL WHERE sampling_event_id = %s'''

                cursor.execute( stmt, (sampling_event_id,))

                stmt = '''DELETE FROM sampling_event_attrs WHERE sampling_event_id = %s'''

                cursor.execute( stmt, (sampling_event_id,))

                stmt = '''DELETE FROM event_set_members WHERE sampling_event_id = %s'''

                cursor.execute( stmt, (sampling_event_id,))

                stmt = '''DELETE FROM sampling_events WHERE id = %s'''

                cursor.execute( stmt, (sampling_event_id,))

                rc = cursor.rowcount


        if rc != 1:
            raise MissingKeyException("Error deleting sampling_event {}".format(sampling_event_id))


