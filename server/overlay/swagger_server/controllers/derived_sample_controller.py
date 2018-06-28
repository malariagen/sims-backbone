import connexion
import six

from swagger_server.models.derived_sample import DerivedSample  # noqa: E501
from swagger_server.models.derived_samples import DerivedSamples  # noqa: E501
from swagger_server import util

import logging

from backbone_server.controllers.derived_sample_controller  import DerivedSampleController

derived_sample_controller = DerivedSampleController()

def create_derived_sample(derivedSample, user=None, token_info=None):  # noqa: E501
    """create_derived_sample

    Create a DerivedSample # noqa: E501

    :param derivedSample: The original sample to create
    :type derivedSample: dict | bytes

    :rtype: DerivedSample
    """
    if connexion.request.is_json:
        derivedSample = DerivedSample.from_dict(connexion.request.get_json())  # noqa: E501
    return derived_sample_controller.create_derived_sample(derivedSample, user,
                                                           derived_sample_controller.token_info(token_info))


def delete_derived_sample(derivedSampleId, user=None, token_info=None):  # noqa: E501
    """deletes an DerivedSample

     # noqa: E501

    :param derivedSampleId: ID of DerivedSample to fetch
    :type derivedSampleId: str

    :rtype: None
    """
    return derived_sample_controller.delete_derived_sample(derivedSampleId, user,
                                                           derived_sample_controller.token_info(token_info))


def download_derived_sample(derivedSampleId, user=None, token_info=None):  # noqa: E501
    """fetches an DerivedSample

     # noqa: E501

    :param derivedSampleId: ID of DerivedSample to fetch
    :type derivedSampleId: str

    :rtype: DerivedSample
    """
    return derived_sample_controller.download_derived_sample(derivedSampleId, user,
                                                           derived_sample_controller.token_info(token_info))


def download_derived_samples_by_attr(propName, propValue, studyName=None, user=None, token_info=None):  # noqa: E501
    """fetches one or more DerivedSample by property value

     # noqa: E501

    :param propName: name of property to search
    :type propName: str
    :param propValue: matching value of property to search
    :type propValue: str
    :param studyName: if you want to restrict the search to a study e.g. for partner_id
    :type studyName: str

    :rtype: DerivedSamples
    """
    return derived_sample_controller.download_derived_samples_by_attr(propName, propValue, studyName, user,
                                                           derived_sample_controller.token_info(token_info))


def download_derived_samples_by_os_attr(propName, propValue, studyName=None, user=None, token_info=None):  # noqa: E501
    """fetches one or more derivedSamples by property value of associated original samples

     # noqa: E501

    :param propName: name of property to search
    :type propName: str
    :param propValue: matching value of property to search
    :type propValue: str
    :param studyName: if you want to restrict the search to a study e.g. for partner_id
    :type studyName: str

    :rtype: DerivedSamples
    """
    return derived_sample_controller.download_derived_samples_by_os_attr(propName, propValue, studyName, user,
                                                           derived_sample_controller.token_info(token_info))


def update_derived_sample(derivedSampleId, derivedSample, user=None, token_info=None):  # noqa: E501
    """updates an DerivedSample

     # noqa: E501

    :param derivedSampleId: ID of DerivedSample to update
    :type derivedSampleId: str
    :param derivedSample: 
    :type derivedSample: dict | bytes

    :rtype: DerivedSample
    """
    if connexion.request.is_json:
        derivedSample = DerivedSample.from_dict(connexion.request.get_json())  # noqa: E501
    return derived_sample_controller.update_derived_sample(derivedSampleId, derivedSample, user,
                                                           derived_sample_controller.token_info(token_info))
