import json
import os, sys, inspect
# realpath() will make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
     sys.path.insert(0, cmd_folder)

# Use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe() ))[0],"server")))
if cmd_subfolder not in sys.path:
     sys.path.insert(0, cmd_subfolder)

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0],"server/bb_server")))
if cmd_subfolder not in sys.path:
     sys.path.insert(0, cmd_subfolder)

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0],"dev")))
if cmd_subfolder not in sys.path:
     sys.path.insert(0, cmd_subfolder)

from swagger_server.models.studies import Studies
from swagger_server.models.study import Study

import logging

from decimal import *

from backbone_server.controllers.studies_controller import StudiesController

studies_controller = StudiesController()

def create_response(retcode, value):

    return {
        "statusCode": retcode,
        "headers": {
            "Access-Control-Allow-Origin" : "*"
        },
        "body": json.dumps(value.to_dict())
    }

def download_studies(self, start=None, count=None):

    user = event['requestContext']['authorizer']['principalId']

    start =  None
    count =  None

    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'start' in event["queryStringParameters"]:
            start = event["queryStringParameters"]["start"]
        if 'count' in event["queryStringParameters"]:
            count = event["queryStringParameters"]["count"]

    return create_response(studies_controller.download_studies(start, count, user))

def download_study(self, studyId):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        study_id = event["pathParameters"]["study_id"]

    return create_response( studies_controller.download_study(study_id, user))


def update_study(self, studyId, study, user=None):

    user = event['requestContext']['authorizer']['principalId']

    study = Study.from_dict(json.loads(event["body"]))

    return create_response(studies_controller.update_study(study, user))

