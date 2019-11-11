from openapi_server.models.location import Location
from openapi_server.models.locations import Locations

from backbone_server.location.fetch import LocationFetch
from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.permission_exception import PermissionException

import logging

class LocationGetByGPS():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    def get(self, latitude, longitude, studies):

        with self._connection:
            with self._connection.cursor() as cursor:

                cursor.execute("SELECT id FROM locations WHERE ST_X(location) = %s AND ST_Y(location) = %s", (latitude, longitude,))

                locations = Locations()
                locations.locations = []
                locations.count = 0
                ids = []

                for (location_id,) in cursor:
                    ids.append(str(location_id))

                for location_id in ids:
                    try:
                        location = LocationFetch.fetch(cursor, location_id, studies)
                        locations.locations.append(location)
                        locations.count = locations.count + 1
                    except PermissionException as pme:
                        pass


        if len(locations.locations) == 0:
            raise MissingKeyException("GPS location not found {}, {}".format(latitude, longitude))

        return locations
