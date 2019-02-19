from openapi_server.models.location import Location
from openapi_server.models.locations import Locations

from backbone_server.location.fetch import LocationFetch
from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

class LocationGetByPartnerName():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    def get(self, partner_id):

        with self._connection:
            with self._connection.cursor() as cursor:

                cursor.execute('''SELECT DISTINCT location_id FROM location_attrs
                               JOIN attrs ON attrs.id = location_attrs.attr_id
                               WHERE attr_type = %s AND attr_value = %s''', ('partner_name', partner_id,))

                locations = Locations()
                locations.locations = []
                locations.count = 0
                locs = []

                for (location_id,) in cursor:
                    locs.append(location_id)

                for location_id in locs:
                    location = LocationFetch.fetch(cursor, location_id)
                    locations.locations.append(location)
                    locations.count = locations.count + 1

        if len(locations.locations) == 0:
            raise MissingKeyException("Partner location not found {}".format(partner_id))

        return locations
