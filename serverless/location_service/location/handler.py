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

from openapi_server.models.location import Location

import logging

from decimal import *

from backbone_server.controllers.location_controller import LocationController

from util.response_util import create_response
from util.request_util import get_body, get_user, get_auths

location_controller = LocationController()

def create_location(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(location_controller, event)

    location = Location.from_dict(get_body(event))

    value, retcode = location_controller.create_location(location, user=user,
                                                         auths=auths)

    value.location_id = str(value.location_id)

    return create_response(event, retcode, value)

def delete_location(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(location_controller, event)

    if 'pathParameters' in event:
        location_id = event["pathParameters"]["location_id"]

    value, retcode = location_controller.delete_location(location_id, user=user,
                                                         auths=auths)

    return create_response(event, retcode, value)

def download_location(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(location_controller, event)

    if 'pathParameters' in event:
        location_id = event["pathParameters"]["location_id"]

    value, retcode = location_controller.download_location(location_id, user=user,
                                                           auths=auths)

    value.location_id = str(value.location_id)

    return create_response(event, retcode, value)

def download_locations(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(location_controller, event)

    study_name = None
    start = None
    count = None
    orderby = None

    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'study_name' in event["queryStringParameters"]:
            study_name = event["queryStringParameters"]["study_name"]
        if 'start' in event["queryStringParameters"]:
            start = int(event["queryStringParameters"]["start"])
        if 'count' in event["queryStringParameters"]:
            count = int(event["queryStringParameters"]["count"])
        if 'orderby' in event["queryStringParameters"]:
            orderby = event["queryStringParameters"]["orderby"]

    value, retcode = location_controller.download_locations(study_name, start, count,
                                                            orderby, user=user,
                                                            auths=auths)

    for loc in value.locations:
        loc.location_id = str(loc.location_id)

    return create_response(event, retcode, value)

def download_partner_location(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(location_controller, event)

    if 'pathParameters' in event:
        partner_id = event["pathParameters"]["partner_id"]

    value, retcode = location_controller.download_partner_location(partner_id, user=user,
                                                                   auths=auths)

    value.location_id = str(value.location_id)

    return create_response(event, retcode, value)

def update_location(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(location_controller, event)

    if 'pathParameters' in event:
        location_id = event["pathParameters"]["location_id"]

    location = Location.from_dict(get_body(event))

    value, retcode = location_controller.update_location(location_id, location, user=user,
                                                         auths=auths)

    value.location_id = str(value.location_id)

    return create_response(event, retcode, value)

def download_gps_location(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(location_controller, event)

    if 'pathParameters' in event:
        latitude = event["pathParameters"]["latitude"]
        longitude = event["pathParameters"]["longitude"]

    lat = Decimal(latitude)
    lng = Decimal(longitude)

    value, retcode = location_controller.download_gps_location(lat, lng, user=user,
                                                               auths=auths)

    value.location_id = str(value.location_id)

    return create_response(event, retcode, value)
