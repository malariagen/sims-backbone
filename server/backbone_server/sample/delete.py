from swagger_server.models.sample import Sample

from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

class SampleDelete():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def __del__(self):
        if self._connection:
            self._connection.close()

    def delete(self, sample_id):

        cursor = self._connection.cursor()

        stmt = '''DELETE FROM identifiers WHERE sample_id = %s'''

        cursor.execute( stmt, (sample_id,))

        stmt = '''DELETE FROM samples WHERE id = %s'''

        cursor.execute( stmt, (sample_id,))

        rc = cursor.rowcount

        self._connection.commit()

        cursor.close()

        if rc != 1:
            raise MissingKeyException("Error deleting sample {}".format(sample_id))

