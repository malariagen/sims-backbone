from swagger_server.models.derivative_sample import DerivativeSample

from backbone_server.errors.missing_key_exception import MissingKeyException

import psycopg2
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

        stmt = '''SELECT original_sample_id, parent_derivative_sample_id FROM derivative_samples WHERE id = %s'''

        cursor.execute(stmt, (derivative_sample_id,))

        original_sample_id = None
        parent_derivative_sample_id = None
        for (orig_sample_id, parent_deriv_sample_id) in cursor:
            original_sample_id = orig_sample_id
            parent_derivative_sample_id = parent_deriv_sample_id

        try:
            stmt = '''SELECT id FROM derivative_samples WHERE parent_derivative_sample_id = %s'''

            cursor.execute(stmt, (derivative_sample_id,))

            for (sample_id,) in cursor:
                if parent_derivative_sample_id:
                    stmt = '''UPDATE derivative_samples
                    SET parent_derivative_sample_id = %s
                    WHERE id = %s'''
                    cursor.execute(stmt, (parent_derivative_sample_id, sample_id,))
                elif original_sample_id:
                    stmt = '''UPDATE derivative_samples
                    SET original_sample_id = %s, parent_derivative_sample_id = NULL
                    WHERE id = %s'''
                    cursor.execute(stmt, (original_sample_id, sample_id,))
                else:
                    stmt = '''UPDATE derivative_samples
                    SET parent_derivative_sample_id = NULL
                    WHERE id = %s'''
                    cursor.execute(stmt, (sample_id,))
        except psycopg2.ProgrammingError as err:
            pass

        stmt = '''DELETE FROM derivative_sample_attrs WHERE derivative_sample_id = %s'''

        cursor.execute(stmt, (derivative_sample_id,))

        stmt = '''DELETE FROM derivative_samples WHERE id = %s'''

        cursor.execute(stmt, (derivative_sample_id,))

        rc = cursor.rowcount


        if rc != 1:
            raise MissingKeyException("Error deleting derivative_sample {}".format(derivative_sample_id))


