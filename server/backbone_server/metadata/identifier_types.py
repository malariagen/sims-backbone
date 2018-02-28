
import logging

class IdentifierTypesGet():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, table='identifiers'):

        identifier_types = []

        with self._connection:
            with self._connection.cursor() as cursor:

                stmt = '''SELECT DISTINCT identifier_type FROM '''+ table
                cursor.execute( stmt, )

                for (identifier_type,) in cursor:
                    identifier_types.append(identifier_type)

        return identifier_types
