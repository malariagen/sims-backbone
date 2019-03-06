from openapi_server.models.location import Location
from openapi_server.models.locations import Locations

from backbone_server.location.fetch import LocationFetch
from backbone_server.errors.missing_key_exception import MissingKeyException

import logging


class LocationGetByAttr():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    def get(self, attr_type, attr_value, study_code):

        with self._connection:
            with self._connection.cursor() as cursor:

                query = '''SELECT DISTINCT location_id FROM location_attrs
                           JOIN attrs ON attrs.id = location_attrs.attr_id'''

                if study_code:
                    query += ''' LEFT JOIN studies s ON s.id = a.study_id'''

                query += ''' WHERE attr_type = %s AND attr_value = %s'''
                args = (attr_type, attr_value,)

                if study_code:
                    query += ''' AND study_code = %s'''
                    args += (study_code[:4], )

                cursor.execute(query, args)

                locations=Locations()
                locations.locations=[]
                locations.count=0
                locs=[]

                for (location_id,) in cursor:
                    locs.append(location_id)

                for location_id in locs:
                    location=LocationFetch.fetch(cursor, location_id)
                    locations.locations.append(location)
                    locations.count=locations.count + 1

        return locations
