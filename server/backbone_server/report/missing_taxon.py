
import logging

from swagger_server.models.studies import Studies
from backbone_server.study.fetch import StudyFetch


class MissingTaxon():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self):

        response = Studies([],0)

        with self._connection:
            with self._connection.cursor() as cursor:

                stmt = '''select distinct study_name from partner_species_identifiers 
                LEFT JOIN taxonomy_identifiers ON taxonomy_identifiers.partner_species_id = partner_species_identifiers.id 
                JOIN studies ON studies.id=study_id 
                WHERE taxonomy_id IS NULL ORDER BY study_name'''

                cursor.execute(stmt)

                studies = []

                for (study_name,) in cursor:
                    studies.append(study_name)

                for study_id in studies:
                    study = StudyFetch.fetch(cursor, study_id)
                    response.studies.append(study)
                    response.count = response.count + 1

        return response
