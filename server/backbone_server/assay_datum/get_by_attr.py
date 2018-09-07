from swagger_server.models.assay_datum import AssayDatum
from swagger_server.models.assay_data import AssayData

from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.assay_datum.fetch import AssayDatumFetch

import logging

class AssayDatumGetByAttr():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    def get(self, attr_type, attr_value):

        with self._connection:
            with self._connection.cursor() as cursor:

                derivative_samples = {}

                stmt = '''SELECT DISTINCT assay_datum_id, derivative_sample_id, ebi_run_acc FROM assay_datum_attrs
                JOIN attrs ON attrs.id = assay_datum_attrs.attr_id
                JOIN assay_data ON assay_data.id = assay_datum_attrs.assay_datum_id
                WHERE attr_type = %s AND attr_value = %s'''
                args = (attr_type, attr_value)

                cursor.execute(stmt, args)

                assay_data = AssayData(assay_data=[], count=0)

                assay_data.assay_data, assay_data.derivative_samples = AssayDatumFetch.load_assay_data(cursor)

                assay_data.count = len(assay_data.assay_data)

                assay_data.attr_types = [attr_type]

        #partner_name has a unique key
        if assay_data.count == 0:
            raise MissingKeyException("AssayDatum not found {} {}".format(attr_type,
                                                                      attr_value))
#Allow for when partner ident is used in different studies
#        if assay_data.count > 1:
#            raise MissingKeyException("Too many assay_data not found {} {}".format(attr_type,
#                                                                      attr_value))

        return assay_data
