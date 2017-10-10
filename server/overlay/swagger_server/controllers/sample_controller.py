import connexion
from swagger_server.models.sample import Sample
from swagger_server.models.samples import Samples
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime


def create_sample(sample):
    """
    create_sample
    Create a sample
    :param sample: 
    :type sample: dict | bytes

    :rtype: Sample
    """
    if connexion.request.is_json:
        sample = Sample.from_dict(connexion.request.get_json())
    return 'do some magic!'


def delete_sample(sampleId):
    """
    deletes an sample
    
    :param sampleId: ID of sample to fetch
    :type sampleId: str

    :rtype: None
    """
    return 'do some magic!'


def download_sample(sampleId):
    """
    fetches an sample
    
    :param sampleId: ID of sample to fetch
    :type sampleId: str

    :rtype: Sample
    """
    return 'do some magic!'


def download_samples_by_property(propName, propValue, start=None, count=None, orderby=None):
    """
    fetches samples by property value
    
    :param propName: name of property to search
    :type propName: str
    :param propValue: matching value of property to search
    :type propValue: str
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int
    :param orderby: how to order the result set
    :type orderby: str

    :rtype: Samples
    """
    return 'do some magic!'


def update_sample(sampleId, sample):
    """
    updates an sample
    
    :param sampleId: ID of sample to update
    :type sampleId: str
    :param sample: 
    :type sample: dict | bytes

    :rtype: Sample
    """
    if connexion.request.is_json:
        sample = Sample.from_dict(connexion.request.get_json())
    return 'do some magic!'
