import logging

from openapi_server.models.attr import Attr
from openapi_server.models.taxonomy import Taxonomy
from openapi_server.models.derivative_sample import DerivativeSample

from backbone_server.controllers.base_controller import BaseController
from backbone_server.original_sample.fetch import OriginalSampleFetch

class DerivativeSampleFetch():


    @staticmethod
    def fetch_attrs(cursor, derivative_sample_id):

        stmt = '''SELECT attr_type, attr_value, attr_source FROM attrs
        JOIN derivative_sample_attrs ON derivative_sample_attrs.attr_id = attrs.id
        WHERE derivative_sample_id = %s
                ORDER BY attr_type, attr_value, attr_source'''

        cursor.execute(stmt, (derivative_sample_id,))

        attrs = []
        for (name, value, source) in cursor:
            ident = Attr(name, value, source)
            attrs.append(ident)

        if len(attrs) == 0:
            attrs = None

        return attrs

    @staticmethod
    def fetch(cursor, derivative_sample_id, studies=None, original_samples=None):

        if not derivative_sample_id:
            return None

        stmt = '''SELECT derivative_samples.id, original_sample_id, dna_prep,
        parent_derivative_sample_id, derivative_samples.acc_date
        FROM derivative_samples'''
        if studies:
            filt = BaseController.study_filter(studies)
            if filt:
                stmt += '''LEFT JOIN original_samples ON derivative_samples.original_sample_id = original_samples.id
        LEFT JOIN studies ON original_samples.study_id = studies.id'''
                stmt += ' AND ' + filt

        stmt += ''' WHERE derivative_samples.id = %s'''

        #print(stmt % (derivative_sample_id,))
        cursor.execute(stmt, (derivative_sample_id,))

        derivative_sample = None

        for (deriv_sample_id, original_sample_id,
             dna_prep, parent_derivative_sample_id, acc_date) in cursor:
            derivative_sample = DerivativeSample(str(deriv_sample_id),
                                                 dna_prep=dna_prep,
                                                 acc_date=acc_date)
            if original_sample_id:
                derivative_sample.original_sample_id = str(original_sample_id)
            if parent_derivative_sample_id:
                derivative_sample.parent_derivative_sample_id = parent_derivative_sample_id

        if not derivative_sample:
            return derivative_sample

        derivative_sample.attrs = DerivativeSampleFetch.fetch_attrs(cursor, derivative_sample_id)


        return derivative_sample

    @staticmethod
    def load_derivative_samples(cursor, all_attrs=True):

        derivative_samples = []
        original_sample_list = []

        for (derivative_sample_id, original_sample_id, dna_prep, study_id) in cursor:
            derivative_sample = DerivativeSample(str(derivative_sample_id),
                                                 dna_prep=dna_prep)
            if original_sample_id:
                derivative_sample.original_sample_id = str(original_sample_id)
                if not str(original_sample_id) in original_sample_list:
                    original_sample_list.append(str(original_sample_id))

            derivative_samples.append(derivative_sample)

        for derivative_sample in derivative_samples:
            derivative_sample.attrs = DerivativeSampleFetch.fetch_attrs(cursor,
                                                                              derivative_sample.derivative_sample_id)

        original_samples = {}

        for original_sample_id in original_sample_list:
                original_sample = OriginalSampleFetch.fetch(cursor, original_sample_id)
                original_samples[original_sample_id] = original_sample

        return derivative_samples, original_samples
