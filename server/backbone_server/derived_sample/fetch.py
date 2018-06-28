from swagger_server.models.attr import Attr
from swagger_server.models.taxonomy import Taxonomy
from swagger_server.models.derived_sample import DerivedSample
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.original_sample.fetch import OriginalSampleFetch

import logging

class DerivedSampleFetch():


    @staticmethod
    def fetch_attrs(cursor, derived_sample_id):

        stmt = '''SELECT attr_type, attr_value, attr_source FROM attrs
        JOIN derived_sample_attrs ON derived_sample_attrs.attr_id = attrs.id
        WHERE derived_sample_id = %s
                ORDER BY attr_type, attr_value, attr_source'''

        cursor.execute(stmt, (derived_sample_id,))

        attrs = []
        for (name, value, source) in cursor:
            ident = Attr(name, value, source)
            attrs.append(ident)

        if len(attrs) == 0:
            attrs = None

        return attrs

    @staticmethod
    def fetch(cursor, derived_sample_id, original_samples=None):

        if not derived_sample_id:
            return None

        stmt = '''SELECT derived_samples.id, original_sample_id, dna_prep
        FROM derived_samples
        WHERE derived_samples.id = %s'''
        cursor.execute( stmt, (derived_sample_id,))

        derived_sample = None

        for (derived_sample_id, original_sample_id,
             dna_prep) in cursor:
            derived_sample = DerivedSample(str(derived_sample_id),
                                            dna_prep=dna_prep)
            if original_sample_id:
                derived_sample.original_sample_id = str(original_sample_id)

        if not derived_sample:
            return derived_sample

        derived_sample.attrs = DerivedSampleFetch.fetch_attrs(cursor, derived_sample_id)


        return derived_sample

    @staticmethod
    def load_derived_samples(cursor, all_attrs=True):

        derived_samples = []
        sampling_event_list = []

        for (derived_sample_id, original_sample_id, dna_prep) in cursor:
            derived_sample = DerivedSample(str(derived_sample_id),
                                             dna_prep=dna_prep)
            if sampling_event_id:
                derived_sample.original_sample_id = str(original_sample_id)
                if not str(sampling_event_id) in sampling_event_list:
                    sampling_event_list.append(str(sampling_event_id))

            derived_samples.append(derived_sample)

        for derived_sample in derived_samples:
            derived_sample.attrs = DerivedSampleFetch.fetch_attrs(cursor,
                                                                              derived_sample.derived_sample_id)

        original_samples = {}

        for original_sample_id in original_sample_list:
                original_sample = OriginalSampleFetch.fetch(cursor, original_sample_id)
                original_samples[original_sample_id] = original_sample

        return derived_samples, sampling_events
