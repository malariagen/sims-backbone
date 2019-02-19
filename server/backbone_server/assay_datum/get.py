from openapi_server.models.assay_datum import AssayDatum
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.assay_datum.fetch import AssayDatumFetch

import logging

class AssayDatumGetById():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, assay_datum_id):

        with self._connection:
            with self._connection.cursor() as cursor:

                assay_datum = AssayDatumFetch.fetch(cursor, assay_datum_id)

        if not assay_datum:
            raise MissingKeyException("No assay_datum {}".format(assay_datum_id))

        return assay_datum
