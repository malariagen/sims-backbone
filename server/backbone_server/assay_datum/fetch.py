from swagger_server.models.attr import Attr
from swagger_server.models.assay_datum import AssayDatum
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.derived_sample.fetch import DerivedSampleFetch

import logging

class AssayDatumFetch():


    @staticmethod
    def fetch_attrs(cursor, assay_datum_id):

        stmt = '''SELECT attr_type, attr_value, attr_source FROM attrs
        JOIN assay_datum_attrs ON assay_datum_attrs.attr_id = attrs.id
        WHERE assay_datum_id = %s
                ORDER BY attr_type, attr_value, attr_source'''

        cursor.execute(stmt, (assay_datum_id,))

        attrs = []
        for (name, value, source) in cursor:
            ident = Attr(name, value, source)
            attrs.append(ident)

        if len(attrs) == 0:
            attrs = None

        return attrs

    @staticmethod
    def fetch(cursor, assay_datum_id, derived_samples=None):

        if not assay_datum_id:
            return None

        stmt = '''SELECT assay_data.id, derived_sample_id, ebi_run_acc
        FROM assay_data
        WHERE assay_data.id = %s'''
        cursor.execute( stmt, (assay_datum_id,))

        assay_datum = None

        for (assay_datum_id, derived_sample_id,
             ebi_run_acc) in cursor:
            assay_datum = AssayDatum(str(assay_datum_id),
                                            ebi_run_acc=ebi_run_acc)
            if derived_sample_id:
                assay_datum.derived_sample_id = str(derived_sample_id)

        if not assay_datum:
            return assay_datum

        assay_datum.attrs = AssayDatumFetch.fetch_attrs(cursor, assay_datum_id)


        return assay_datum

    @staticmethod
    def load_assay_data(cursor, all_attrs=True):

        assay_data = []
        derived_sample_list = []

        for (assay_datum_id, derived_sample_id, ebi_run_acc) in cursor:
            assay_datum = AssayDatum(str(assay_datum_id),
                                             ebi_run_acc=ebi_run_acc)
            if derived_sample_id:
                assay_datum.derived_sample_id = str(derived_sample_id)
                if not str(derived_sample_id) in derived_sample_list:
                    derived_sample_list.append(str(derived_sample_id))

            assay_data.append(assay_datum)

        for assay_datum in assay_data:
            assay_datum.attrs = AssayDatumFetch.fetch_attrs(cursor,
                                                                              assay_datum.assay_datum_id)

        derived_samples = {}

        for derived_sample_id in derived_sample_list:
                derived_sample = DerivedSampleFetch.fetch(cursor, derived_sample_id)
                derived_samples[derived_sample_id] = derived_sample

        return assay_data, derived_samples
