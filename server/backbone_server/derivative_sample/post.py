from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from backbone_server.derivative_sample.edit import DerivativeSampleEdit
from backbone_server.sampling_event.edit import SamplingEventEdit
from backbone_server.derivative_sample.fetch import DerivativeSampleFetch

from swagger_server.models.derivative_sample import DerivativeSample

import psycopg2

import logging
import uuid

class DerivativeSamplePost():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def post(self, derivative_sample):

        with self._connection:
            with self._connection.cursor() as cursor:

                uuid_val = uuid.uuid4()

                stmt = '''INSERT INTO derivative_samples
                            (id, original_sample_id, dna_prep,
                            parent_derivative_sample_id)
                            VALUES (%s, %s, %s, %s)'''
                args = (uuid_val, derivative_sample.original_sample_id,
                        derivative_sample.dna_prep,
                        derivative_sample.parent_derivative_sample_id)

                try:
                    cursor.execute(stmt, args)

                    DerivativeSampleEdit.add_attrs(cursor, uuid_val, derivative_sample)

                except psycopg2.IntegrityError as err:
                    print(err.pgcode)
                    print(err.pgerror)
                    raise DuplicateKeyException("Error inserting derivative_sample {}".format(derivative_sample)) from err
                except DuplicateKeyException as err:
                    raise err

                derivative_sample = DerivativeSampleFetch.fetch(cursor, uuid_val)

        return derivative_sample

