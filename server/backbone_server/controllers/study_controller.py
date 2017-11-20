from swagger_server.models.studies import Studies

from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.integrity_exception import IntegrityException
from backbone_server.study.gets import StudiesGet
from backbone_server.study.get import StudyGet
from backbone_server.study.put import StudyPut

from backbone_server.controllers.base_controller  import BaseController

import logging

class StudyController(BaseController):

    def download_studies(self, start=None, count=None, user=None):
        """
        fetches studies
        
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: Studies
        """
        get = StudiesGet(self.get_connection())

        studies = get.get()

        return studies, 200

    def download_study(self, studyId, user=None):
        """
        fetches a study
        
        :param studyId: ID of study to fetch
        :type studyId: str

        :rtype: Study
        """
        get = StudyGet(self.get_connection())

        study = None
        retcode = 200
        try:
            study = get.get(studyId)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("update_study: {}".format(repr(dme)))
            retcode = 404

        return study, retcode


    def update_study(self, studyId, study, user=None):
        """
        updates a study
        
        :param studyId: ID of study to update
        :type studyId: str
        :param study: 
        :type study: dict | bytes

        :rtype: Study
        """

        retcode = 200
        updated_study = None

        try:
            put = StudyPut(self.get_connection())

            updated_study = put.put(studyId, study)
        except IntegrityException as dme:
            logging.getLogger(__name__).error("update_study: {}".format(repr(dme)))
            retcode = 422
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("update_study: {}".format(repr(dme)))
            retcode = 404

        return updated_study, retcode
