from swagger_server.models.taxonomies import Taxonomies
from swagger_server.models.taxonomy import Taxonomy
from backbone_server.errors.missing_key_exception import MissingKeyException


import logging

class TaxonomyPost():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def post(self, taxa):

        ret = Taxonomy()

        with self._connection:
            with self._connection.cursor() as cursor:

                stmt = '''INSERT INTO taxonomies (id, rank, name) VALUES (%s, %s, %s)'''
                cursor.execute( stmt, (taxa.taxonomy_id, taxa.rank, taxa.name))

                stmt = '''SELECT id, rank, name FROM taxonomies WHERE id = %s'''
                cursor.execute( stmt, (taxa.taxonomy_id,))
                for (tid, trank, tname) in cursor:
                    ret.taxonomy_id = tid
                    ret.rank = trank
                    ret.name = tname

        return ret

