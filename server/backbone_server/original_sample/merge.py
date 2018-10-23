from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.incompatible_exception import IncompatibleException

from backbone_server.sampling_event.merge import SamplingEventMerge
from backbone_server.original_sample.edit import OriginalSampleEdit
from backbone_server.original_sample.put import OriginalSamplePut
from backbone_server.original_sample.delete import OriginalSampleDelete
from backbone_server.original_sample.fetch import OriginalSampleFetch
from backbone_server.location.edit import LocationEdit

from swagger_server.models.original_sample import OriginalSample

import psycopg2

import logging

class OriginalSampleMerge():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def merge(self, into, merged):

        with self._connection:
            with self._connection.cursor() as cursor:

                original_sample1 = OriginalSampleFetch.fetch(cursor, into)

                if not original_sample1:
                    raise MissingKeyException("No original_sample {}".format(into))

                if original_sample1.original_sample_id == merged:
                    return original_sample1

                original_sample2 = OriginalSampleFetch.fetch(cursor, merged)

                if not original_sample2:
                    raise MissingKeyException("No original_sample {}".format(merged))

        if original_sample1.study_name:
            if original_sample2.study_name:
                if original_sample1.study_name[:4] == '0000':
                    original_sample1.study_name = original_sample2.study_name
                elif original_sample2.study_name[:4] == '0000':
                    pass
                elif original_sample1.study_name != original_sample2.study_name:
                    msg = 'Incompatible study_name {} {}'.format(original_sample1.study_name,
                                                       original_sample2.study_name)
                    raise IncompatibleException(msg)
        else:
            original_sample1.study_name = original_sample2.study_name

        if original_sample1.days_in_culture:
            if original_sample2.days_in_culture:
                if original_sample1.days_in_culture != original_sample2.days_in_culture:
                    msg = 'Incompatible days_in_culture {} {}'.format(original_sample1.days_in_culture,
                                                       original_sample2.days_in_culture)
                    raise IncompatibleException(msg)
        else:
            original_sample1.days_in_culture = original_sample2.days_in_culture

        if original_sample1.partner_species:
            if original_sample2.partner_species:
                if original_sample1.partner_species != original_sample2.partner_species:
                    msg = 'Incompatible partner_species {} {}'.format(original_sample1.partner_species,
                                                       original_sample2.partner_species)
                    raise IncompatibleException(msg)
        else:
            original_sample1.partner_species = original_sample2.partner_species

        if original_sample2.attrs:
            for new_ident in original_sample2.attrs:
                found = False
                for existing_ident in original_sample1.attrs:
                    if new_ident == existing_ident:
                        found = True
                if not found:
                    new_ident_value = True
                    original_sample1.attrs.append(new_ident)

        if original_sample1.sampling_event_id:
            if original_sample2.sampling_event_id:
                merge = SamplingEventMerge(self._connection)
                merged_se = merge.merge(original_sample1.sampling_event_id,
                            original_sample2.sampling_event_id)
                original_sample1.sampling_event_id = merged_se.sampling_event_id
                original_sample2.sampling_event_id = None
        else:
            original_sample1.sampling_event_id = original_sample2.sampling_event_id

        with self._connection:
            with self._connection.cursor() as cursor:
                stmt = '''UPDATE derivative_samples SET original_sample_id = %s WHERE
                original_sample_id = %s'''
                cursor.execute(stmt, (original_sample1.original_sample_id,
                                      original_sample2.original_sample_id))

        delete = OriginalSampleDelete(self._connection)

        delete.delete(original_sample2.original_sample_id)

        put = OriginalSamplePut(self._connection)

        return put.put(original_sample1.original_sample_id, original_sample1)
