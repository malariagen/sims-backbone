from swagger_server.models.location import Location
from swagger_server.models.locations import Locations
from swagger_server.models.identifier import Identifier
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.location.fetch import LocationFetch

import logging

class LocationsGet():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def __del__(self):
        if self._connection:
            self._connection.close()

    def get(self, study_name=None, start=None, count=None, orderby=None):

        result = Locations()

        try:
            cursor = self._connection.cursor()

            query_body = ' FROM locations l'
            args = ()
            if study_name or orderby == 'study_name':
                query_body = query_body + ''' LEFT JOIN location_identifiers li ON li.location_id = l.id
                LEFT JOIN studies s ON s.id = li.study_id'''
                if study_name:
                    query_body = query_body + " WHERE study_name = %s"
                    args = (study_name, )

            count_args = args
            count_query = 'SELECT COUNT(DISTINCT l.id) ' + query_body

            query_body = query_body + " ORDER BY " + orderby + ", l.id"

            if not (start is None and count is None):
                query_body = query_body + ' LIMIT %s OFFSET %s'
                args = args + (count, start)

            cursor.execute('SELECT DISTINCT l.id, ' + orderby + query_body, args)

            locations = []
            for (location_id, ignored) in cursor:
                lcursor = self._connection.cursor()
                location = LocationFetch.fetch(lcursor, location_id)
                locations.append(location)
                lcursor.close()

        except MissingKeyException as mke:
            cursor.close()
            raise mke

        if not (start is None and count is None):
            cursor.execute(count_query, count_args)
            result.count = cursor.fetchone()[0]
        else:
            result.count = len(locations)

        result.locations = locations
        cursor.close()

        return result