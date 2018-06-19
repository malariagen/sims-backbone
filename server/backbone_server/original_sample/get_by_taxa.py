from swagger_server.models.original_sample import OriginalSample
from swagger_server.models.original_samples import OriginalSamples
from swagger_server.models.location import Location
from swagger_server.models.attr import Attr
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.location.fetch import LocationFetch
from backbone_server.original_sample.fetch import OriginalSampleFetch

from backbone_server.original_sample.edit import OriginalSampleEdit

import logging

class OriginalSamplesGetByTaxa():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, taxa_id, start, count):
        with self._connection:
            with self._connection.cursor() as cursor:

                stmt = '''SELECT id FROM taxonomies WHERE id = %s'''
                cursor.execute(stmt, (taxa_id, ))
                vtaxa_id = None
                for tid in cursor:
                    vtaxa_id = tid

                if not vtaxa_id:
                    raise MissingKeyException("No taxa {}".format(taxa_id))

                fields = '''SELECT id, study_name, sampling_event_id, days_in_culture '''
                query_body = ''' FROM original_samples os
                JOIN sampling_events se ON se.id = os.sampling_event_id
                LEFT JOIN studies s ON s.id = os.study_id
                        JOIN taxonomy_identifiers ti ON ti.partner_species_id = se.partner_species_id
                        WHERE ti.taxonomy_id = %s'''
                args = (taxa_id,)

                count_args = args
                count_query = 'SELECT COUNT(id) ' + query_body

                query_body = query_body + ''' ORDER BY doc, study_id, id'''

                if not (start is None and count is None):
                    query_body = query_body + ' LIMIT %s OFFSET %s'
                    args = args + (count, start)

                original_samples = OriginalSamples(original_samples=[], count=0)

                stmt = fields + query_body

                cursor.execute(stmt, args)

                original_samples.original_samples, original_samples.locations = OriginalSampleFetch.load_original_samples(cursor, True)

                if not (start is None and count is None):
                    cursor.execute(count_query, count_args)
                    original_samples.count = cursor.fetchone()[0]
                else:
                    original_samples.count = len(original_samples.original_samples)

                original_samples.attr_types = []

                col_query = '''select distinct attr_type from original_sample_attrs sea
                        JOIN attrs a ON a.id=sea.attr_id
                        JOIN original_samples se ON se.id = sea.original_sample_id
                        LEFT JOIN taxonomy_identifiers ti ON ti.partner_species_id = se.partner_species_id
                        WHERE ti.taxonomy_id = %s'''

                cursor.execute(col_query, (taxa_id,))
                for (attr_type,) in cursor:
                    original_samples.attr_types.append(attr_type)


        return original_samples
