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

from swagger_server.models.sampling_event import SamplingEvent

import logging

import datetime

from backbone_server.controllers.sampling_event_controller import SamplingEventController

sampling_event_controller = SamplingEventController()

def create_response(retcode, value):

    return {
        "statusCode": retcode,
        "headers": {
            "Access-Control-Allow-Origin" : "*"
        },
        "body": json.dumps(value.to_dict())
    }

def prepare_for_serialization(sampling_event):
    sampling_event.sampling_event_id = str(sampling_event.sampling_event_id)
    sampling_event.doc = sampling_event.doc.strftime('%Y-%m-%d')
    if sampling_event.location_id:
        sampling_event.location_id = str(sampling_event.location_id)
        sampling_event.location.location_id = str(sampling_event.location.location_id)
    if sampling_event.proxy_location_id:
        sampling_event.proxy_location_id = str(sampling_event.proxy_location_id)
        sampling_event.proxy_location.location_id = str(sampling_event.proxy_location.location_id)


def create_sampling_event(event, context):

    user = event['requestContext']['authorizer']['principalId']

    sampling_event = SamplingEvent.from_dict(json.loads(event["body"]))

    value, retcode = sampling_event_controller.create_sampling_event(sampling_event, user)

    return create_response(retcode, value)


def delete_sampling_event(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        sampling_event_id = event["pathParameters"]["sampling_event_id"]

    value, retcode =  sampling_event_controller.delete_sampling_event(sampling_event_id, user)

    return create_response(retcode, value)


def download_sampling_event(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        sampling_event_id = event["pathParameters"]["sampling_event_id"]

    value, retcode =  sampling_event_controller.download_sampling_event(sampling_event_id, user)

    prepare_for_serialization(value)

    return create_response(retcode, value)

def download_sampling_event_by_identifier(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        prop_name = event["pathParameters"]["prop_name"]
        prop_value = event["pathParameters"]["prop_value"]

    value, retcode = sampling_event_controller.download_sampling_event_by_identifier(prop_name, prop_value, user)

    prepare_for_serialization(value)

    return create_response(retcode, value)

def download_sampling_events_by_location(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        location_id = event["pathParameters"]["location_id"]

    value, retcode = sampling_event_controller.download_sampling_events_by_location(location_id, user)

    for se in value.sampling_events:
        prepare_for_serialization(se)

    return create_response(retcode, value)


def download_sampling_events_by_study(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        study_name = event["pathParameters"]["study_name"]

    value, retcode = sampling_event_controller.download_sampling_events_by_study(study_name, user)

    for se in value.sampling_events:
        prepare_for_serialization(se)

    return create_response(retcode, value)

def update_sampling_event(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        sampling_event_id = event["pathParameters"]["sampling_event_id"]

    sampling_event = SamplingEvent.from_dict(json.loads(event["body"]))

    value, retcode = sampling_event_controller.update_location(sampling_event_id, sampling_event, user)

    prepare_for_serialization(value)

    return create_response(retcode, value)

