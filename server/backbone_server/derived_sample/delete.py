from swagger_server.models.derived_sample import DerivedSample

from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

class DerivedSampleDelete():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def delete(self, derived_sample_id):

        with self._connection:
            with self._connection.cursor() as cursor:

                stmt = '''DELETE FROM derived_sample_attrs WHERE derived_sample_id = %s'''

                cursor.execute( stmt, (derived_sample_id,))

                stmt = '''DELETE FROM derived_samples WHERE id = %s'''

                cursor.execute( stmt, (derived_sample_id,))

                rc = cursor.rowcount


        if rc != 1:
            raise MissingKeyException("Error deleting derived_sample {}".format(derived_sample_id))


