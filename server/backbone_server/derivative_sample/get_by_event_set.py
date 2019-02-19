from openapi_server.models.derivative_sample import DerivativeSample
from openapi_server.models.derivative_samples import DerivativeSamples

from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.derivative_sample.fetch import DerivativeSampleFetch

import logging


class DerivativeSamplesGetByEventSet():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    def get(self, event_set_name, start, count):

        with self._connection:
            with self._connection.cursor() as cursor:

                stmt = '''SELECT id FROM event_sets WHERE event_set_name = %s'''
                cursor.execute(stmt, (event_set_name, ))
                event_set_id = None
                for tid in cursor:
                    event_set_id = tid

                if not event_set_id:
                    raise MissingKeyException(
                        "No event_set_name {}".format(event_set_name))

                fields = '''SELECT DISTINCT ds.id, original_sample_id, dna_prep, os.study_id '''

                query_body = '''FROM derivative_samples ds
                JOIN original_samples os ON os.id = ds.original_sample_id
                JOIN event_set_members esm ON esm.sampling_event_id = os.sampling_event_id
                LEFT JOIN studies s ON s.id = os.study_id
                WHERE esm.event_set_id = %s'''
                args = (event_set_id, )

                count_args = args
                count_query = 'SELECT COUNT(ds.id) ' + query_body

                query_body = query_body + ''' ORDER BY os.study_id, id'''

                if not (start is None and count is None):
                    query_body = query_body + ' LIMIT %s OFFSET %s'
                    args = args + (count, start)

                stmt = fields + query_body

                cursor.execute(stmt, args)

                derivative_samples = DerivativeSamples(
                    derivative_samples=[], count=0)

                cursor.execute(stmt, args)

                deriv_samps, orig_samps = DerivativeSampleFetch.load_derivative_samples(cursor, True)

                derivative_samples.derivative_samples = deriv_samps
                derivative_samples.original_samples = orig_samps

                derivative_samples.count = len(
                    derivative_samples.derivative_samples)

                if not (start is None and count is None):
                    cursor.execute(count_query, count_args)
                    derivative_samples.count = cursor.fetchone()[0]

                derivative_samples.attr_types = []

                col_query = '''select distinct attr_type from derivative_sample_attrs dsa
                JOIN attrs a ON a.id=dsa.attr_id
                JOIN derivative_samples ds ON ds.id = dsa.derivative_sample_id
                JOIN original_samples os ON os.id = ds.original_sample_id
                JOIN event_set_members esm ON esm.sampling_event_id = os.sampling_event_id
                WHERE esm.event_set_id = %s'''

                cursor.execute(col_query, (event_set_id,))
                for (attr_type,) in cursor:
                    derivative_samples.attr_types.append(attr_type)

        if derivative_samples.count == 0:
            msg = "DerivativeSamples not found for event set {}".format(
                event_set_id)
            raise MissingKeyException(msg)

        return derivative_samples
