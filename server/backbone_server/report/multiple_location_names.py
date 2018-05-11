
import logging

from swagger_server.models.studies import Studies
from backbone_server.study.fetch import StudyFetch


class MultipleLocationNames():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self):

        response = Studies([],0)

        with self._connection:
            with self._connection.cursor() as cursor:

                #, curated_name, accuracy, country, partner_name
                # ST_X(location) as latitude, ST_Y(location) as longitude
                stmt = '''select study_code from locations l
                    join location_attrs li ON li.location_id = l.id
                    JOIN studies s ON li.study_id = s.id
                    group by location, study_code
                    having count(location) > 1 ORDER BY study_code;'''

                cursor.execute(stmt)

                studies = []

                for (study_name,) in cursor:
                    studies.append(study_name)

                for study_id in studies:
                    study = StudyFetch.fetch(cursor, study_id)
                    response.studies.append(study)
                    response.count = response.count + 1

        return response
