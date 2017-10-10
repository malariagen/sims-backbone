import connexion
from swagger_server.models.sample import Sample
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime


def download_source_sample(sourceId, sourceSampleId, studyId=None):
    """
    fetches an sample
    
    :param sourceId: ID of source to query
    :type sourceId: str
    :param sourceSampleId: ID of sample to fetch
    :type sourceSampleId: str
    :param studyId: which study the sample belongs to
    :type studyId: int

    :rtype: Sample
    """
    return 'do some magic!'
