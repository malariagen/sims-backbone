import connexion

from openapi_server.models.original_sample import OriginalSample  # noqa: E501
from openapi_server.models.original_samples import OriginalSamples  # noqa: E501
from openapi_server import util

import logging

from backbone_server.controllers.original_sample_controller import OriginalSampleController

original_sample_controller = OriginalSampleController()


def create_original_sample(body, user=None, token_info=None):
    """
    create_original_sample
    Create a originalSample
    :param originalSample:
    :type originalSample: dict | bytes

    :rtype: OriginalSample
    """
    if connexion.request.is_json:
        original_sample = OriginalSample.from_dict(
            connexion.request.get_json())

    return original_sample_controller.create_original_sample(original_sample,
                                                             studies=None,
                                                             user=user,
                                                             auths=original_sample_controller.token_info(token_info))


def delete_original_sample(original_sample_id, user=None, token_info=None):
    """
    deletes an originalSample

    :param originalSampleId: ID of originalSample to fetch
    :type originalSampleId: str

    :rtype: None
    """
    return original_sample_controller.delete_original_sample(original_sample_id, studies=None, user=user,
                                                             auths=original_sample_controller.token_info(token_info))


def download_original_sample(original_sample_id, user=None, token_info=None):
    """
    fetches an originalSample

    :param originalSampleId: ID of originalSample to fetch
    :type originalSampleId: str

    :rtype: OriginalSample
    """
    return original_sample_controller.download_original_sample(original_sample_id, studies=None, user=user,
                                                               auths=original_sample_controller.token_info(token_info))


def download_original_samples(search_filter=None, value_type=None, start=None, count=None,
                              studies=None, user=None, token_info=None):  # noqa: E501
    """fetches originalSamples

     # noqa: E501

    :param search_filter: search filter e.g. studyId:0000, attr:name:value, location:locationId, taxa:taxId, eventSet:setName
    :type search_filter: str
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int

    :rtype: OriginalSamples
    """
    return original_sample_controller.download_original_samples(search_filter,
                                                                value_type=value_type,
                                                                start=start,
                                                                count=count,
                                                                studies=studies, user=user,
                                                                auths=original_sample_controller.token_info(token_info))


def download_original_samples_by_event_set(event_set_id, start=None, count=None, user=None, token_info=None):
    """
    fetches originalSamples in a given event set

    :param eventSetId: Event Set name
    :type eventSetId: str
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int

    :rtype: OriginalSamples
    """
    return original_sample_controller.download_original_samples_by_event_set(event_set_id, start,
                                                                             count, studies=None, user=user,
                                                                             auths=original_sample_controller.token_info(token_info))


def download_original_samples_by_attr(prop_name, prop_value, study_name=None, value_type=None,
                                      start=None, count=None,
                                      studies=None, user=None, token_info=None):
    """
    fetches a originalSample by property value

    :param propName: name of property to search
    :type propName: str
    :param propValue: matching value of property to search
    :type propValue: str

    :rtype: OriginalSample
    """
    return original_sample_controller.download_original_samples_by_attr(prop_name, prop_value,
                                                                        study_name,
                                                                        value_type=value_type,
                                                                        start=start,
                                                                        count=count,
                                                                        studies=studies, user=user,
                                                                        auths=original_sample_controller.token_info(token_info))


def download_original_samples_by_location(location_id, start=None, count=None,
                                          studies=None, user=None, token_info=None):
    """
    fetches originalSamples for a location

    :param locationId: location
    :type locationId: str
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int

    :rtype: OriginalSamples
    """
    return original_sample_controller.download_original_samples_by_location(location_id, start,
                                                                            count,
                                                                            studies=studies, user=user,
                                                                            auths=original_sample_controller.token_info(token_info))


def download_original_samples_by_manifest(release_id, start=None,
                                          count=None, studies=None, user=None,
                                          token_info=None):  # noqa: E501
    """fetches OriginalSamples in a given release

     # noqa: E501

    :param release_id: release name
    :type release_id: str
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int

    :rtype: OriginalSamples
    """
    return original_sample_controller.download_original_samples_by_manifest(release_id, start,
                                                                            count,
                                                                            studies=studies, user=user,
                                                                            auths=original_sample_controller.token_info(token_info))

def download_original_samples_by_study(study_name, start=None, count=None,
                                       studies=None, user=None, token_info=None):
    """
    fetches originalSamples for a study

    :param studyName: 4 digit study code
    :type studyName: str
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int

    :rtype: OriginalSamples
    """
    return original_sample_controller.download_original_samples_by_study(study_name, start,
                                                                         count,
                                                                         studies=studies, user=user,
                                                                         auths=original_sample_controller.token_info(token_info))


def download_original_samples_by_taxa(taxa_id, start=None, count=None,
                                      studies=None, user=None, token_info=None):
    """
    fetches originalSamples for a given taxonomy classification code

    :param taxaId: NCBI taxonomy code
    :type taxaId: str
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int

    :rtype: OriginalSamples
    """
    return original_sample_controller.download_original_samples_by_taxa(taxa_id, start,
                                                                        count,
                                                                        studies=studies, user=user,
                                                                        auths=original_sample_controller.token_info(token_info))


def merge_original_samples(into, merged, user=None, token_info=None):  # noqa: E501
    """merges two OriginalSamples

    merges original samples with compatible properties updating references and merging sampling events # noqa: E501

    :param into: name of property to search
    :type into: str
    :param merged: matching value of property to search
    :type merged: str

    :rtype: OriginalSample
    """
    return original_sample_controller.merge_original_samples(into, merged,
                                                             auths=original_sample_controller.token_info(token_info))


def update_original_sample(original_sample_id, body, studies=None, user=None, token_info=None):
    """
    updates an originalSample

    :param originalSampleId: ID of originalSample to update
    :type originalSampleId: str
    :param originalSample:
    :type originalSample: dict | bytes

    :rtype: OriginalSample
    """
    if connexion.request.is_json:
        original_sample = OriginalSample.from_dict(
            connexion.request.get_json())
    return original_sample_controller.update_original_sample(original_sample_id,
                                                             original_sample,
                                                             studies=studies, user=user,
                                                             auths=original_sample_controller.token_info(token_info))
