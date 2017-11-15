import connexion
from swagger_server.models.studies import Studies
from datetime import date, datetime
from typing import List, Dict
from six import iteritems

from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.integrity_exception import IntegrityException
from backbone_server.study.gets import StudiesGet
from backbone_server.study.get import StudyGet
from backbone_server.study.put import StudyPut

from backbone_server.connect  import get_connection

import logging

class StudyController():

    @staticmethod
    def download_studies(start=None, count=None):
        """
        fetches studies
        
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: Studies
        """
        get = StudiesGet(get_connection())

        studies = get.get()

        return studies, 200

    @staticmethod
    def download_study(studyId):
        """
        fetches a study
        
        :param studyId: ID of study to fetch
        :type studyId: str

        :rtype: Study
        """
        get = StudyGet(get_connection())

        study = None
        retcode = 200
        try:
            study = get.get(studyId)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("update_study: {}".format(repr(dme)))
            retcode = 404

        return study, retcode


    @staticmethod
    def update_study(studyId, study, user=None):
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
            put = StudyPut(get_connection())

            updated_study = put.put(studyId, study)
        except IntegrityException as dme:
            logging.getLogger(__name__).error("update_study: {}".format(repr(dme)))
            retcode = 422
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("update_study: {}".format(repr(dme)))
            retcode = 404

        return updated_study, retcode
