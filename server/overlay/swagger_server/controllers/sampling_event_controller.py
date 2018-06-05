import connexion
import six

from swagger_server.models.sampling_event import SamplingEvent  # noqa: E501
from swagger_server.models.sampling_events import SamplingEvents  # noqa: E501
from swagger_server import util

import logging

from backbone_server.controllers.sampling_event_controller  import SamplingEventController

sampling_event_controller = SamplingEventController()

def create_sampling_event(samplingEvent, user=None, token_info=None):
    """
    create_sampling_event
    Create a samplingEvent
    :param samplingEvent: 
    :type samplingEvent: dict | bytes

    :rtype: SamplingEvent
    """
    if connexion.request.is_json:
        samplingEvent = SamplingEvent.from_dict(connexion.request.get_json())

    return sampling_event_controller.create_sampling_event(samplingEvent, user,
                                                           sampling_event_controller.token_info(token_info))

def delete_sampling_event(samplingEventId, user=None, token_info=None):
    """
    deletes an samplingEvent
    
    :param samplingEventId: ID of samplingEvent to fetch
    :type samplingEventId: str

    :rtype: None
    """
    return sampling_event_controller.delete_sampling_event(samplingEventId, user,
                                                           sampling_event_controller.token_info(token_info))


def download_sampling_event(samplingEventId, user=None, token_info=None):
    """
    fetches an samplingEvent
    
    :param samplingEventId: ID of samplingEvent to fetch
    :type samplingEventId: str

    :rtype: SamplingEvent
    """
    return sampling_event_controller.download_sampling_event(samplingEventId, user,
                                                             sampling_event_controller.token_info(token_info))


def download_sampling_events(filter=None, start=None, count=None, user=None, token_info=None):  # noqa: E501
    """fetches samplingEvents

     # noqa: E501

    :param filter: search filter e.g. studyId:0000, attr:name:value, location:locationId, taxa:taxId, eventSet:setName
    :type filter: str
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int

    :rtype: SamplingEvents
    """
    return sampling_event_controller.download_sampling_events(filter, start,
                                                              count, user,
                                                              sampling_event_controller.token_info(token_info))

def download_sampling_events_by_event_set(eventSetId, start=None, count=None, user=None, token_info=None):
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
    return sampling_event_controller.download_sampling_events_by_event_set(eventSetId,start,
                                                                           count, user,
                                                                       sampling_event_controller.token_info(token_info))

def download_sampling_events_by_attr(propName, propValue, studyName=None, user=None, token_info=None):
    """
    fetches a samplingEvent by property value
    
    :param propName: name of property to search
    :type propName: str
    :param propValue: matching value of property to search
    :type propValue: str

    :rtype: SamplingEvent
    """
    return sampling_event_controller.download_sampling_events_by_attr(propName, propValue,
                                                                           studyName,
                                                                           user,
                                                                           sampling_event_controller.token_info(token_info))

def download_sampling_events_by_location(locationId, start=None, count=None, user=None, token_info=None):
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
    return sampling_event_controller.download_sampling_events_by_location(locationId, start,
                                                                          count, user,
                                                                          sampling_event_controller.token_info(token_info))

def download_sampling_events_by_study(studyName, start=None, count=None, user=None, token_info=None):
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
    return sampling_event_controller.download_sampling_events_by_study(studyName, start,
                                                                       count, user,
                                                                       sampling_event_controller.token_info(token_info))

def download_sampling_events_by_taxa(taxaId, start=None, count=None, user=None, token_info=None):
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
    return sampling_event_controller.download_sampling_events_by_taxa(taxaId, start,
                                                                      count, user,
                                                                       sampling_event_controller.token_info(token_info))


def update_sampling_event(samplingEventId, samplingEvent, user=None, token_info=None):
    """
    updates an samplingEvent
    
    :param samplingEventId: ID of samplingEvent to update
    :type samplingEventId: str
    :param samplingEvent: 
    :type samplingEvent: dict | bytes

    :rtype: SamplingEvent
    """
    if connexion.request.is_json:
        samplingEvent = SamplingEvent.from_dict(connexion.request.get_json())
    return sampling_event_controller.update_sampling_event(samplingEventId, samplingEvent, user,
                                                           sampling_event_controller.token_info(token_info))

