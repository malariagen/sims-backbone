import connexion
from swagger_server.models.sample import Sample
from swagger_server.models.samples import Samples
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

import logging

from backbone_server.sample.post import SamplePost
from backbone_server.sample.put import SamplePut
from backbone_server.sample.get import SampleGetById
from backbone_server.sample.delete import SampleDelete
from backbone_server.sample.get_by_identifier import SampleGetByIdentifier

from backbone_server.connect  import get_connection

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException

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

    retcode = 200
    samp = None

    try:
        post = SamplePost(get_connection())

        samp = post.post(sample)
    except DuplicateKeyException as dke:
        logging.getLogger(__name__).error("create_sample: {}".format(repr(dke)))
        retcode = 422

    return samp, retcode


def delete_sample(sampleId):
    """
    deletes an sample
    
    :param sampleId: ID of sample to fetch
    :type sampleId: str

    :rtype: None
    """
    delete = SampleDelete(get_connection())

    retcode = 200
    samp = None

    try:
        delete.delete(sampleId)
    except MissingKeyException as dme:
        logging.getLogger(__name__).error("delete_sample: {}".format(repr(dme)))
        retcode = 404

    return None, retcode


def download_sample(sampleId):
    """
    fetches an sample
    
    :param sampleId: ID of sample to fetch
    :type sampleId: str

    :rtype: Sample
    """
    get = SampleGetById(get_connection())

    retcode = 200
    samp = None

    try:
        samp = get.get(sampleId)
    except MissingKeyException as dme:
        logging.getLogger(__name__).error("download_sample: {}".format(repr(dme)))
        retcode = 404

    return samp, retcode


def download_sample_by_identifier(propName, propValue):
    """
    fetches a sample by property value
    
    :param propName: name of property to search
    :type propName: str
    :param propValue: matching value of property to search
    :type propValue: str

    :rtype: Sample
    """
    get = SampleGetByIdentifier(get_connection())

    retcode = 200
    samp = None

    try:
        samp = get.get(propName, propValue)
    except MissingKeyException as dme:
        logging.getLogger(__name__).error("download_sample: {}".format(repr(dme)))
        retcode = 404

    return samp, retcode


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
    retcode = 200
    samp = None

    try:
        put = SamplePut(get_connection())

        samp = put.put(sampleId, sample)
    except DuplicateKeyException as dke:
        logging.getLogger(__name__).error("update_sample: {}".format(repr(dke)))
        retcode = 422
    except MissingKeyException as dme:
        logging.getLogger(__name__).error("update_sample: {}".format(repr(dme)))
        retcode = 404

    return samp, retcode

