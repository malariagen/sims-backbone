import json
import os, sys, inspect
currentframe = os.path.split(inspect.getfile(inspect.currentframe()))[0]
paths = os.getenv('PYTHON_PATH').split(':')

for include_path in paths:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(currentframe,include_path)))
    if cmd_subfolder not in sys.path:
         sys.path.insert(0, cmd_subfolder)

from util.response_util import create_response
from util.request_util import get_body,get_user,get_auths

from openapi_server.models.event_set import EventSet
from openapi_server.models.event_set_note import EventSetNote

from backbone_server.controllers.event_set_controller import EventSetController

event_set_controller = EventSetController()

def create_event_set(event, context):
    """
    creates an eventSet

    :param eventSetId: ID of eventSet to create
    :type eventSetId: str
    :param eventSet:
    :type eventSet: dict | bytes

    :rtype: EventSet
    """
    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(event_set_controller, event)

    if 'pathParameters' in event:
        event_set_id = event["pathParameters"]["event_set_id"]

    value, retcode = event_set_controller.create_event_set(event_set_id, user, auths)

    return create_response(event, retcode, value)


def create_event_set_item(event, context):
    """
    Adds a samplingEvent to an eventSet

    :param eventSetId: ID of eventSet to modify
    :type eventSetId: str
    :param samplingEventId: ID of samplingEvent to add to the set
    :type samplingEventId: str

    :rtype: EventSet
    """

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(event_set_controller, event)

    if 'pathParameters' in event:
        event_set_id = event["pathParameters"]["event_set_id"]
        sampling_event_id = event["pathParameters"]["sampling_event_id"]

    (value, retcode) = event_set_controller.create_event_set_item(event_set_id, sampling_event_id,
                                                                  user, auths)

    return create_response(event, retcode, value)


def create_event_set_note(event, context):
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

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(event_set_controller, event)

    if 'pathParameters' in event:
        event_set_id = event["pathParameters"]["event_set_id"]
        note_id = event["pathParameters"]["note_id"]

    note = EventSetNote.from_dict(json.loads(event["body"]))

    value, retcode = event_set_controller.create_event_set_note(event_set_id, note_id, note, user,
                                                                auths)

    return create_response(event, retcode, value)

def delete_event_set(event, context):
    """
    deletes an eventSet

    :param eventSetId: ID of eventSet to delete
    :type eventSetId: str

    :rtype: None
    """

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(event_set_controller, event)

    if 'pathParameters' in event:
        event_set_id = event["pathParameters"]["event_set_id"]

    value, retcode = event_set_controller.delete_event_set(event_set_id, user, auths)

    return create_response(event, retcode, value)

def delete_event_set_item(event, context):
    """
    deletes a samplingEvent from an eventSet

    :param eventSetId: ID of eventSet to modify
    :type eventSetId: str
    :param samplingEventId: ID of samplingEvent to remove from the set
    :type samplingEventId: str

    :rtype: None
    """

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(event_set_controller, event)

    if 'pathParameters' in event:
        event_set_id = event["pathParameters"]["event_set_id"]
        sampling_event_id = event["pathParameters"]["sampling_event_id"]

    value, retcode = event_set_controller.delete_event_set_item(event_set_id, sampling_event_id,
                                                                user, auths)

    return create_response(event, retcode, value)

def delete_event_set_note(event, context):
    """
    deletes an eventSet note

    :param eventSetId: ID of eventSet to modify
    :type eventSetId: str
    :param noteId: ID of note to remove from the set
    :type noteId: str

    :rtype: None
    """

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(event_set_controller, event)

    if 'pathParameters' in event:
        event_set_id = event["pathParameters"]["event_set_id"]
        note_id = event["pathParameters"]["note_id"]

    value, retcode = event_set_controller.delete_event_set_note(event_set_id, note_id, user, auths)

    return create_response(event, retcode, value)

def download_event_set(event, context):
    """
    fetches an eventSet

    :param eventSetId: ID of eventSet to fetch
    :type eventSetId: str

    :rtype: EventSet
    """

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(event_set_controller, event)

    start =  None
    count =  None

    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'start' in event["queryStringParameters"]:
            start = int(event["queryStringParameters"]["start"])
        if 'count' in event["queryStringParameters"]:
            count = int(event["queryStringParameters"]["count"])

    if 'pathParameters' in event:
        event_set_id = event["pathParameters"]["event_set_id"]

    value, retcode = event_set_controller.download_event_set(event_set_id, start, count, user,
                                                             auths)

    return create_response(event, retcode, value)

def download_event_sets(event, context):
    """
    fetches eventSets


    :rtype: EventSets
    """

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(event_set_controller, event)

    value, retcode = event_set_controller.download_event_sets(user, auths)

    return create_response(event, retcode, value)

def update_event_set(event, context):
    """
    updates an eventSet

    :param eventSetId: ID of eventSet to update
    :type eventSetId: str
    :param eventSet:
    :type eventSet: dict | bytes

    :rtype: EventSet
    """

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(event_set_controller, event)

    if 'pathParameters' in event:
        event_set_id = event["pathParameters"]["event_set_id"]

    event_set = EventSet.from_dict(json.loads(event["body"]))

    value, retcode = event_set_controller.update_event_set(event_set_id, event_set, user, auths)

    return create_response(event, retcode, value)

def update_event_set_note(event, context):
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

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(event_set_controller, event)

    if 'pathParameters' in event:
        event_set_id = event["pathParameters"]["event_set_id"]
        note_id = event["pathParameters"]["note_id"]

    note = EventSetNote.from_dict(json.loads(event["body"]))

    value, retcode = event_set_controller.update_event_set_note(event_set_id, note_id, note, user,
                                                                auths)

    return create_response(event, retcode, value)
