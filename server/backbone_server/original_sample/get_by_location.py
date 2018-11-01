from swagger_server.models.original_sample import OriginalSample
from swagger_server.models.original_samples import OriginalSamples
from swagger_server.models.location import Location
from swagger_server.models.attr import Attr
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.location.fetch import LocationFetch
from backbone_server.original_sample.fetch import OriginalSampleFetch

from backbone_server.original_sample.edit import OriginalSampleEdit

import logging

class OriginalSamplesGetByLocation():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, location_id, start, count):

        with self._connection:
            with self._connection.cursor() as cursor:

                try:
                    location = LocationFetch.fetch(cursor, location_id)
                except MissingKeyException as mke:
                    raise mke

                fields = '''SELECT os.id, study_name, sampling_event_id,
                days_in_culture, partner_species'''
                query_body = ''' FROM original_samples os
                JOIN sampling_events se ON se.id = os.sampling_event_id
                LEFT JOIN partner_species_identifiers psi ON psi.id = os.partner_species_id
                LEFT JOIN studies s ON s.id = os.study_id
                WHERE location_id = %s OR proxy_location_id = %s'''
                args = (location_id, location_id,)

                count_args = args
                count_query = 'SELECT COUNT(os.id) ' + query_body

                query_body = query_body + ''' ORDER BY study_name, os.id'''

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

                col_query = '''select distinct attr_type from original_sample_attrs osa
                JOIN attrs a ON osa.attr_id=a.id
                JOIN original_samples os ON os.id = osa.original_sample_id
                JOIN sampling_events se ON se.id = os.sampling_event_id
                WHERE se.location_id = %s OR se.proxy_location_id = %s'''

                cursor.execute(col_query, (location_id,location_id))
                for (attr_type,) in cursor:
                    original_samples.attr_types.append(attr_type)

        return original_samples
