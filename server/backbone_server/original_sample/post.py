from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from backbone_server.original_sample.edit import OriginalSampleEdit
from backbone_server.sampling_event.edit import SamplingEventEdit
from backbone_server.original_sample.fetch import OriginalSampleFetch

from swagger_server.models.original_sample import OriginalSample

import psycopg2

import logging
import uuid

class OriginalSamplePost():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def post(self, original_sample):

        with self._connection:
            with self._connection.cursor() as cursor:

                uuid_val = uuid.uuid4()

                study_id = SamplingEventEdit.fetch_study_id(cursor, original_sample.study_name, True)

                stmt = '''INSERT INTO original_samples 
                            (id, study_id, sampling_event_id) 
                            VALUES (%s, %s, %s)'''
                args = (uuid_val,study_id, original_sample.sampling_event_id)

                try:
                    cursor.execute(stmt, args)

                    OriginalSampleEdit.add_attrs(cursor, uuid_val, original_sample)

                except psycopg2.IntegrityError as err:
                    print(err.pgcode)
                    print(err.pgerror)
                    raise DuplicateKeyException("Error inserting original_sample {}".format(original_sample)) from err
                except DuplicateKeyException as err:
                    raise err

                original_sample = OriginalSampleFetch.fetch(cursor, uuid_val)

        return original_sample

