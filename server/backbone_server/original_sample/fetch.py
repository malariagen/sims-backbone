from swagger_server.models.attr import Attr
from swagger_server.models.taxonomy import Taxonomy
from swagger_server.models.original_sample import OriginalSample
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.sampling_event.fetch import SamplingEventFetch

import logging

class OriginalSampleFetch():


    @staticmethod
    def fetch_attrs(cursor, original_sample_id):

        stmt = '''SELECT attr_type, attr_value, attr_source FROM attrs
        JOIN original_sample_attrs ON original_sample_attrs.attr_id = attrs.id
        WHERE original_sample_id = %s
                ORDER BY attr_type, attr_value, attr_source'''

        cursor.execute(stmt, (original_sample_id,))

        attrs = []
        for (name, value, source) in cursor:
            ident = Attr(name, value, source)
            attrs.append(ident)

        if len(attrs) == 0:
            attrs = None

        return attrs

    @staticmethod
    def fetch(cursor, original_sample_id, sampling_events=None):

        if not original_sample_id:
            return None

        stmt = '''SELECT original_samples.id, studies.study_name AS study_id, days_in_culture
        FROM original_samples
        LEFT JOIN studies ON studies.id = original_samples.study_id
        WHERE original_samples.id = %s'''
        cursor.execute( stmt, (original_sample_id,))

        original_sample = None

        for (original_sample_id, study_id, days_in_culture) in cursor:
            original_sample = OriginalSample(str(original_sample_id), study_name = study_id)

        if not original_sample:
            return original_sample

        original_sample.attrs = OriginalSampleFetch.fetch_attrs(cursor, original_sample_id)


        return original_sample

    @staticmethod
    def load_original_samples(cursor, all_attrs=True):

        original_samples = []
        sampling_event_list = []

        for (original_sample_id, study_id, sampling_event_id, days_in_culture) in cursor:
            original_sample = OriginalSample(str(original_sample_id), study_name=study_id)
            if sampling_event_id:
                original_sample.sampling_event_id = str(sampling_event_id)
                if not str(sampling_event_id) in sampling_event_list:
                    sampling_event_list.append(str(sampling_event_id))

            original_samples.append(original_sample)

        for original_sample in original_samples:
            original_sample.attrs = OriginalSampleFetch.fetch_attrs(cursor,
                                                                              original_sample.original_sample_id)

        sampling_events = {}

        for sampling_event_id in sampling_event_list:
                sampling_event = SamplingEventFetch.fetch(cursor, sampling_event_id)
                sampling_events[sampling_event_id] = sampling_event

        return original_samples, sampling_events
