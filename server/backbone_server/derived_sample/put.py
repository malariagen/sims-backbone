from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.derived_sample.edit import DerivedSampleEdit
from backbone_server.derived_sample.fetch import DerivedSampleFetch

from swagger_server.models.derived_sample import DerivedSample

import psycopg2

import logging

class DerivedSamplePut():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def put(self, derived_sample_id, derived_sample):

        with self._connection:
            with self._connection.cursor() as cursor:

                stmt = '''SELECT id FROM derived_samples WHERE id = %s'''
                cursor.execute( stmt, (derived_sample_id,))

                existing_derived_sample = None

                for (derived_sample_id,) in cursor:
                    existing_derived_sample = DerivedSample(derived_sample_id)

                if not existing_derived_sample:
                    raise MissingKeyException("Could not find derived_sample to update {}".format(derived_sample_id))

                stmt = '''UPDATE derived_samples 
                            SET original_sample_id = %s,
                            dna_prep = %s
                            WHERE id = %s'''
                args = (derived_sample.original_sample_id,
                        derived_sample.dna_prep,
                        derived_sample_id)

                try:
                    cursor.execute(stmt, args)
                    rc = cursor.rowcount

                    cursor.execute('DELETE FROM derived_sample_attrs WHERE derived_sample_id = %s',
                                   (derived_sample_id,))

                    DerivedSampleEdit.add_attrs(cursor, derived_sample_id, derived_sample)

                except psycopg2.IntegrityError as err:
                    raise DuplicateKeyException("Error updating derived_sample {}".format(derived_sample)) from err
                except DuplicateKeyException as err:
                    raise err

                derived_sample = DerivedSampleFetch.fetch(cursor, derived_sample_id)

        if rc != 1:
            raise MissingKeyException("Error updating derived_sample {}".format(derived_sample_id))


        return derived_sample
