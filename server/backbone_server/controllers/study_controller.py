from swagger_server.models.studies import Studies

from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.integrity_exception import IntegrityException
from backbone_server.study.gets import StudiesGet
from backbone_server.study.get import StudyGet
from backbone_server.study.put import StudyPut

from backbone_server.controllers.base_controller  import BaseController

from backbone_server.errors.permission_exception import PermissionException

import logging

class StudyController(BaseController):

    def download_studies(self, start=None, count=None, user=None, auths = None):
        """
        fetches studies
        
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: Studies
        """

        try:
            self.check_permissions(None, auths)
        except PermissionException as pe:
            self.log_action(user, 'download_studies', None, None, None, 403)
            return pe.message, 403

        get = StudiesGet(self.get_connection())

        studies = get.get()

        self.log_action(user, 'download_studies', None, None, studies, 403)

        return studies, 200

    def download_study(self, studyName, user=None, auths = None):
        """
        fetches a study
        
        :param studyName: ID of study to fetch
        :type studyName: str

        :rtype: Study
        """

        try:
            self.check_permissions(None, auths)
        except PermissionException as pe:
            self.log_action(user, 'download_study', studyName, None, None, 403)
            return pe.message, 403

        get = StudyGet(self.get_connection())

        study = None
        retcode = 200
        try:
            study = get.get(studyName)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("update_study: {}".format(repr(dme)))
            retcode = 404

        self.log_action(user, 'download_study', studyName, None, study, retcode)

        return study, retcode


    def update_study(self, studyName, study, user=None, auths = None):
        """
        updates a study
        
        :param studyName: ID of study to update
        :type studyName: str
        :param study: 
        :type study: dict | bytes

        :rtype: Study
        """

        try:
            study_id = None;
            if studyName:
                study_id = studyName[:4]

            self.check_permissions(study_id, auths)
        except PermissionException as pe:
            self.log_action(user, 'update_study', studyName, study, None, 403)
            return pe.message, 403


        retcode = 200
        updated_study = None

        try:
            put = StudyPut(self.get_connection())

            updated_study = put.put(studyName, study)
        except IntegrityException as dme:
            logging.getLogger(__name__).error("update_study: {}".format(repr(dme)))
            retcode = 422
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("update_study: {}".format(repr(dme)))
            retcode = 404

        self.log_action(user, 'update_study', studyName, study, updated_study, retcode)

        return updated_study, retcode
