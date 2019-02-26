from openapi_server.models.derivative_sample import DerivativeSample
from openapi_server.models.derivative_samples import DerivativeSamples

from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.derivative_sample.fetch import DerivativeSampleFetch
from backbone_server.original_sample.edit import OriginalSampleEdit

import logging

class DerivativeSamplesGetByStudy():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    def get(self, study_name, start, count):

        with self._connection:
            with self._connection.cursor() as cursor:

                study_id = OriginalSampleEdit.fetch_study_id(cursor, study_name, False)

                if not study_id:
                    raise MissingKeyException("No study {}".format(study_name))

                fields = '''SELECT DISTINCT ds.id, original_sample_id, dna_prep, s.study_name '''

                query_body = '''FROM derivative_samples ds
                JOIN original_samples os ON os.id = ds.original_sample_id
                LEFT JOIN studies s ON s.id = os.study_id
                WHERE os.study_id = %s'''
                args = (study_id, )

                count_args = args
                count_query = 'SELECT COUNT(ds.id) ' + query_body

                query_body = query_body + ''' ORDER BY s.study_name, id'''

                if not (start is None and count is None):
                    query_body = query_body + ' LIMIT %s OFFSET %s'
                    args = args + (count, start)

                stmt = fields + query_body

                cursor.execute(stmt, args)

                derivative_samples = DerivativeSamples(derivative_samples=[], count=0)

                cursor.execute(stmt, args)

                derivative_samples.derivative_samples, derivative_samples.original_samples = DerivativeSampleFetch.load_derivative_samples(cursor, True)

                derivative_samples.count = len(derivative_samples.derivative_samples)

                if not (start is None and count is None):
                    cursor.execute(count_query, count_args)
                    derivative_samples.count = cursor.fetchone()[0]

                derivative_samples.attr_types = []

                col_query = '''select distinct attr_type from derivative_sample_attrs dsa
                JOIN attrs a ON a.id=dsa.attr_id
                JOIN derivative_samples ds ON ds.id = dsa.derivative_sample_id
                JOIN original_samples os ON os.id = ds.original_sample_id
                WHERE os.study_id = %s'''

                cursor.execute(col_query, (study_id,))
                for (attr_type,) in cursor:
                    derivative_samples.attr_types.append(attr_type)


        return derivative_samples
