from openapi_server.models.studies import Studies
from openapi_server.models.study import Study
from backbone_server.controllers.base_controller import BaseController


import logging

class StudiesGet():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, studies):

        with self._connection:
            with self._connection.cursor() as cursor:

                ret_studies = Studies([], 0)

                stmt = '''SELECT study_name, study_code FROM studies'''

                study_filter = BaseController.study_filter(studies)

                if study_filter:
                    stmt += f' WHERE {study_filter}'

                stmt += ' ORDER BY study_code'

                cursor.execute(stmt, )


                for (study_name, study_code) in cursor:
                    study = Study(name=study_name, code=study_code)
                    ret_studies.studies.append(study)
                    ret_studies.count = ret_studies.count + 1

        return ret_studies
