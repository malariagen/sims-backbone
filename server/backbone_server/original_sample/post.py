from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from backbone_server.original_sample.edit import OriginalSampleEdit
from backbone_server.sampling_event.edit import SamplingEventEdit
from backbone_server.original_sample.fetch import OriginalSampleFetch

from openapi_server.models.original_sample import OriginalSample

import psycopg2

import logging
import uuid


class OriginalSamplePost():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    def post(self, original_sample, uuid_val=None):

        with self._connection:
            with self._connection.cursor() as cursor:

                if not uuid_val:
                    uuid_val = uuid.uuid4()

                study_id = SamplingEventEdit.fetch_study_id(
                    cursor, original_sample.study_name, True)

                partner_species = OriginalSampleEdit.fetch_partner_species(
                    cursor, original_sample, study_id)
                stmt = '''INSERT INTO original_samples
                            (id, study_id, sampling_event_id, days_in_culture, partner_species_id)
                            VALUES (%s, %s, %s, %s, %s)'''
                args = (uuid_val, study_id, original_sample.sampling_event_id,
                        original_sample.days_in_culture, partner_species)

                cursor.execute(stmt, args)

                OriginalSampleEdit.add_attrs(cursor, uuid_val, original_sample)

                original_sample = OriginalSampleFetch.fetch(cursor, uuid_val)

        return original_sample
