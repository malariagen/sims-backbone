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

assay_datum_controller = AssayDatumController()

def create_assay_datum(event, context):

    user = event['requestContext']['authorizer']['principalId']

    assay_datum = AssayDatum.from_dict(json.loads(event["body"]))

    value, retcode = assay_datum_controller.create_assay_datum(assay_datum, user,
                                                                       assay_datum_controller.authorizer(event['requestContext']['authorizer']))

    return create_response(event, retcode, value)


def delete_assay_datum(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        assay_datum_id = event["pathParameters"]["assay_datum_id"]

    value, retcode =  assay_datum_controller.delete_assay_datum(assay_datum_id, user,
                                                                        assay_datum_controller.authorizer(event['requestContext']['authorizer']))

    return create_response(event, retcode, value)


def download_assay_datum(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        assay_datum_id = event["pathParameters"]["assay_datum_id"]

    value, retcode =  assay_datum_controller.download_assay_datum(assay_datum_id, user,
                                                                          assay_datum_controller.authorizer(event['requestContext']['authorizer']))

    return create_response(event, retcode, value)


def download_assay_data_by_attr(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        prop_name = event["pathParameters"]["prop_name"]
        prop_value = event["pathParameters"]["prop_value"]

    study_name = None
    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'study_name' in event["queryStringParameters"]:
            study_name = event["queryStringParameters"]["study_name"]

    value, retcode = assay_datum_controller.download_assay_data_by_attr(prop_name,
                                                                                  prop_value,
                                                                                  study_name,
                                                                                  user,
                                                                                  assay_datum_controller.authorizer(event['requestContext']['authorizer']))


    return create_response(event, retcode, value)

def download_assay_data_by_os_attr(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        prop_name = event["pathParameters"]["prop_name"]
        prop_value = event["pathParameters"]["prop_value"]

    study_name = None
    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'study_name' in event["queryStringParameters"]:
            study_name = event["queryStringParameters"]["study_name"]

    value, retcode = assay_datum_controller.download_assay_data_by_os_attr(prop_name,
                                                                                     prop_value,
                                                                                     study_name,
                                                                                     user,
                                                                                     assay_datum_controller.authorizer(event['requestContext']['authorizer']))


    return create_response(event, retcode, value)

def update_assay_datum(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        assay_datum_id = event["pathParameters"]["assay_datum_id"]

    assay_datum = AssayDatum.from_dict(json.loads(event["body"]))

    value, retcode = assay_datum_controller.update_location(assay_datum_id, assay_datum,
                                                                user,
                                                                assay_datum_controller.authorizer(event['requestContext']['authorizer']))

    return create_response(event, retcode, value)


