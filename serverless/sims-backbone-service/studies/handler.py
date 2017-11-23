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

from swagger_server.models.studies import Studies
from swagger_server.models.study import Study

import logging

from decimal import *

from backbone_server.controllers.study_controller import StudyController

study_controller = StudyController()

def create_response(retcode, value):

    return {
        "statusCode": retcode,
        "headers": {
            "Access-Control-Allow-Origin" : "*"
        },
        "body": json.dumps(value.to_dict())
    }

def download_studies(event, context):

    user = event['requestContext']['authorizer']['principalId']

    start =  None
    count =  None

    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'start' in event["queryStringParameters"]:
            start = event["queryStringParameters"]["start"]
        if 'count' in event["queryStringParameters"]:
            count = event["queryStringParameters"]["count"]

    value, retcode = study_controller.download_studies(start, count, user)

    return create_response(retcode, value)

def download_study(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        study_id = event["pathParameters"]["study_id"]

    value, retcode =  study_controller.download_study(study_id, user)

    for s in value.locations.locations:
        s.location_id = str(s.location_id)
    return create_response(retcode, value)


def update_study(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        study_id = event["pathParameters"]["study_id"]

    study = Study.from_dict(json.loads(event["body"]))

    value, retcode = study_controller.update_study(study_id, study, user)

    return create_response(retcode, value)

