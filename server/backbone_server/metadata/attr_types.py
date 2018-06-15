
import logging

class AttrTypesGet():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, table='attrs'):

        attr_types = []

        with self._connection:
            with self._connection.cursor() as cursor:

                if table == 'attrs':
                    stmt = '''SELECT DISTINCT attr_type FROM attrs a'''
                else:
                    stmt = '''SELECT DISTINCT attr_type FROM attrs a
                    JOIN '''+ table + ' ON a.id = ' + table + '.attr_id'
                cursor.execute( stmt, )

                for (attr_type,) in cursor:
                    attr_types.append(attr_type)

        return attr_types
