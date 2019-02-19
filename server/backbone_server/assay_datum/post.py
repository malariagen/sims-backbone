from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from backbone_server.assay_datum.edit import AssayDatumEdit
from backbone_server.assay_datum.fetch import AssayDatumFetch

from openapi_server.models.assay_datum import AssayDatum

import psycopg2

import logging
import uuid

class AssayDatumPost():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def post(self, assay_datum):

        with self._connection:
            with self._connection.cursor() as cursor:

                uuid_val = uuid.uuid4()

                stmt = '''INSERT INTO assay_data
                            (id, derivative_sample_id, ebi_run_acc)
                            VALUES (%s, %s, %s)'''
                args = (uuid_val, assay_datum.derivative_sample_id,
                        assay_datum.ebi_run_acc)

                try:
                    cursor.execute(stmt, args)

                    AssayDatumEdit.add_attrs(cursor, uuid_val, assay_datum)

                except psycopg2.IntegrityError as err:
                    raise DuplicateKeyException("Error inserting assay_datum {}".format(assay_datum)) from err
                except DuplicateKeyException as err:
                    raise err

                assay_datum = AssayDatumFetch.fetch(cursor, uuid_val)

        return assay_datum

