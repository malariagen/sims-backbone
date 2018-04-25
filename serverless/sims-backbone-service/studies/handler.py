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

from swagger_server.models.studies import Studies
from swagger_server.models.study import Study

import logging

from backbone_server.controllers.study_controller import StudyController

study_controller = StudyController()

def download_studies(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 200, {})

    auths = get_auths(study_controller, event)

    start = None
    count = None

    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'start' in event["queryStringParameters"]:
            start = int(event["queryStringParameters"]["start"])
        if 'count' in event["queryStringParameters"]:
            count = int(event["queryStringParameters"]["count"])

    value, retcode = study_controller.download_studies(start, count, user, auths)

    return create_response(event, retcode, value)

def download_study(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(study_controller, event)

    if 'pathParameters' in event:
        study_id = event["pathParameters"]["study_id"]

    value, retcode = study_controller.download_study(study_id, user, auths)

    return create_response(event, retcode, value)


def update_study(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(study_controller, event)

    if 'pathParameters' in event:
        study_id = event["pathParameters"]["study_id"]

    study = Study.from_dict(json.loads(event["body"]))

    value, retcode = study_controller.update_study(study_id, study, user, auths)

    return create_response(event, retcode, value)

