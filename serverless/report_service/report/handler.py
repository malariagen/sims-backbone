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

from backbone_server.controllers.report_controller import ReportController


report_controller = ReportController()

def missing_locations(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(report_controller, event)

    include_country = False

    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'include_country' in event["queryStringParameters"]:
            include_country = event["queryStringParameters"]["include_country"]

    value, retcode = report_controller.missing_locations(include_country, user, auths)

    return create_response(event, retcode, value)


def missing_taxon(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(report_controller, event)

    value, retcode = report_controller.missing_taxon(user, auths)

    return create_response(event, retcode, value)


def multiple_location_gps(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(report_controller, event)

    value, retcode = report_controller.multiple_location_gps(user, auths)

    return create_response(event, retcode, value)

def multiple_location_names(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(report_controller, event)

    value, retcode = report_controller.multiple_location_names(user, auths)

    return create_response(event, retcode, value)

def uncurated_locations(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(report_controller, event)

    value, retcode = report_controller.uncurated_locations(user, auths)

    return create_response(event, retcode, value)
