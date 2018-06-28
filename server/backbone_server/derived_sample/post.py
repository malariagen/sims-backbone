from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from backbone_server.derived_sample.edit import DerivedSampleEdit
from backbone_server.sampling_event.edit import SamplingEventEdit
from backbone_server.derived_sample.fetch import DerivedSampleFetch

from swagger_server.models.derived_sample import DerivedSample

import psycopg2

import logging
import uuid

class DerivedSamplePost():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def post(self, derived_sample):

        with self._connection:
            with self._connection.cursor() as cursor:

                uuid_val = uuid.uuid4()

                stmt = '''INSERT INTO derived_samples 
                            (id, original_sample_id, dna_prep)
                            VALUES (%s, %s, %s)'''
                args = (uuid_val, derived_sample.original_sample_id,
                        derived_sample.dna_prep)

                try:
                    cursor.execute(stmt, args)

                    DerivedSampleEdit.add_attrs(cursor, uuid_val, derived_sample)

                except psycopg2.IntegrityError as err:
                    print(err.pgcode)
                    print(err.pgerror)
                    raise DuplicateKeyException("Error inserting derived_sample {}".format(derived_sample)) from err
                except DuplicateKeyException as err:
                    raise err

                derived_sample = DerivedSampleFetch.fetch(cursor, uuid_val)

        return derived_sample

