from openapi_server.models.assay_datum import AssayDatum
from openapi_server.models.assay_data import AssayData

from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.assay_datum.fetch import AssayDatumFetch

import logging

class AssayDatumGetByOsAttr():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    def get(self, attr_type, attr_value):

        with self._connection:
            with self._connection.cursor() as cursor:

                locations = {}

                stmt = '''SELECT DISTINCT ad.id FROM assay_data ad
                JOIN derivative_samples ds ON ds.id = ad.derivative_sample_id
                JOIN original_sample_attrs osa ON osa.original_sample_id = ds.original_sample_id
                JOIN attrs ON attrs.id = osa.attr_id
                WHERE attr_type = %s AND attr_value = %s'''
                args = (attr_type, attr_value)

                cursor.execute(stmt, args)

                assay_data = AssayData(assay_data=[], count=0)
                event_ids = []

                for assay_datum_id in cursor:
                    event_ids.append(assay_datum_id)

                for assay_datum_id in event_ids:
                    assay_datum = AssayDatumFetch.fetch(cursor, assay_datum_id, locations)
                    assay_data.assay_data.append(assay_datum)
                    assay_data.count = assay_data.count + 1

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
