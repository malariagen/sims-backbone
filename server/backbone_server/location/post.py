from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from backbone_server.location.edit import LocationEdit
from backbone_server.location.fetch import LocationFetch

from swagger_server.models.location import Location
from swagger_server.models.identifier import Identifier

import mysql.connector
from mysql.connector import errorcode
import psycopg2

import logging
import uuid

class LocationPost(LocationEdit):

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def post(self, location):

        with self._connection:
            with self._connection.cursor() as cursor:

                stmt = '''SELECT id, ST_X(location) as latitude, ST_Y(location) as longitude,
                accuracy, curated_name, curation_method, country
                               FROM locations WHERE  location = ST_SetSRID(ST_MakePoint(%s, %s), 4326)'''
                cursor.execute( stmt, (location.latitude, location.longitude,))

                existing_location = None

                for (location_id, latitude, longitude, accuracy, curated_name,
                     curation_method, country) in cursor:
                    existing_location = Location(location_id, latitude, longitude, accuracy,
                                        curated_name, curation_method, country)

                if existing_location:
                    raise DuplicateKeyException("Error inserting location {}".format(existing_location))

                uuid_val = uuid.uuid4()

                stmt = '''INSERT INTO locations 
                            (id, location, accuracy, curated_name, curation_method, country, notes) 
                            VALUES (%s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s, %s, %s, %s, %s)'''
                args = (uuid_val, location.latitude, location.longitude,
                        location.accuracy, location.curated_name, location.curation_method,
                        location.country, location.notes)
                try:
                    cursor.execute(stmt, args)

                    LocationEdit.add_identifiers(cursor, uuid_val, location)

                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_DUP_ENTRY:
                        raise DuplicateKeyException("Error inserting location {}".format(location)) from err
                    else:
                        self._logger.fatal(repr(error))
                except psycopg2.IntegrityError as err:
                    self._logger.error(repr(err))
                    raise DuplicateKeyException("Error inserting location {}".format(location)) from err

                location = LocationFetch.fetch(cursor, uuid_val)

        return location

