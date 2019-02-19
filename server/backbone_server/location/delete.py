from openapi_server.models.location import Location

from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

class LocationDelete():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def delete(self, location_id):

        with self._connection:
            with self._connection.cursor() as cursor:

                return self.run_command(cursor, location_id)

    def run_command(self, cursor, location_id):

        stmt = '''DELETE FROM location_attrs WHERE location_id = %s'''

        cursor.execute( stmt, (location_id,))

        stmt = '''DELETE FROM locations WHERE id = %s'''

        cursor.execute( stmt, (location_id,))

        rc = cursor.rowcount

        if rc != 1:
            raise MissingKeyException("Error deleting location {}".format(location_id))


