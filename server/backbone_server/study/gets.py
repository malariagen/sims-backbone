from swagger_server.models.studies import Studies
from swagger_server.models.study import Study
from backbone_server.errors.missing_key_exception import MissingKeyException


import logging

class StudiesGet():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self):

        cursor = self._connection.cursor()

        stmt = '''SELECT study_name, study_code FROM studies'''
        cursor.execute( stmt, )

        studies = Studies([], 0)

        for (study_name, study_code) in cursor:
            study = Study(name = study_name, code = study_code)
            studies.studies.append(study)
            studies.count = studies.count + 1

        cursor.close()

        return studies
