from openapi_server.models.original_sample import OriginalSample
from openapi_server.models.original_samples import OriginalSamples
from openapi_server.models.location import Location
from openapi_server.models.attr import Attr

from backbone_server.controllers.base_controller import BaseController
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.location.fetch import LocationFetch
from backbone_server.original_sample.fetch import OriginalSampleFetch

from backbone_server.original_sample.edit import OriginalSampleEdit

import logging

class OriginalSamplesGetByStudy():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, study_name, start, count, studies):

        with self._connection:
            with self._connection.cursor() as cursor:

                study_id = OriginalSampleEdit.fetch_study_id(cursor, study_name, False)

                if not study_id:
                    raise MissingKeyException("No study {}".format(study_name))

                BaseController.has_study_permission(studies, study_name,
                                                    BaseController.GET_PERMISSION)

                fields = '''SELECT original_samples.id, study_name, sampling_event_id,
                days_in_culture, partner_species'''
                query_body = ''' FROM original_samples
                LEFT JOIN sampling_events se ON se.id = original_samples.sampling_event_id
                        LEFT JOIN studies s ON s.id = original_samples.study_id
                        LEFT JOIN partner_species_identifiers psi ON psi.id = original_samples.partner_species_id
                        WHERE s.id = %s'''
                args = (study_id,)

                if studies:
                    filt = BaseController.study_filter(studies)
                    if filt:
                        query_body += ' AND ' + filt

                count_args = args
                count_query = 'SELECT COUNT(original_samples.id) ' + query_body

                query_body = query_body + ''' ORDER BY doc, id'''

                if not (start is None and count is None):
                    query_body = query_body + ' LIMIT %s OFFSET %s'
                    args = args + (count, start)

                original_samples = OriginalSamples(original_samples=[], count=0)

                stmt = fields + query_body

                cursor.execute(stmt, args)

                original_samples.original_samples, original_samples.sampling_events = OriginalSampleFetch.load_original_samples(cursor,
                                                                                                                                studies=studies,
                                                                                                                                all_attrs=True)
                if not (start is None and count is None):
                    cursor.execute(count_query, count_args)
                    original_samples.count = cursor.fetchone()[0]
                else:
                    original_samples.count = len(original_samples.original_samples)

                original_samples.attr_types = []

                col_query = '''select DISTINCT attr_type from original_samples os
                JOIN original_sample_attrs ose ON ose.original_sample_id=os.id
                JOIN attrs a ON a.id=ose.attr_id
                WHERE os.study_id = %s'''

                cursor.execute(col_query, (study_id,))
                for (attr_type,) in cursor:
                    original_samples.attr_types.append(attr_type)

        return original_samples
