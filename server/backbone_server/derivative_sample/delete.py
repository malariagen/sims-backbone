from swagger_server.models.derivative_sample import DerivativeSample

from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

class DerivativeSampleDelete():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def delete(self, derivative_sample_id):

        with self._connection:
            with self._connection.cursor() as cursor:

                return self.run_command(cursor, derivative_sample_id)

    def run_command(self, cursor, derivative_sample_id):

        stmt = '''DELETE FROM derivative_sample_attrs WHERE derivative_sample_id = %s'''

        cursor.execute( stmt, (derivative_sample_id,))

        stmt = '''DELETE FROM derivative_samples WHERE id = %s'''

        cursor.execute( stmt, (derivative_sample_id,))

        rc = cursor.rowcount


        if rc != 1:
            raise MissingKeyException("Error deleting derivative_sample {}".format(derivative_sample_id))


