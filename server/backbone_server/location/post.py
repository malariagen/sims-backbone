from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from backbone_server.location.edit import LocationEdit
from backbone_server.location.fetch import LocationFetch

from openapi_server.models.location import Location

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

                LocationEdit.check_for_duplicate(cursor, location, None)

                uuid_val = uuid.uuid4()

                stmt = '''INSERT INTO locations
                            (id, location, accuracy, curated_name,
                            curation_method, country, notes, proxy_location_id)
                            VALUES (%s, ST_SetSRID(ST_MakePoint(%s, %s), 4326),
                            %s, %s, %s, %s, %s, %s)'''
                args = (uuid_val, location.latitude, location.longitude,
                        location.accuracy, location.curated_name, location.curation_method,
                        location.country, location.notes,
                        location.proxy_location_id)

                cursor.execute(stmt, args)

                LocationEdit.add_attrs(cursor, uuid_val, location)

                location = LocationFetch.fetch(cursor, uuid_val)

        return location

