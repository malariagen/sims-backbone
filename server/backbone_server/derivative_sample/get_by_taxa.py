import logging

from openapi_server.models.derivative_sample import DerivativeSample
from openapi_server.models.derivative_samples import DerivativeSamples

from backbone_server.controllers.base_controller import BaseController
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.derivative_sample.fetch import DerivativeSampleFetch

class DerivativeSamplesGetByTaxa():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    def get(self, taxa_id, studies, start, count):

        with self._connection:
            with self._connection.cursor() as cursor:

                filt = None

                stmt = '''SELECT id FROM taxonomies WHERE id = %s'''
                cursor.execute(stmt, (taxa_id, ))
                vtaxa_id = None
                for tid in cursor:
                    vtaxa_id = tid

                if not vtaxa_id:
                    raise MissingKeyException("No taxa {}".format(taxa_id))

                fields = '''SELECT DISTINCT ds.id, original_sample_id, dna_prep, os.study_id '''

                query_body = '''FROM derivative_samples ds
                JOIN original_samples os ON os.id = ds.original_sample_id
                LEFT JOIN studies s ON s.id = os.study_id
                JOIN taxonomy_identifiers ti ON ti.partner_species_id = os.partner_species_id
                WHERE ti.taxonomy_id = %s'''
                args = (taxa_id, )

                if studies:
                    filt = BaseController.study_filter(studies)
                    if filt:
                        query_body += ' AND ' + filt

                count_args = args
                count_query = 'SELECT COUNT(ds.id) ' + query_body

                query_body = query_body + ''' ORDER BY os.study_id, id'''

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
                LEFT JOIN taxonomy_identifiers ti ON ti.partner_species_id = os.partner_species_id
                WHERE ti.taxonomy_id = %s'''

                if filt:
                    query_body += ' AND ' + filt

                cursor.execute(col_query, (taxa_id,))
                for (attr_type,) in cursor:
                    derivative_samples.attr_types.append(attr_type)


        return derivative_samples
