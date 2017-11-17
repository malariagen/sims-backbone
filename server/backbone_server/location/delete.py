from swagger_server.models.location import Location

from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

class LocationDelete():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def delete(self, location_id):

        cursor = self._connection.cursor()

        stmt = '''DELETE FROM location_identifiers WHERE location_id = %s'''

        cursor.execute( stmt, (location_id,))

        stmt = '''DELETE FROM locations WHERE id = %s'''

        cursor.execute( stmt, (location_id,))

        rc = cursor.rowcount

        self._connection.commit()

        cursor.close()

        if rc != 1:
            raise MissingKeyException("Error deleting location {}".format(location_id))


