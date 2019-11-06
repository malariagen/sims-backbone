from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.assay_datum.edit import AssayDatumEdit
from backbone_server.assay_datum.fetch import AssayDatumFetch

from openapi_server.models.assay_datum import AssayDatum

import psycopg2

import logging

class AssayDatumPut():

    def __init__(self, conn, cursor=None):
        self._logger = logging.getLogger(__name__)
        self._connection = conn
        self._cursor = cursor


    def put(self, assay_datum_id, assay_datum):

        with self._connection:
            with self._connection.cursor() as cursor:

                return self.run_command(cursor, assay_datum_id, assay_datum)

    def run_command(self, cursor, assay_datum_id, assay_datum):

        stmt = '''SELECT id FROM assay_data WHERE id = %s'''
        cursor.execute( stmt, (assay_datum_id,))

        existing_assay_datum = None

        for (assay_datum_id,) in cursor:
            existing_assay_datum = AssayDatum(assay_datum_id)

        if not existing_assay_datum:
            raise MissingKeyException("Could not find assay_datum to update {}".format(assay_datum_id))

        stmt = '''UPDATE assay_data
                    SET derivative_sample_id = %s,
                    ebi_run_acc = %s,
                    acc_date = %s
                    WHERE id = %s'''
        args = (assay_datum.derivative_sample_id,
                assay_datum.ebi_run_acc,
                assay_datum.acc_date,
                assay_datum_id)

        try:
            cursor.execute(stmt, args)
            rc = cursor.rowcount

            cursor.execute('DELETE FROM assay_datum_attrs WHERE assay_datum_id = %s',
                           (assay_datum_id,))

            AssayDatumEdit.add_attrs(cursor, assay_datum_id, assay_datum)

        except psycopg2.IntegrityError as err:
            raise DuplicateKeyException("Error updating assay_datum {}".format(assay_datum)) from err
        except DuplicateKeyException as err:
            raise err

        assay_datum = AssayDatumFetch.fetch(cursor, assay_datum_id)

        if rc != 1:
            raise MissingKeyException("Error updating assay_datum {}".format(assay_datum_id))


        return assay_datum
