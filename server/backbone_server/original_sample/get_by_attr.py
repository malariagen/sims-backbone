from openapi_server.models.original_sample import OriginalSample
from openapi_server.models.original_samples import OriginalSamples

from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.original_sample.fetch import OriginalSampleFetch

import logging

class OriginalSampleGetByAttr():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    def get(self, attr_type, attr_value, study_name):

        with self._connection:
            with self._connection.cursor() as cursor:

                sampling_events = {}

                stmt = '''SELECT DISTINCT original_sample_id FROM original_sample_attrs
                JOIN attrs ON attrs.id = original_sample_attrs.attr_id
                WHERE attr_type = %s AND attr_value = %s'''
                args = (attr_type, attr_value)

                if study_name:
                    stmt = '''SELECT DISTINCT original_sample_id FROM original_sample_attrs
                    JOIN attrs ON attrs.id = original_sample_attrs.attr_id
                    LEFT JOIN original_samples ON original_sample_attrs.original_sample_id=original_samples.id
                    LEFT JOIN studies ON original_samples.study_id=studies.id
                WHERE attr_type = %s AND attr_value = %s AND study_code = %s'''
                    args = args + (study_name[:4],)

                cursor.execute(stmt, args)

                original_samples = OriginalSamples(original_samples=[], count=0)
                event_ids = []

                for original_sample_id in cursor:
                    event_ids.append(original_sample_id)

                for original_sample_id in event_ids:
                    original_sample = OriginalSampleFetch.fetch(cursor, original_sample_id,
                                                                sampling_events)
                    original_samples.original_samples.append(original_sample)
                    original_samples.count = original_samples.count + 1

                original_samples.sampling_events = sampling_events

                original_samples.attr_types = [attr_type]

        #partner_name has a unique key
        if original_samples.count == 0:
            raise MissingKeyException("OriginalSample not found {} {}".format(attr_type,
                                                                      attr_value))
#Allow for when partner ident is used in different studies
#        if original_samples.count > 1:
#            raise MissingKeyException("Too many original_samples not found {} {}".format(attr_type,
#                                                                      attr_value))

        return original_samples
