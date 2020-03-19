import connexion

from openapi_server.models.sampling_event import SamplingEvent  # noqa: E501
from openapi_server.models.sampling_events import SamplingEvents  # noqa: E501
from openapi_server import util

import logging

from backbone_server.controllers.sampling_event_controller import SamplingEventController

sampling_event_controller = SamplingEventController()


def create_sampling_event(body, user=None, token_info=None):
    """
    create_sampling_event
    Create a samplingEvent
    :param samplingEvent:
    :type samplingEvent: dict | bytes

    :rtype: SamplingEvent
    """
    if connexion.request.is_json:
        sampling_event = SamplingEvent.from_dict(connexion.request.get_json())

    return sampling_event_controller.create_sampling_event(sampling_event, studies=None, user=user,
                                                           auths=sampling_event_controller.token_info(token_info))


def delete_sampling_event(sampling_event_id, user=None, token_info=None):
    """
    deletes an samplingEvent

    :param samplingEventId: ID of samplingEvent to fetch
    :type samplingEventId: str

    :rtype: None
    """
    return sampling_event_controller.delete_sampling_event(sampling_event_id, studies=None, user=user,
                                                           auths=sampling_event_controller.token_info(token_info))


def download_sampling_event(sampling_event_id, user=None, token_info=None):
    """
    fetches an samplingEvent

    :param samplingEventId: ID of samplingEvent to fetch
    :type samplingEventId: str

    :rtype: SamplingEvent
    """
    return sampling_event_controller.download_sampling_event(sampling_event_id, studies=None, user=user,
                                                             auths=sampling_event_controller.token_info(token_info))


def download_sampling_events(search_filter=None, start=None,
                             count=None, value_type=None, studies=None, user=None, token_info=None):  # noqa: E501
    """fetches samplingEvents

     # noqa: E501

    :param search_filter: search filter e.g. studyId:0000, attr:name:value, location:locationId, taxa:taxId, eventSet:setName
    :type search_filter: str
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int

    :rtype: SamplingEvents
    """
    return sampling_event_controller.download_sampling_events(search_filter,
                                                              start=start,
                                                              count=count,
                                                              value_type=value_type,
                                                              studies=studies, user=user,
                                                              auths=sampling_event_controller.token_info(token_info))


def download_sampling_events_by_event_set(event_set_id, start=None, count=None, user=None, token_info=None):
    """
    fetches samplingEvents in a given event set

    :param eventSetId: Event Set name
    :type eventSetId: str
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int

    :rtype: SamplingEvents
    """
    return sampling_event_controller.download_sampling_events_by_event_set(event_set_id,
                                                                           start=start,
                                                                           count=count, studies=None, user=user,
                                                                           auths=sampling_event_controller.token_info(token_info))


def download_sampling_events_by_attr(prop_name, prop_value, study_name=None,
                                     start=None, count=None, value_type=None, user=None, token_info=None):
    """
    fetches a samplingEvent by property value

    :param propName: name of property to search
    :type propName: str
    :param propValue: matching value of property to search
    :type propValue: str

    :rtype: SamplingEvent
    """
    return sampling_event_controller.download_sampling_events_by_attr(prop_name, prop_value,
                                                                      study_name,
                                                                      start=start,
                                                                      count=count,
                                                                      value_type=value_type,
                                                                      studies=studies, user=user,
                                                                      auths=sampling_event_controller.token_info(token_info))


def download_sampling_events_by_os_attr(prop_name, prop_value, study_name=None,
                                        start=None, count=None,
                                        value_type=None, user=None, token_info=None):
    """
    fetches a samplingEvent by property value of associated original sample

    :param propName: name of property to search
    :type propName: str
    :param propValue: matching value of property to search
    :type propValue: str

    :rtype: SamplingEvent
    """
    return sampling_event_controller.download_sampling_events_by_os_attr(prop_name, prop_value,
                                                                         study_name,
                                                                         start=start,
                                                                         count=count,
                                                                         value_type=value_type,
                                                                         studies=studies, user=user,
                                                                         auths=sampling_event_controller.token_info(token_info))


def download_sampling_events_by_location(location_id, start=None, count=None, user=None, token_info=None):
    """
    fetches samplingEvents for a location

    :param locationId: location
    :type locationId: str
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int

    :rtype: SamplingEvents
    """
    return sampling_event_controller.download_sampling_events_by_location(location_id,
                                                                          start=start,
                                                                          count=count, studies=None, user=user,
                                                                          auths=sampling_event_controller.token_info(token_info))


def download_sampling_events_by_study(study_name, start=None, count=None, user=None, token_info=None):
    """
    fetches samplingEvents for a study

    :param studyName: 4 digit study code
    :type studyName: str
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int

    :rtype: SamplingEvents
    """
    return sampling_event_controller.download_sampling_events_by_study(study_name, start=start,
                                                                       count=count, studies=None, user=user,
                                                                       auths=sampling_event_controller.token_info(token_info))


def download_sampling_events_by_taxa(taxa_id, start=None, count=None,
                                     studies=None, user=None, token_info=None):
    """
    fetches samplingEvents for a given taxonomy classification code

    :param taxaId: NCBI taxonomy code
    :type taxaId: str
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int

    :rtype: SamplingEvents
    """
    return sampling_event_controller.download_sampling_events_by_taxa(taxa_id,
                                                                      start=start,
                                                                      count=count,
                                                                      studies=studies, user=user,
                                                                      auths=sampling_event_controller.token_info(token_info))


def merge_sampling_events(into, merged, user=None, token_info=None):  # noqa: E501
    """merges two samplingEvents

    merges sampling events with compatible properties updating references # noqa: E501

    :param into: name of property to search
    :type into: str
    :param merged: matching value of property to search
    :type merged: str

    :rtype: SamplingEvent
    """
    return sampling_event_controller.merge_sampling_events(into, merged,
                                                           studies=None,
                                                           user=user,
                                                           auths=sampling_event_controller.token_info(token_info))


def update_sampling_event(sampling_event_id, body, user=None, token_info=None):
    """
    updates an samplingEvent

    :param samplingEventId: ID of samplingEvent to update
    :type samplingEventId: str
    :param samplingEvent:
    :type samplingEvent: dict | bytes

    :rtype: SamplingEvent
    """
    if connexion.request.is_json:
        sampling_event = SamplingEvent.from_dict(connexion.request.get_json())
    return sampling_event_controller.update_sampling_event(sampling_event_id, sampling_event, studies=None, user=user,
                                                           auths=sampling_event_controller.token_info(token_info))
