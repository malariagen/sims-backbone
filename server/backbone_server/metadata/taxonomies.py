from swagger_server.models.taxonomies import Taxonomies
from swagger_server.models.taxonomy import Taxonomy
from backbone_server.errors.missing_key_exception import MissingKeyException


import logging

class TaxonomiesGet():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def __del__(self):
        if self._connection:
            self._connection.close()

    def get(self):

        cursor = self._connection.cursor()

        stmt = '''SELECT id, rank, name FROM taxonomies '''
        cursor.execute( stmt, )

        taxonomies = Taxonomies([], 0)

        for (taxonomy_id, rank, name) in cursor:
            taxa = Taxonomy(taxonomy_id = taxonomy_id, name = name, rank = rank)
            taxonomies.taxonomies.append(taxa)
            taxonomies.count = taxonomies.count + 1

        cursor.close()

        return taxonomies
