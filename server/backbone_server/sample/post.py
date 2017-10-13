from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from swagger_server.models.sample import Sample

import mysql.connector
from mysql.connector import errorcode
import psycopg2

import logging
import uuid

class SamplePost():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    def __del__(self):
        if self._connection:
            self._connection.close()


    def post(self, sample):

        cursor = self._connection.cursor()

        uuid_val = uuid.uuid4()

        stmt = '''INSERT INTO samples 
                    (id, study_id, doc, location_id, proxy_location_id) 
                    VALUES (%s, %s, %s, %s, %s)'''
        args = (uuid_val,sample.study_id, sample.doc, sample.location_id, sample.proxy_location_id)

        try:
            cursor.execute(stmt, args)

            if sample.identifiers:
                for ident in sample.identifiers:
                    stmt = '''INSERT INTO identifiers (sample_id, identifier_type, identifier_value)
                    VALUES (%s, %s, %s)'''
                    cursor.execute(stmt, (uuid_val, ident.identifier_type, ident.identifier_value))

        except mysql.connector.Error as err:
            cursor.close()
            if err.errno == errorcode.ER_DUP_ENTRY:
                raise DuplicateKeyException("Error inserting sample {}".format(sample)) from err
            else:
                self._logger.fatal(repr(error))
        except psycopg2.IntegrityError as err:
            cursor.close()
            raise DuplicateKeyException("Error inserting sample {}".format(sample)) from err

        self._connection.commit()

        cursor.close()

        sample.sample_id = uuid_val
        return sample

