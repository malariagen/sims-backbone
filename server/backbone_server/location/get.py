from swagger_server.models.location import Location
from swagger_server.models.identifier import Identifier
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.location.fetch import LocationFetch

import logging

class LocationGetById():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def __del__(self):
        if self._connection:
            self._connection.close()

    def get(self, location_id):

        location = None

        try:
            cursor = self._connection.cursor()

            location = LocationFetch.fetch(cursor, location_id)

        except MissingKeyException as mke:
            cursor.close()
            raise mke

        cursor.close()

        return location
