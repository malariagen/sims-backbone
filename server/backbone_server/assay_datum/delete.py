from openapi_server.models.assay_datum import AssayDatum

from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

class AssayDatumDelete():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def delete(self, assay_datum_id):

        with self._connection:
            with self._connection.cursor() as cursor:

                return self.run_command(cursor, assay_datum_id)

    def run_command(self, cursor, assay_datum_id):

        stmt = '''DELETE FROM assay_datum_attrs WHERE assay_datum_id = %s'''

        cursor.execute( stmt, (assay_datum_id,))

        stmt = '''DELETE FROM assay_data WHERE id = %s'''

        cursor.execute( stmt, (assay_datum_id,))

        rc = cursor.rowcount


        if rc != 1:
            raise MissingKeyException("Error deleting assay_datum {}".format(assay_datum_id))


