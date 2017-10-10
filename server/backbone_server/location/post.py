from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from swagger_server.models.location import Location

import mysql.connector
from mysql.connector import errorcode
import psycopg2

import logging
import uuid

class LocationPost():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    def __del__(self):
        if self._connection:
            self._connection.close()


    def post(self, location):

        cursor = self._connection.cursor()

        uuid_val = uuid.uuid4()

        stmt = '''INSERT INTO locations 
                    (id, partner_name, location, precision, curated_name, curation_method, country) 
                    VALUES (%s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s, %s, %s, %s)'''
        args = (uuid_val,location.partner_name, location.latitude, location.longitude,
                location.precision, location.curated_name, location.curation_method,
                location.country)
        try:
            cursor.execute(stmt, args)
        except mysql.connector.Error as err:
            cursor.close()
            if err.errno == errorcode.ER_DUP_ENTRY:
                raise DuplicateKeyException("Error inserting location {}".format(location.partner_name)) from err
            else:
                self._logger.fatal(repr(error))
        except psycopg2.IntegrityError as err:
            cursor.close()
            raise DuplicateKeyException("Error inserting location {}".format(location.partner_name)) from err
        self._connection.commit()

        cursor.close()

        location.location_id = uuid_val
        return location
