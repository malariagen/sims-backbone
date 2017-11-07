from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from backbone_server.sampling_event.edit import SamplingEventEdit

from swagger_server.models.sampling_event import SamplingEvent

import mysql.connector
from mysql.connector import errorcode
import psycopg2

import logging
import uuid

class SamplingEventPost():

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

            SamplingEventEdit.add_identifiers(cursor, uuid_val, sample)

        except mysql.connector.Error as err:
            cursor.close()
            if err.errno == errorcode.ER_DUP_ENTRY:
                raise DuplicateKeyException("Error inserting sample {}".format(sample)) from err
            else:
                self._logger.fatal(repr(error))
        except psycopg2.IntegrityError as err:
            cursor.close()
            raise DuplicateKeyException("Error inserting sample {}".format(sample)) from err
        except DuplicateKeyException as err:
            cursor.close()
            raise err

        self._connection.commit()

        cursor.close()

        sample.sampling_event_id = uuid_val
        return sample

