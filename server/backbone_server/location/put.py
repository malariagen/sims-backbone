from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException

from swagger_server.models.location import Location

import mysql.connector
from mysql.connector import errorcode
import psycopg2

import logging

class LocationPut():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    def __del__(self):
        if self._connection:
            self._connection.close()


    def put(self, location_id, location):

        cursor = self._connection.cursor()

        stmt = '''SELECT id, partner_name, ST_X(location) as latitude, ST_Y(location) as longitude,
        precision, curated_name, curation_method, country
                       FROM locations WHERE  id = %s'''
        cursor.execute( stmt, (location_id,))

        existing_location = None

        for (location_id, partner_name, latitude, longitude, precision, curated_name,
             curation_method, country) in cursor:
            existing_location = Location(location_id, partner_name, latitude, longitude, precision,
                                curated_name, curation_method, country)

        if not existing_location:
            cursor.close()
            raise MissingKeyException("Error updating location {}".format(location_id))

        stmt = '''SELECT id, partner_name, ST_X(location) as latitude, ST_Y(location) as longitude,
        precision, curated_name, curation_method, country
                       FROM locations WHERE  location = ST_SetSRID(ST_MakePoint(%s, %s), 4326)'''
        cursor.execute( stmt, (location.latitude, location.longitude,))

        existing_location = None

        for (location_id, partner_name, latitude, longitude, precision, curated_name,
             curation_method, country) in cursor:
            existing_location = Location(location_id, partner_name, latitude, longitude, precision,
                                curated_name, curation_method, country)

        if existing_location and str(existing_location.location_id) != location_id:
            cursor.close()
            raise DuplicateKeyException("Error inserting location {}".format(existing_location.partner_name))

        stmt = '''UPDATE locations 
                    SET partner_name = %s, location = ST_SetSRID(ST_MakePoint(%s, %s), 4326),
                    precision = %s, curated_name = %s, curation_method = %s, country = %s
                    WHERE id = %s''' 
        args = (location.partner_name, location.latitude, location.longitude,
                location.precision, location.curated_name, location.curation_method,
                location.country, location_id)
        try:
            cursor.execute(stmt, args)
        except mysql.connector.Error as err:
            cursor.close()
            if err.errno == errorcode.ER_DUP_ENTRY:
                raise DuplicateKeyException("Error updating location {}".format(location.partner_name)) from err
            else:
                self._logger.fatal(repr(error))
        except psycopg2.IntegrityError as err:
            cursor.close()
            raise DuplicateKeyException("Error updating location {}".format(location.partner_name)) from err

        rc = cursor.rowcount

        self._connection.commit()

        cursor.close()

        if rc != 1:
            raise MissingKeyException("Error updating location {}".format(location_id))

        location.location_id = location_id

        return location
