from openapi_server.models.location import Location
from openapi_server.models.locations import Locations
from openapi_server.models.attr import Attr
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.location.fetch import LocationFetch

import logging

class LocationsGet():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, study_code=None, start=None, count=None, orderby='location'):

        result = Locations()

        with self._connection:
            with self._connection.cursor() as cursor:

                query_body = ' FROM locations l'
                args = ()
                if study_code or orderby == 'study_name':
                    query_body = query_body + ''' LEFT JOIN location_attrs li ON li.location_id = l.id
                    JOIN attrs a ON li.attr_id = a.id
                    LEFT JOIN studies s ON s.id = a.study_id'''
                    if study_code:
                        query_body = query_body + " WHERE study_code = %s"
                        args = (study_code[:4], )

                count_args = args
                count_query = 'SELECT COUNT(DISTINCT l.id) ' + query_body

                if orderby:
                    query_body = query_body + " ORDER BY " + orderby + ", l.id"

                if not (start is None and count is None):
                    query_body = query_body + ' LIMIT %s OFFSET %s'
                    args = args + (count, start)

                if orderby:
                    cursor.execute('SELECT DISTINCT l.id, ' + orderby + query_body, args)
                else:
                    cursor.execute('SELECT DISTINCT l.id, l.curated_name ' + query_body, args)

                locations = []
                for (location_id, ignored) in cursor:
                    with self._connection.cursor() as lcursor:
                        location = LocationFetch.fetch(lcursor, location_id)
                        locations.append(location)


                if not (start is None and count is None):
                    cursor.execute(count_query, count_args)
                    result.count = cursor.fetchone()[0]
                else:
                    result.count = len(locations)

        result.locations = locations

        return result
