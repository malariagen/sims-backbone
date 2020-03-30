import json
import os, sys, inspect
# realpath() will make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
     sys.path.insert(0, cmd_folder)

# Use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0],"../server")))
if cmd_subfolder not in sys.path:
     sys.path.insert(0, cmd_subfolder)

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0],"../server/bb_server")))
if cmd_subfolder not in sys.path:
     sys.path.insert(0, cmd_subfolder)

from openapi_server.models.sampling_event import SamplingEvent

import logging

import datetime

from backbone_server.controllers.sampling_event_controller import SamplingEventController

from util.response_util import create_response
from util.request_util import get_body, get_user, get_auths

sampling_event_controller = SamplingEventController()

def create_sampling_event(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(sampling_event_controller, event)

    sampling_event = SamplingEvent.from_dict(get_body(event))

    value, retcode = sampling_event_controller.create_sampling_event(sampling_event, user=user,
                                                                     auths=auths)

    return create_response(event, retcode, value)


def delete_sampling_event(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(sampling_event_controller, event)

    if 'pathParameters' in event:
        sampling_event_id = event["pathParameters"]["sampling_event_id"]

    value, retcode = sampling_event_controller.delete_sampling_event(sampling_event_id, user=user,
                                                                      auths=auths)

    return create_response(event, retcode, value)


def download_sampling_event(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(sampling_event_controller, event)

    if 'pathParameters' in event:
        sampling_event_id = event["pathParameters"]["sampling_event_id"]

    value, retcode = sampling_event_controller.download_sampling_event(sampling_event_id, user=user,
                                                                        auths=auths)

    return create_response(event, retcode, value)


def download_sampling_events(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(sampling_event_controller, event)

    start = None
    count = None
    search_filter = None
    value_type = None

    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'start' in event["queryStringParameters"]:
            start = int(event["queryStringParameters"]["start"])
        if 'count' in event["queryStringParameters"]:
            count = int(event["queryStringParameters"]["count"])
        if 'search_filter' in event['queryStringParameters']:
            search_filter = event["queryStringParameters"]["search_filter"]
        if 'value_type' in event["queryStringParameters"]:
            value_type = event["queryStringParameters"]["value_type"]

    value, retcode = sampling_event_controller.download_sampling_events(search_filter,
                                                                        value_type=value_type,
                                                                        start=start,
                                                                        count=count,
                                                                        user=user,
                                                                        auths=auths)

    return create_response(event, retcode, value)

def download_sampling_events_by_attr(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(sampling_event_controller, event)

    if 'pathParameters' in event:
        prop_name = event["pathParameters"]["prop_name"]
        prop_value = event["pathParameters"]["prop_value"]

    study_name = None
    start = None
    count = None
    value_type = None
    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'study_name' in event["queryStringParameters"]:
            study_name = event["queryStringParameters"]["study_name"]
        if 'start' in event["queryStringParameters"]:
            start = event["queryStringParameters"]["start"]
        if 'count' in event["queryStringParameters"]:
            count = event["queryStringParameters"]["count"]
        if 'value_type' in event["queryStringParameters"]:
            value_type = event["queryStringParameters"]["value_type"]

    value, retcode = sampling_event_controller.download_sampling_events_by_attr(prop_name,
                                                                                prop_value,
                                                                                study_name,
                                                                                value_type=value_type,
                                                                                start=start,
                                                                                count=count,
                                                                                user=user,
                                                                                auths=auths)


    return create_response(event, retcode, value)

def download_sampling_events_by_os_attr(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(sampling_event_controller, event)

    if 'pathParameters' in event:
        prop_name = event["pathParameters"]["prop_name"]
        prop_value = event["pathParameters"]["prop_value"]

    study_name = None
    start = None
    count = None
    value_type = None
    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'study_name' in event["queryStringParameters"]:
            study_name = event["queryStringParameters"]["study_name"]
        if 'start' in event["queryStringParameters"]:
            start = event["queryStringParameters"]["start"]
        if 'count' in event["queryStringParameters"]:
            count = event["queryStringParameters"]["count"]
        if 'value_type' in event["queryStringParameters"]:
            value_type = event["queryStringParameters"]["value_type"]

    value, retcode = sampling_event_controller.download_sampling_events_by_os_attr(prop_name,
                                                                                   prop_value,
                                                                                   study_name,
                                                                                   value_type=value_type,
                                                                                   start=start,
                                                                                   count=count,
                                                                                   user=user,
                                                                                   auths=auths)


    return create_response(event, retcode, value)

def download_sampling_events_by_location(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(sampling_event_controller, event)

    start = None
    count = None

    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'start' in event["queryStringParameters"]:
            start = int(event["queryStringParameters"]["start"])
        if 'count' in event["queryStringParameters"]:
            count = int(event["queryStringParameters"]["count"])

    if 'pathParameters' in event:
        location_id = event["pathParameters"]["location_id"]

    value, retcode = sampling_event_controller.download_sampling_events_by_location(location_id,
                                                                                    start, count,
                                                                                    user=user,
                                                                                    auths=auths)

    return create_response(event, retcode, value)


def download_sampling_events_by_study(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(sampling_event_controller, event)

    start = None
    count = None

    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'start' in event["queryStringParameters"]:
            start = int(event["queryStringParameters"]["start"])
        if 'count' in event["queryStringParameters"]:
            count = int(event["queryStringParameters"]["count"])

    if 'pathParameters' in event:
        study_name = event["pathParameters"]["study_name"]

    value, retcode = sampling_event_controller.download_sampling_events_by_study(study_name, start,
                                                                                 count, user=user,
                                                                                 auths=auths)

    return create_response(event, retcode, value)

def download_sampling_events_by_taxa(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(sampling_event_controller, event)

    start = None
    count = None

    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'start' in event["queryStringParameters"]:
            start = int(event["queryStringParameters"]["start"])
        if 'count' in event["queryStringParameters"]:
            count = int(event["queryStringParameters"]["count"])

    if 'pathParameters' in event:
        taxa_id = event["pathParameters"]["taxa_id"]

    value, retcode = sampling_event_controller.download_sampling_events_by_taxa(taxa_id, start,
                                                                                count, user=user,
                                                                                auths=auths)

    return create_response(event, retcode, value)

def download_sampling_events_by_event_set(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(sampling_event_controller, event)

    start = None
    count = None

    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'start' in event["queryStringParameters"]:
            start = int(event["queryStringParameters"]["start"])
        if 'count' in event["queryStringParameters"]:
            count = int(event["queryStringParameters"]["count"])

    if 'pathParameters' in event:
        event_set_id = event["pathParameters"]["event_set_id"]

    value, retcode = sampling_event_controller.download_sampling_events_by_event_set(event_set_id,
                                                                                     start, count,
                                                                                     user=user,
                                                                                     auths=auths)

    return create_response(event, retcode, value)

def update_sampling_event(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(sampling_event_controller, event)

    if 'pathParameters' in event:
        sampling_event_id = event["pathParameters"]["sampling_event_id"]

    sampling_event = SamplingEvent.from_dict(get_body(event))

    value, retcode = sampling_event_controller.update_location(sampling_event_id, sampling_event,
                                                               user=user,
                                                               auths=auths)

    return create_response(event, retcode, value)


def merge_sampling_events(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(sampling_event_controller, event)

    if 'pathParameters' in event:
        into = event["pathParameters"]["into"]
        merged = event["pathParameters"]["merged"]

    value, retcode = sampling_event_controller.merge_sampling_events(into,
                                                                     merged,
                                                                     user=user,
                                                                     auths=auths)


    return create_response(event, retcode, value)
