from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.location.fetch import LocationFetch

import logging

class LocationGetById():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, location_id):

        location = None

        with self._connection:
            with self._connection.cursor() as cursor:

                location = LocationFetch.fetch(cursor, location_id)


        return location
