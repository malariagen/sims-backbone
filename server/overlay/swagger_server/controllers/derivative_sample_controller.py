import connexion
import six

from swagger_server.models.derivative_sample import DerivativeSample  # noqa: E501
from swagger_server.models.derivative_samples import DerivativeSamples  # noqa: E501
from swagger_server import util

import logging

from backbone_server.controllers.derivative_sample_controller  import DerivativeSampleController

derivative_sample_controller = DerivativeSampleController()

def create_derivative_sample(derivativeSample, user=None, token_info=None):  # noqa: E501
    """create_derivative_sample

    Create a DerivativeSample # noqa: E501

    :param derivativeSample: The original sample to create
    :type derivativeSample: dict | bytes

    :rtype: DerivativeSample
    """
    if connexion.request.is_json:
        derivativeSample = DerivativeSample.from_dict(connexion.request.get_json())  # noqa: E501
    return derivative_sample_controller.create_derivative_sample(derivativeSample, user,
                                                                 derivative_sample_controller.token_info(token_info))


def delete_derivative_sample(derivativeSampleId, user=None, token_info=None):  # noqa: E501
    """deletes an DerivativeSample

     # noqa: E501

    :param derivativeSampleId: ID of DerivativeSample to fetch
    :type derivativeSampleId: str

    :rtype: None
    """
    return derivative_sample_controller.delete_derivative_sample(derivativeSampleId, user,
                                                                 derivative_sample_controller.token_info(token_info))


def download_derivative_sample(derivativeSampleId, user=None, token_info=None):  # noqa: E501
    """fetches an DerivativeSample

     # noqa: E501

    :param derivativeSampleId: ID of DerivativeSample to fetch
    :type derivativeSampleId: str

    :rtype: DerivativeSample
    """
    return derivative_sample_controller.download_derivative_sample(derivativeSampleId, user,
                                                                   derivative_sample_controller.token_info(token_info))



def download_derivative_samples(search_filter=None, start=None, count=None, user=None, token_info=None):  # noqa: E501
    """fetches DerivativeSamples

     # noqa: E501

    :param search_filter: search filter e.g. studyId:0000, attr:name:value, location:locationId, taxa:taxId, eventSet:setName
    :type search_filter: str
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int

    :rtype: DerivativeSamples
    """
    return derivative_sample_controller.download_derivative_samples(search_filter, start,
                                                                    count, user,
                                                                    derivative_sample_controller.token_info(token_info))

def download_derivative_samples_by_attr(propName, propValue, studyName=None, user=None, token_info=None):  # noqa: E501
    """fetches one or more DerivativeSample by property value

     # noqa: E501

    :param propName: name of property to search
    :type propName: str
    :param propValue: matching value of property to search
    :type propValue: str
    :param studyName: if you want to restrict the search to a study e.g. for partner_id
    :type studyName: str

    :rtype: DerivativeSamples
    """
    return derivative_sample_controller.download_derivative_samples_by_attr(propName, propValue, studyName, user,
                                                                            derivative_sample_controller.token_info(token_info))

def download_derivative_samples_by_event_set(eventSetId, start=None, count=None, user=None, token_info=None):
    """fetches DerivativeSamples in a given event set

     # noqa: E501

    :param eventSetId: Event Set name
    :type eventSetId: str
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int

    :rtype: DerivativeSamples
    """
    return derivative_sample_controller.download_derivative_samples_by_event_set(eventSetId,start,
                                                                                 count, user,
                                                                                 derivative_sample_controller.token_info(token_info))


def download_derivative_samples_by_os_attr(propName, propValue, studyName=None, user=None, token_info=None):  # noqa: E501
    """fetches one or more derivativeSamples by property value of associated original samples

     # noqa: E501

    :param propName: name of property to search
    :type propName: str
    :param propValue: matching value of property to search
    :type propValue: str
    :param studyName: if you want to restrict the search to a study e.g. for partner_id
    :type studyName: str

    :rtype: DerivativeSamples
    """
    return derivative_sample_controller.download_derivative_samples_by_os_attr(propName, propValue, studyName, user,
                                                                               derivative_sample_controller.token_info(token_info))


def download_derivative_samples_by_study(studyName, start=None, count=None, user=None, token_info=None):
    """fetches DerivativeSamples for a study

     # noqa: E501

    :param studyName: 4 digit study code
    :type studyName: str
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int

    :rtype: DerivativeSamples
    """
    return derivative_sample_controller.download_derivative_samples_by_study(studyName, start,
                                                                             count, user,
                                                                             derivative_sample_controller.token_info(token_info))

def download_derivative_samples_by_taxa(taxaId, start=None, count=None, user=None, token_info=None):
    """fetches DerivativeSamples for a given taxonomy classification code

    :param taxaId: NCBI taxonomy code
    :type taxaId: str
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int

    :rtype: DerivativeSamples
    """
    return derivative_sample_controller.download_derivative_samples_by_taxa(taxaId, start,
                                                                            count, user,
                                                                            derivative_sample_controller.token_info(token_info))

def update_derivative_sample(derivativeSampleId, derivativeSample, user=None, token_info=None):  # noqa: E501
    """updates an DerivativeSample

     # noqa: E501

    :param derivativeSampleId: ID of DerivativeSample to update
    :type derivativeSampleId: str
    :param derivativeSample:
    :type derivativeSample: dict | bytes

    :rtype: DerivativeSample
    """
    if connexion.request.is_json:
        derivativeSample = DerivativeSample.from_dict(connexion.request.get_json())  # noqa: E501
    return derivative_sample_controller.update_derivative_sample(derivativeSampleId, derivativeSample, user,
                                                                 derivative_sample_controller.token_info(token_info))
