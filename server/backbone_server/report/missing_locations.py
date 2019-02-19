
import logging

from openapi_server.models.studies import Studies
from backbone_server.study.fetch import StudyFetch


class MissingLocations():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, include_country):

        response = Studies([],0)

        with self._connection:
            with self._connection.cursor() as cursor:

                stmt = '''select distinct study_code, accuracy FROM sampling_events 
                LEFT JOIN studies ON studies.id = study_id
                LEFT JOIN locations ON locations.id = location_id
                WHERE location_id IS NULL OR locations.accuracy = 'country';'''

                cursor.execute(stmt)

                studies = []

                for (study_name, accuracy) in cursor:
                    if accuracy and accuracy == 'country':
                        if include_country:
                            studies.append(study_name)
                    else:
                        studies.append(study_name)

                for study_id in studies:
                    study = StudyFetch.fetch(cursor, study_id)
                    response.studies.append(study)
                    response.count = response.count + 1

        return response
