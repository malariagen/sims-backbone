from swagger_server.models.location import Location
from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

class LocationGetById():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def __del__(self):
        if self._connection:
            self._connection.close()

    def get(self, location_id):

        cursor = self._connection.cursor()

        stmt = '''SELECT id, partner_name, ST_X(location) as latitude, ST_Y(location) as longitude,
        precision, curated_name, curation_method, country
                       FROM locations WHERE id = %s'''
        cursor.execute( stmt, (location_id,))

        location = None

        for (location_id, partner_name, latitude, longitude, precision, curated_name,
             curation_method, country) in cursor:
            location = Location(location_id, partner_name, latitude, longitude, precision,
                                curated_name, curation_method, country)

        cursor.close()

        if not location:
            raise MissingKeyException("No location {}".format(location_id))

        return location
