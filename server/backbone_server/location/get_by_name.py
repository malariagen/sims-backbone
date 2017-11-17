from swagger_server.models.location import Location
from swagger_server.models.locations import Locations

from backbone_server.location.fetch import LocationFetch
from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

class LocationGetByPartnerName():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    def get(self, partner_id):

        cursor = self._connection.cursor()

        cursor.execute('''SELECT DISTINCT location_id FROM location_identifiers 
                       WHERE identifier_type = %s AND identifier_value = %s''', ('partner_name', partner_id,))

        locations = Locations()
        locations.locations = []
        locations.count = 0

        for (location_id,) in cursor:
            location = LocationFetch.fetch(cursor, location_id)
            locations.locations.append(location)
            locations.count = locations.count + 1

        cursor.close()

        if len(locations.locations) == 0:
            raise MissingKeyException("Partner location not found {}".format(partner_id))

        return locations
