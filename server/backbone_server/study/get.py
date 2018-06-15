from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.study.fetch import StudyFetch

import logging

class StudyGet():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, study_id):

        study = None
        with self._connection:
            with self._connection.cursor() as cursor:

                study = StudyFetch.fetch(cursor, study_id)


        return study
