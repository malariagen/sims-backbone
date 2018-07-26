from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.derivative_sample.edit import DerivativeSampleEdit
from backbone_server.derivative_sample.fetch import DerivativeSampleFetch

from swagger_server.models.derivative_sample import DerivativeSample

import psycopg2

import logging

class DerivativeSamplePut():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def put(self, derivative_sample_id, derivative_sample):

        with self._connection:
            with self._connection.cursor() as cursor:

                stmt = '''SELECT id FROM derivative_samples WHERE id = %s'''
                cursor.execute( stmt, (derivative_sample_id,))

                existing_derivative_sample = None

                for (derivative_sample_id,) in cursor:
                    existing_derivative_sample = DerivativeSample(derivative_sample_id)

                if not existing_derivative_sample:
                    raise MissingKeyException("Could not find derivative_sample to update {}".format(derivative_sample_id))

                stmt = '''UPDATE derivative_samples 
                            SET original_sample_id = %s,
                            dna_prep = %s
                            WHERE id = %s'''
                args = (derivative_sample.original_sample_id,
                        derivative_sample.dna_prep,
                        derivative_sample_id)

                try:
                    cursor.execute(stmt, args)
                    rc = cursor.rowcount

                    cursor.execute('DELETE FROM derivative_sample_attrs WHERE derivative_sample_id = %s',
                                   (derivative_sample_id,))

                    DerivativeSampleEdit.add_attrs(cursor, derivative_sample_id, derivative_sample)

                except psycopg2.IntegrityError as err:
                    raise DuplicateKeyException("Error updating derivative_sample {}".format(derivative_sample)) from err
                except DuplicateKeyException as err:
                    raise err

                derivative_sample = DerivativeSampleFetch.fetch(cursor, derivative_sample_id)

        if rc != 1:
            raise MissingKeyException("Error updating derivative_sample {}".format(derivative_sample_id))


        return derivative_sample
