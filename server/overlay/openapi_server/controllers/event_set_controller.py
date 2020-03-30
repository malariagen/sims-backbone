import connexion
from openapi_server.models.event_set import EventSet
from openapi_server.models.event_set_note import EventSetNote
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

import logging

from backbone_server.controllers.event_set_controller import EventSetController

event_set_controller = EventSetController()


def create_event_set(event_set_id, studies=None, user=None, token_info=None):
    """
    creates an eventSet

    :param eventSetId: ID of eventSet to create
    :type eventSetId: str
    :param eventSet:
    :type eventSet: dict | bytes

    :rtype: EventSet
    """

    return event_set_controller.create_event_set(event_set_id, studies=studies, user=user,
                                                 auths=event_set_controller.token_info(token_info))


def create_event_set_item(event_set_id, sampling_event_id, studies=None, user=None, token_info=None):
    """
    Adds a samplingEvent to an eventSet

    :param eventSetId: ID of eventSet to modify
    :type eventSetId: str
    :param samplingEventId: ID of samplingEvent to add to the set
    :type samplingEventId: str

    :rtype: EventSet
    """
    (ret, retcode) = event_set_controller.create_event_set_item(event_set_id, sampling_event_id, studies=studies, user=user,
                                                                auths=event_set_controller.token_info(token_info))
    return ret, retcode


def create_event_set_note(event_set_id, note_id, body, studies=None, user=None, token_info=None):
    """
    Adds a note to an eventSet

    :param eventSetId: ID of eventSet to modify
    :type eventSetId: str
    :param noteId: ID of note to modify in the set
    :type noteId: str
    :param note:
    :type note: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        note = EventSetNote.from_dict(connexion.request.get_json())
    return event_set_controller.create_event_set_note(event_set_id, note_id, note, studies=studies, user=user,
                                                      auths=event_set_controller.token_info(token_info))


def delete_event_set(event_set_id, studies=None, user=None, token_info=None):
    """
    deletes an eventSet

    :param eventSetId: ID of eventSet to delete
    :type eventSetId: str

    :rtype: None
    """
    return event_set_controller.delete_event_set(event_set_id, studies=studies, user=user, auths=event_set_controller.token_info(token_info))


def delete_event_set_item(event_set_id, sampling_event_id, studies=None, user=None, token_info=None):
    """
    deletes a samplingEvent from an eventSet

    :param eventSetId: ID of eventSet to modify
    :type eventSetId: str
    :param samplingEventId: ID of samplingEvent to remove from the set
    :type samplingEventId: str

    :rtype: None
    """
    return event_set_controller.delete_event_set_item(event_set_id, sampling_event_id, studies=studies, user=user,
                                                      auths=event_set_controller.token_info(token_info))


def delete_event_set_note(event_set_id, note_id, studies=None, user=None, token_info=None):
    """
    deletes an eventSet note

    :param eventSetId: ID of eventSet to modify
    :type eventSetId: str
    :param noteId: ID of note to remove from the set
    :type noteId: str

    :rtype: None
    """
    return event_set_controller.delete_event_set_note(event_set_id, note_id, studies=studies, user=user,
                                                      auths=event_set_controller.token_info(token_info))


def download_event_set(event_set_id, start=None, count=None,
                       studies=None, user=None, token_info=None):
    """
    fetches an eventSet

    :param eventSetId: ID of eventSet to fetch
    :type eventSetId: str

    :rtype: EventSet
    """
    return event_set_controller.download_event_set(event_set_id,
                                                   start=start, count=count,
                                                   studies=studies,
                                                   user=user,
                                                   auths=event_set_controller.token_info(token_info))


def download_event_sets(studies=None, user=None, token_info=None):
    """
    fetches eventSets


    :rtype: EventSets
    """
    return event_set_controller.download_event_sets(studies=studies, user=user,
                                                    auths=event_set_controller.token_info(token_info))


def update_event_set(event_set_id, body, studies=None, user=None, token_info=None):
    """
    updates an eventSet

    :param eventSetId: ID of eventSet to update
    :type eventSetId: str
    :param eventSet:
    :type eventSet: dict | bytes

    :rtype: EventSet
    """
    if connexion.request.is_json:
        event_set = EventSet.from_dict(connexion.request.get_json())
    return event_set_controller.update_event_set(event_set_id, event_set, studies=studies, user=user,
                                                 auths=event_set_controller.token_info(token_info))


def update_event_set_note(event_set_id, note_id, body, studies=None, user=None, token_info=None):
    """
    Adds a note to an eventSet

    :param eventSetId: ID of eventSet to modify
    :type eventSetId: str
    :param noteId: ID of note to modify in the set
    :type noteId: str
    :param note:
    :type note: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        note = EventSetNote.from_dict(connexion.request.get_json())

    return event_set_controller.update_event_set_note(event_set_id, note_id, note, studies=studies, user=user,
                                                      auths=event_set_controller.token_info(token_info))
