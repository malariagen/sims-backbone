
import logging

from swagger_server.models.studies import Studies
from backbone_server.study.fetch import StudyFetch


class MultipleLocationGPS():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self):

        response = Studies([],0)

        with self._connection:
            with self._connection.cursor() as cursor:

                #, curated_name, accuracy, country, partner_name
                # ST_X(location) as latitude, ST_Y(location) as longitude
                stmt = '''select study_code from location_attrs li
                JOIN studies s ON li.study_id = s.id
                GROUP BY attr_type, attr_value, study_code
                having count(attr_value) > 1'''

                cursor.execute(stmt)

                studies = []

                for (study_name,) in cursor:
                    studies.append(study_name)

                for study_id in studies:
                    study = StudyFetch.fetch(cursor, study_id)
                    response.studies.append(study)
                    response.count = response.count + 1

        return response
