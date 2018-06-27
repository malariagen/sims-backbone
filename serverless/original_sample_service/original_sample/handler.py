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

from swagger_server.models.original_sample import OriginalSample

import logging

import datetime

from backbone_server.controllers.original_sample_controller import OriginalSampleController

from util.response_util import create_response

original_sample_controller = OriginalSampleController()

def create_original_sample(event, context):

    user = event['requestContext']['authorizer']['principalId']

    original_sample = OriginalSample.from_dict(json.loads(event["body"]))

    value, retcode = original_sample_controller.create_original_sample(original_sample, user,
                                                                       original_sample_controller.authorizer(event['requestContext']['authorizer']))

    return create_response(event, retcode, value)


def delete_original_sample(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        original_sample_id = event["pathParameters"]["original_sample_id"]

    value, retcode =  original_sample_controller.delete_original_sample(original_sample_id, user,
                                                                        original_sample_controller.authorizer(event['requestContext']['authorizer']))

    return create_response(event, retcode, value)


def download_original_sample(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        original_sample_id = event["pathParameters"]["original_sample_id"]

    value, retcode =  original_sample_controller.download_original_sample(original_sample_id, user,
                                                                          original_sample_controller.authorizer(event['requestContext']['authorizer']))

    return create_response(event, retcode, value)


def download_original_samples(event, context):

    user = event['requestContext']['authorizer']['principalId']

    start =  None
    count =  None
    search_filter = None

    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'start' in event["queryStringParameters"]:
            start = int(event["queryStringParameters"]["start"])
        if 'count' in event["queryStringParameters"]:
            count = int(event["queryStringParameters"]["count"])
        if 'filter' in event['queryStringParameters']:
            search_filter = event["queryStringParameters"]["filter"]

    value, retcode = original_sample_controller.download_original_samples(search_filter, start,
                                                                          count, user,
                                                                          original_sample_controller.authorizer(event['requestContext']['authorizer']))

    return create_response(event, retcode, value)

def download_original_samples_by_attr(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        prop_name = event["pathParameters"]["prop_name"]
        prop_value = event["pathParameters"]["prop_value"]

    study_name = None
    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'study_name' in event["queryStringParameters"]:
            study_name = event["queryStringParameters"]["study_name"]

    value, retcode = original_sample_controller.download_original_samples_by_attr(prop_name,
                                                                                  prop_value,
                                                                                  study_name,
                                                                                  user,
                                                                                  original_sample_controller.authorizer(event['requestContext']['authorizer']))


    return create_response(event, retcode, value)

def download_original_samples_by_os_attr(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        prop_name = event["pathParameters"]["prop_name"]
        prop_value = event["pathParameters"]["prop_value"]

    study_name = None
    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'study_name' in event["queryStringParameters"]:
            study_name = event["queryStringParameters"]["study_name"]

    value, retcode = original_sample_controller.download_original_samples_by_os_attr(prop_name,
                                                                                     prop_value,
                                                                                     study_name,
                                                                                     user,
                                                                                     original_sample_controller.authorizer(event['requestContext']['authorizer']))


    return create_response(event, retcode, value)

def download_original_samples_by_location(event, context):

    user = event['requestContext']['authorizer']['principalId']

    start =  None
    count =  None

    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'start' in event["queryStringParameters"]:
            start = int(event["queryStringParameters"]["start"])
        if 'count' in event["queryStringParameters"]:
            count = int(event["queryStringParameters"]["count"])

    if 'pathParameters' in event:
        location_id = event["pathParameters"]["location_id"]

    value, retcode = original_sample_controller.download_original_samples_by_location(location_id,
                                                                                      start, count,
                                                                                      user,
                                                                                      original_sample_controller.authorizer(event['requestContext']['authorizer']))

    return create_response(event, retcode, value)


def download_original_samples_by_study(event, context):

    user = event['requestContext']['authorizer']['principalId']

    start =  None
    count =  None

    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'start' in event["queryStringParameters"]:
            start = int(event["queryStringParameters"]["start"])
        if 'count' in event["queryStringParameters"]:
            count = int(event["queryStringParameters"]["count"])

    if 'pathParameters' in event:
        study_name = event["pathParameters"]["study_name"]

    value, retcode = original_sample_controller.download_original_samples_by_study(study_name, start,
                                                                                   count, user,
                                                                                   original_sample_controller.authorizer(event['requestContext']['authorizer']))

    return create_response(event, retcode, value)

def download_original_samples_by_taxa(event, context):

    user = event['requestContext']['authorizer']['principalId']

    start =  None
    count =  None

    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'start' in event["queryStringParameters"]:
            start = int(event["queryStringParameters"]["start"])
        if 'count' in event["queryStringParameters"]:
            count = int(event["queryStringParameters"]["count"])

    if 'pathParameters' in event:
        taxa_id = event["pathParameters"]["taxa_id"]

    value, retcode = original_sample_controller.download_original_samples_by_taxa(taxa_id, start,
                                                                                  count, user,
                                                                                  original_sample_controller.authorizer(event['requestContext']['authorizer']))

    return create_response(event, retcode, value)

def download_original_samples_by_event_set(event, context):

    user = event['requestContext']['authorizer']['principalId']

    start =  None
    count =  None

    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'start' in event["queryStringParameters"]:
            start = int(event["queryStringParameters"]["start"])
        if 'count' in event["queryStringParameters"]:
            count = int(event["queryStringParameters"]["count"])

    if 'pathParameters' in event:
        event_set_id = event["pathParameters"]["event_set_id"]

    value, retcode = original_sample_controller.download_original_samples_by_event_set(event_set_id,
                                                                                       start, count,
                                                                                       user,
                                                                                       original_sample_controller.authorizer(event['requestContext']['authorizer']))

    return create_response(event, retcode, value)

def update_original_sample(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        original_sample_id = event["pathParameters"]["original_sample_id"]

    original_sample = OriginalSample.from_dict(json.loads(event["body"]))

    value, retcode = original_sample_controller.update_location(original_sample_id, original_sample,
                                                                user,
                                                                original_sample_controller.authorizer(event['requestContext']['authorizer']))

    return create_response(event, retcode, value)


def merge_original_samples(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        into = event["pathParameters"]["into"]
        merged = event["pathParameters"]["merged"]

    value, retcode = original_sample_controller.merge_original_samples(into,
                                                                       merged,
                                                                       user,
                                                                       original_sample_controller.authorizer(event['requestContext']['authorizer']))


    return create_response(event, retcode, value)

