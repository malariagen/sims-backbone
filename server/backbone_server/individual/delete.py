from swagger_server.models.individual import Individual

from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

class IndividualDelete():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def delete(self, individual_id):

        with self._connection:
            with self._connection.cursor() as cursor:

                stmt = '''DELETE FROM individual_attrs WHERE individual_id = %s'''

                cursor.execute( stmt, (individual_id,))

                stmt = '''DELETE FROM individuals WHERE id = %s'''

                cursor.execute( stmt, (individual_id,))

                rc = cursor.rowcount

        if rc != 1:
            raise MissingKeyException("Error deleting individual {}".format(individual_id))


