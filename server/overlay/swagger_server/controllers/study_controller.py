import connexion
from swagger_server.models.studies import Studies
from swagger_server.models.study import Study
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from backbone_server.controllers.study_controller import StudyController

def download_studies(start=None, count=None):
    """
    fetches studies
    
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int

    :rtype: Studies
    """
    return StudyController.download_studies(start, count)


def download_study(studyId):
    """
    fetches a study
    
    :param studyId: ID of study to fetch
    :type studyId: str

    :rtype: Study
    """
    return StudyController.download_study(studyId)


def update_study(studyId, study, user=None):
    """
    updates a study
    
    :param studyId: ID of study to update
    :type studyId: str
    :param study: 
    :type study: dict | bytes

    :rtype: Study
    """
    if connexion.request.is_json:
        study = Study.from_dict(connexion.request.get_json())
    return StudyController.update_study(studyId, study, user)
