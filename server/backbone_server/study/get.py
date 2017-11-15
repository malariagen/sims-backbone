from swagger_server.models.study import Study
from swagger_server.models.identifier import Identifier
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.study.fetch import StudyFetch

import logging

class StudyGet():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def __del__(self):
        if self._connection:
            self._connection.close()

    def get(self, study_id):

        study = None

        try:
            cursor = self._connection.cursor()

            study = StudyFetch.fetch(cursor, study_id)

        except MissingKeyException as mke:
            cursor.close()
            raise mke

        cursor.close()

        return study
