from swagger_server.models.location import Location
from swagger_server.models.locations import Locations

from backbone_server.location.fetch import LocationFetch
from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

class LocationGetByGPS():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    def get(self, latitude, longitude):

        with self._connection:
            with self._connection.cursor() as cursor:

                cursor.execute("SELECT id FROM locations WHERE ST_X(location) = %s AND ST_Y(location) = %s", (latitude, longitude,))

                locations = Locations()
                locations.locations = []
                locations.count = 0

                #GPS should be unique
                for (location_id,) in cursor:
                    location = LocationFetch.fetch(cursor, location_id)
                    locations.locations.append(location)
                    locations.count = locations.count + 1


        if len(locations.locations) == 0:
            raise MissingKeyException("GPS location not found {}, {}".format(latitude, longitude))

        return locations.locations[0]
