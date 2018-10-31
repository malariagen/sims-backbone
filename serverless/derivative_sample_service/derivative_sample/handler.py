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

from swagger_server.models.derivative_sample import DerivativeSample

import logging

import datetime

from backbone_server.controllers.derivative_sample_controller import DerivativeSampleController

from util.response_util import create_response

derivative_sample_controller = DerivativeSampleController()

def create_derivative_sample(event, context):

    user = event['requestContext']['authorizer']['principalId']

    derivative_sample = DerivativeSample.from_dict(json.loads(event["body"]))

    value, retcode = derivative_sample_controller.create_derivative_sample(derivative_sample, user,
                                                                       derivative_sample_controller.authorizer(event['requestContext']['authorizer']))

    return create_response(event, retcode, value)


def delete_derivative_sample(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        derivative_sample_id = event["pathParameters"]["derivative_sample_id"]

    value, retcode =  derivative_sample_controller.delete_derivative_sample(derivative_sample_id, user,
                                                                        derivative_sample_controller.authorizer(event['requestContext']['authorizer']))

    return create_response(event, retcode, value)


def download_derivative_sample(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        derivative_sample_id = event["pathParameters"]["derivative_sample_id"]

    value, retcode =  derivative_sample_controller.download_derivative_sample(derivative_sample_id, user,
                                                                          derivative_sample_controller.authorizer(event['requestContext']['authorizer']))

    return create_response(event, retcode, value)

def download_derivative_samples(event, context):

    user = event['requestContext']['authorizer']['principalId']

    search_filter = None
    start = None
    count = None
    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'search_filter' in event["queryStringParameters"]:
            search_filter = event["queryStringParameters"]["search_filter"]
        if 'start' in event["queryStringParameters"]:
            start = event["queryStringParameters"]["start"]
        if 'count' in event["queryStringParameters"]:
            count = event["queryStringParameters"]["count"]

    value, retcode =  derivative_sample_controller.download_derivative_samples(search_filter,
                                                                               start, count,
                                                                               user,
                                                                               derivative_sample_controller.authorizer(event['requestContext']['authorizer']))

    return create_response(event, retcode, value)


def download_derivative_samples_by_taxa(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        taxa_id = event["pathParameters"]["taxaId"]
        prop_value = event["pathParameters"]["prop_value"]

    start = None
    count = None
    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'start' in event["queryStringParameters"]:
            start = event["queryStringParameters"]["start"]
        if 'count' in event["queryStringParameters"]:
            count = event["queryStringParameters"]["count"]

    value, retcode = derivative_sample_controller.download_derivative_samples_by_taxa(taxa_id,
                                                                                  start,
                                                                                  count,
                                                                                  user,
                                                                                  derivative_sample_controller.authorizer(event['requestContext']['authorizer']))


    return create_response(event, retcode, value)

def download_derivative_samples_by_attr(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        prop_name = event["pathParameters"]["prop_name"]
        prop_value = event["pathParameters"]["prop_value"]

    study_name = None
    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'study_name' in event["queryStringParameters"]:
            study_name = event["queryStringParameters"]["study_name"]

    value, retcode = derivative_sample_controller.download_derivative_samples_by_attr(prop_name,
                                                                                  prop_value,
                                                                                  study_name,
                                                                                  user,
                                                                                  derivative_sample_controller.authorizer(event['requestContext']['authorizer']))


    return create_response(event, retcode, value)

def download_derivative_samples_by_os_attr(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        prop_name = event["pathParameters"]["prop_name"]
        prop_value = event["pathParameters"]["prop_value"]

    study_name = None
    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'study_name' in event["queryStringParameters"]:
            study_name = event["queryStringParameters"]["study_name"]

    value, retcode = derivative_sample_controller.download_derivative_samples_by_os_attr(prop_name,
                                                                                     prop_value,
                                                                                     study_name,
                                                                                     user,
                                                                                     derivative_sample_controller.authorizer(event['requestContext']['authorizer']))


    return create_response(event, retcode, value)

def download_derivative_samples_by_study(event, context):

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

    value, retcode = derivative_sample_controller.download_derivative_samples_by_study(study_name, start,
                                                                                       count, user,
                                                                                       derivative_sample_controller.authorizer(event['requestContext']['authorizer']))

    return create_response(event, retcode, value)

def download_derivative_samples_by_event_set(event, context):

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

    value, retcode = derivative_sample_controller.download_derivative_samples_by_event_set(event_set_id,
                                                                                           start, count,
                                                                                           user,
                                                                                           derivative_sample_controller.authorizer(event['requestContext']['authorizer']))

def update_derivative_sample(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        derivative_sample_id = event["pathParameters"]["derivative_sample_id"]

    derivative_sample = DerivativeSample.from_dict(json.loads(event["body"]))

    value, retcode = derivative_sample_controller.update_location(derivative_sample_id, derivative_sample,
                                                                user,
                                                                derivative_sample_controller.authorizer(event['requestContext']['authorizer']))

    return create_response(event, retcode, value)


