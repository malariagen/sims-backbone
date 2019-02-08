from swagger_server.models.original_sample import OriginalSample

from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.original_sample.edit import OriginalSampleEdit

import logging

class OriginalSampleDelete():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def delete(self, original_sample_id):

        with self._connection:
            with self._connection.cursor() as cursor:

                return self.run_command(cursor, original_sample_id)

    def run_command(self, cursor, original_sample_id):

        stmt = '''UPDATE derivative_samples SET original_sample_id = NULL WHERE original_sample_id = %s'''

        cursor.execute( stmt, (original_sample_id,))

        stmt = '''DELETE FROM original_sample_attrs WHERE original_sample_id = %s'''

        cursor.execute( stmt, (original_sample_id,))

        stmt = '''DELETE FROM original_samples WHERE id = %s'''

        cursor.execute( stmt, (original_sample_id,))

        rc = cursor.rowcount

        OriginalSampleEdit.clean_up_taxonomies(cursor)


        if rc != 1:
            raise MissingKeyException("Error deleting original_sample {}".format(original_sample_id))


