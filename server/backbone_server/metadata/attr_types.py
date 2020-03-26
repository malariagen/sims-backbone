
import logging

class AttrTypesGet():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, parent_type):

        attr_types = []

        with self._connection:
            with self._connection.cursor() as cursor:

                stmt = '''SELECT DISTINCT attr_type FROM attr a'''
                if parent_type and not parent_type == 'attrs':
            # enum: ['os', 'ds', 'ad', 'loc', 'se']
                    table = None
                    if parent_type == 'os':
                        table = 'original_sample_attr'
                    elif parent_type == 'ds':
                        table = 'derivative_sample_attr'
                    elif parent_type == 'ad':
                        table = 'assay_data_attr'
                    elif parent_type == 'loc':
                        table = 'location_attr'
                    elif parent_type == 'se':
                        table = 'sampling_event_attr'

                    if table:
                        stmt += ''' JOIN '''+ table + ' ON a.id = ' + table + '.attr_id'
                cursor.execute(stmt, )

                for (attr_type,) in cursor:
                    attr_types.append(attr_type)

        return attr_types
