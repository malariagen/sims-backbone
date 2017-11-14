import connexion
from swagger_server.models.studies import Studies
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
