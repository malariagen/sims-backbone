from swagger_server.models.original_sample import OriginalSample
from swagger_server.models.original_samples import OriginalSamples
from swagger_server.models.location import Location
from swagger_server.models.attr import Attr
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.original_sample.fetch import OriginalSampleFetch

from backbone_server.original_sample.edit import OriginalSampleEdit

import logging

class OriginalSamplesGetByEventSet():

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
                    raise MissingKeyException("No event_set_name {}".format(event_set_name))

                fields = '''SELECT os.id, study_name, os.sampling_event_id,
                days_in_culture, partner_species '''
                query_body = ''' FROM original_samples os
                JOIN sampling_events se ON se.id = os.sampling_event_id
                LEFT JOIN partner_species_identifiers psi ON psi.id = os.partner_species_id
                JOIN event_set_members esm ON esm.sampling_event_id = se.id
                LEFT JOIN studies s ON s.id = os.study_id
                WHERE esm.event_set_id = %s'''
                args = (event_set_id,)

                count_args = args
                count_query = 'SELECT COUNT(os.id) ' + query_body

                query_body = query_body + ''' ORDER BY doc, os.study_id, id'''

                if not (start is None and count is None):
                    query_body = query_body + ' LIMIT %s OFFSET %s'
                    args = args + (count, start)

                original_samples = OriginalSamples(original_samples=[], count=0)

                stmt = fields + query_body

                cursor.execute(stmt, args)

                original_samples.original_samples, original_samples.sampling_events = OriginalSampleFetch.load_original_samples(cursor, True)

                if not (start is None and count is None):
                    cursor.execute(count_query, count_args)
                    original_samples.count = cursor.fetchone()[0]
                else:
                    original_samples.count = len(original_samples.original_samples)

                original_samples.attr_types = []

                col_query = '''select distinct attr_type from original_sample_attrs sea
                JOIN attrs a ON a.id=sea.attr_id
                JOIN original_samples os ON os.id = sea.original_sample_id
                JOIN sampling_events se ON se.id = os.sampling_event_id
                JOIN event_set_members esm ON esm.sampling_event_id = se.id
                WHERE esm.event_set_id = %s'''

                cursor.execute(col_query, (event_set_id,))
                for (attr_type,) in cursor:
                    original_samples.attr_types.append(attr_type)


        return original_samples
