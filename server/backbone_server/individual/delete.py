from openapi_server.models.individual import Individual

from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.individual.edit import IndividualEdit

import logging

class IndividualDelete():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def delete(self, individual_id):

        with self._connection:
            with self._connection.cursor() as cursor:

                return self.run_command(cursor, individual_id)

    def run_command(self, cursor, individual_id):

        IndividualEdit.delete_attrs(cursor, individual_id)

        stmt = '''DELETE FROM individuals WHERE id = %s'''

        cursor.execute( stmt, (individual_id,))

        rc = cursor.rowcount

        if rc != 1:
            raise MissingKeyException("Error deleting individual {}".format(individual_id))


