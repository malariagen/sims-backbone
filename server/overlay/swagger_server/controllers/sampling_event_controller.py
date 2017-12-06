import connexion
from swagger_server.models.sampling_event import SamplingEvent
from swagger_server.models.sampling_events import SamplingEvents
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

import logging


from backbone_server.controllers.sampling_event_controller  import SamplingEventController

sampling_event_controller = SamplingEventController()

def create_sampling_event(samplingEvent, user = None, token_info = None):
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

def delete_sampling_event(samplingEventId, user = None, token_info = None):
    """
    deletes an samplingEvent
    
    :param samplingEventId: ID of samplingEvent to fetch
    :type samplingEventId: str

    :rtype: None
    """
    return sampling_event_controller.delete_sampling_event(samplingEventId, user,
                                                           sampling_event_controller.token_info(token_info))


def download_sampling_event(samplingEventId, user = None, token_info = None):
    """
    fetches an samplingEvent
    
    :param samplingEventId: ID of samplingEvent to fetch
    :type samplingEventId: str

    :rtype: SamplingEvent
    """
    return sampling_event_controller.download_sampling_event(samplingEventId, user,
                                                             sampling_event_controller.token_info(token_info))


def download_sampling_event_by_identifier(propName, propValue, user = None, token_info = None):
    """
    fetches a samplingEvent by property value
    
    :param propName: name of property to search
    :type propName: str
    :param propValue: matching value of property to search
    :type propValue: str

    :rtype: SamplingEvent
    """
    return sampling_event_controller.download_sampling_event_by_identifier(propName, propValue,
                                                                           user,
                                                                           sampling_event_controller.token_info(token_info))

def download_sampling_events_by_event_set(eventSetId, user = None, token_info = None):
    """
    fetches samplingEvents in a given event set
    
    :param eventSetId: Event Set name
    :type eventSetId: str

    :rtype: SamplingEvents
    """
    return sampling_event_controller.download_sampling_events_by_event_set(eventSetId, user,
                                                                       sampling_event_controller.token_info(token_info))

def download_sampling_events_by_location(locationId, user = None, token_info = None):
    """
    fetches samplingEvents for a location
    
    :param locationId: location
    :type locationId: str

    :rtype: SamplingEvents
    """
    return sampling_event_controller.download_sampling_events_by_location(locationId, user,
                                                                          sampling_event_controller.token_info(token_info))

def download_sampling_events_by_study(studyName, user = None, token_info = None):
    """
    fetches samplingEvents for a study
    
    :param studyName: 4 digit study code
    :type studyName: str

    :rtype: SamplingEvents
    """
    return sampling_event_controller.download_sampling_events_by_study(studyName, user,
                                                                       sampling_event_controller.token_info(token_info))

def download_sampling_events_by_taxa(taxaId, user = None, token_info = None):
    """
    fetches samplingEvents for a given taxonomy classification code
    
    :param taxaId: NCBI taxonomy code
    :type taxaId: str

    :rtype: SamplingEvents
    """
    return sampling_event_controller.download_sampling_events_by_taxa(taxaId, user,
                                                                       sampling_event_controller.token_info(token_info))


def update_sampling_event(samplingEventId, samplingEvent, user = None, token_info = None):
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

