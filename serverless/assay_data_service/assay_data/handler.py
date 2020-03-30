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

from openapi_server.models.assay_datum import AssayDatum

import logging

import datetime

from backbone_server.controllers.assay_datum_controller import AssayDatumController

from util.response_util import create_response
from util.request_util import get_body, get_user, get_auths

assay_datum_controller = AssayDatumController()

def create_assay_datum(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(assay_datum_controller, event)

    assay_datum = AssayDatum.from_dict(get_body(event))

    value, retcode = assay_datum_controller.create_assay_datum(assay_datum, user=user,
                                                               auths=auths)

    return create_response(event, retcode, value)


def delete_assay_datum(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(assay_datum_controller, event)

    if 'pathParameters' in event:
        assay_datum_id = event["pathParameters"]["assay_datum_id"]

    value, retcode = assay_datum_controller.delete_assay_datum(assay_datum_id, user=user,
                                                               auths=auths)

    return create_response(event, retcode, value)


def download_assay_datum(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(assay_datum_controller, event)


    if 'pathParameters' in event:
        assay_datum_id = event["pathParameters"]["assay_datum_id"]

    value, retcode = assay_datum_controller.download_assay_datum(assay_datum_id, user=user,
                                                                 auths=auths)

    return create_response(event, retcode, value)


def download_assay_data_by_attr(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(assay_datum_controller, event)


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

    value, retcode = assay_datum_controller.download_assay_data_by_attr(prop_name,
                                                                        prop_value,
                                                                        study_name,
                                                                        value_type=value_type,
                                                                        start=start,
                                                                        count=count,
                                                                        user=user,
                                                                        auths=auths)


    return create_response(event, retcode, value)

def download_assay_data_by_os_attr(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(assay_datum_controller, event)


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

    value, retcode = assay_datum_controller.download_assay_data_by_os_attr(prop_name,
                                                                           prop_value,
                                                                           study_name,
                                                                           value_type=value_type,
                                                                           start=start,
                                                                           count=count,
                                                                           user=user,
                                                                           auths=auths)


    return create_response(event, retcode, value)

def update_assay_datum(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(assay_datum_controller, event)


    if 'pathParameters' in event:
        assay_datum_id = event["pathParameters"]["assay_datum_id"]

    assay_datum = AssayDatum.from_dict(get_body(event))

    value, retcode = assay_datum_controller.update_location(assay_datum_id, assay_datum,
                                                            user=user,
                                                            auths=auths)

    return create_response(event, retcode, value)
