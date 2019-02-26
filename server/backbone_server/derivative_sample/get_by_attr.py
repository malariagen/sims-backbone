from openapi_server.models.derivative_sample import DerivativeSample
from openapi_server.models.derivative_samples import DerivativeSamples

from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.derivative_sample.fetch import DerivativeSampleFetch

import logging

class DerivativeSampleGetByAttr():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    def get(self, attr_type, attr_value):

        with self._connection:
            with self._connection.cursor() as cursor:

                sampling_events = {}

                stmt = '''SELECT DISTINCT derivative_sample_id FROM derivative_sample_attrs
                JOIN attrs ON attrs.id = derivative_sample_attrs.attr_id
                WHERE attr_type = %s AND attr_value = %s'''
                args = (attr_type, attr_value)

                cursor.execute(stmt, args)

                derivative_samples = DerivativeSamples(derivative_samples=[], count=0)
                event_ids = []

                for derivative_sample_id in cursor:
                    event_ids.append(derivative_sample_id)

                for derivative_sample_id in event_ids:
                    derivative_sample = DerivativeSampleFetch.fetch(cursor, derivative_sample_id,
                                                                sampling_events)
                    derivative_samples.derivative_samples.append(derivative_sample)
                    derivative_samples.count = derivative_samples.count + 1

                derivative_samples.sampling_events = sampling_events

                derivative_samples.attr_types = [attr_type]

#Allow for when partner ident is used in different studies
#        if derivative_samples.count > 1:
#            raise MissingKeyException("Too many derivative_samples not found {} {}".format(attr_type,
#                                                                      attr_value))

        return derivative_samples
