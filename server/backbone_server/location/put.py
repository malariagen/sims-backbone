from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.location.edit import LocationEdit
from backbone_server.location.fetch import LocationFetch

from openapi_server.models.location import Location
from openapi_server.models.attr import Attr

import psycopg2

import logging

class LocationPut(LocationEdit):

    def __init__(self, conn, cursor=None):
        self._logger = logging.getLogger(__name__)
        self._connection = conn
        self._cursor = cursor


    def put(self, location_id, location):

        with self._connection:
            with self._connection.cursor() as cursor:
                return self.run_command(cursor, location_id, location)

    def run_command(self, cursor, location_id, location):

        stmt = '''SELECT id, ST_X(location) as latitude, ST_Y(location) as longitude,
        accuracy, curated_name, curation_method, country
                       FROM locations WHERE  id = %s'''
        cursor.execute( stmt, (location_id,))

        existing_location = None

        for (location_id, latitude, longitude, accuracy, curated_name,
             curation_method, country) in cursor:
            existing_location = Location(location_id, latitude, longitude, accuracy,
                                curated_name, curation_method, country)

        if not existing_location:
            raise MissingKeyException("Error updating location {}".format(location_id))

        LocationEdit.check_for_duplicate(cursor, location, location_id)

        stmt = '''UPDATE locations
                    SET location = ST_SetSRID(ST_MakePoint(%s, %s), 4326),
                    accuracy = %s, curated_name = %s, curation_method = %s, country = %s,
                    notes = %s
                    WHERE id = %s'''
        args = (location.latitude, location.longitude,
                location.accuracy, location.curated_name, location.curation_method,
                location.country, location.notes, location_id)
        try:
            cursor.execute(stmt, args)
            rc = cursor.rowcount

            cursor.execute('''DELETE FROM location_attrs WHERE location_id = %s''',
                           (location_id,))

            LocationEdit.add_attrs(cursor, location_id, location)

        except psycopg2.IntegrityError as err:
            raise DuplicateKeyException("Error updating location {}".format(location)) from err

        location = LocationFetch.fetch(cursor, location_id)


        if rc != 1:
            raise MissingKeyException("Error updating location {}".format(location_id))
        #
        return location
