from backbone_server.controllers.base_controller import BaseController
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.study.fetch import StudyFetch

import logging

class StudyGet():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, study_id, studies):

        study = None
        with self._connection:
            with self._connection.cursor() as cursor:

                BaseController.has_study_permission(studies, study_id,
                                                    BaseController.GET_PERMISSION)

                study = StudyFetch.fetch(cursor, study_id)


        return study
