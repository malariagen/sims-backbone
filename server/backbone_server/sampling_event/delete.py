from swagger_server.models.sampling_event import SamplingEvent

from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

class SamplingEventDelete():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def delete(self, sample_id):

        with self._connection:
            with self._connection.cursor() as cursor:

                stmt = '''DELETE FROM identifiers WHERE sample_id = %s'''

                cursor.execute( stmt, (sample_id,))

                stmt = '''DELETE FROM event_set_members WHERE sampling_event_id = %s'''

                cursor.execute( stmt, (sample_id,))

                stmt = '''DELETE FROM samples WHERE id = %s'''

                cursor.execute( stmt, (sample_id,))

                rc = cursor.rowcount


        if rc != 1:
            raise MissingKeyException("Error deleting sample {}".format(sample_id))


