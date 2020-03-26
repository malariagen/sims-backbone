from openapi_server.models.taxonomies import Taxonomies
from openapi_server.models.taxonomy import Taxonomy


import logging

class TaxonomiesGet():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self):

        with self._connection:
            with self._connection.cursor() as cursor:

                stmt = '''SELECT id, rank, name, os_count, ds_count FROM taxonomy
                LEFT JOIN (SELECT taxon, COUNT(*) AS ds_count FROM derivative_sample GROUP BY taxon) ds ON ds.taxon = taxonomy.id
                LEFT JOIN (SELECT taxonomy_id, COUNT(*) AS os_count FROM original_sample os
                JOIN partner_species_identifier psi ON os.partner_species_id = psi.id
                JOIN taxonomy_identifier ti ON ti.partner_species_identifier_id = psi.id
                JOIN study s ON s.id = os.study_id GROUP BY taxonomy_id) os ON os.taxonomy_id = taxonomy_id
                ;'''
                cursor.execute( stmt, )

                taxonomies = Taxonomies([], 0)

                for (taxonomy_id, rank, name, os_count, ds_count) in cursor:
                    taxa = Taxonomy(taxonomy_id=taxonomy_id,
                                    name=name,
                                    rank=rank,
                                    num_original_samples=os_count,
                                    num_derivative_samples=ds_count)
                    taxonomies.taxonomies.append(taxa)
                    taxonomies.count = taxonomies.count + 1

        return taxonomies
