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

from swagger_server.models.location import Location

import logging

from decimal import *

from backbone_server.controllers.location_controller import LocationController

location_controller = LocationController()

def create_location(event, context):

    user = event['requestContext']['authorizer']['principalId']

    location = Location.from_dict(json.loads(event["body"]))

    loc, retcode = location_controller.create_location(location, user)

    response = {
        "statusCode": retcode,
        "headers": {
            "Access-Control-Allow-Origin" : "*"
        },
        "body": str(loc)
    }

    return response

def download_location(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        location_id = event["pathParameters"]["location_id"]

    loc, retcode = location_controller.download_location(location_id, user)

    response = {
        "statusCode": retcode,
        "headers": {
            "Access-Control-Allow-Origin" : "*"
        },
        "body": str(loc)
    }

    return response


def download_locations(event, context):

    user = event['requestContext']['authorizer']['principalId']

    study_name = None
    start =  None
    count =  None
    orderby =  'location'

    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'study_name' in event["queryStringParameters"]:
            study_name = event["queryStringParameters"]["study_name"]
        if 'start' in event["queryStringParameters"]:
            start = event["queryStringParameters"]["start"]
        if 'count' in event["queryStringParameters"]:
            count = event["queryStringParameters"]["count"]
        if 'orderby' in event["queryStringParameters"]:
            orderby = event["queryStringParameters"]["orderby"]

    loc, retcode = location_controller.download_locations(study_name, start, count, orderby, user)

    response = {
        "statusCode": retcode,
        "headers": {
            "Access-Control-Allow-Origin" : "*"
        },
        "body": json.dumps(loc.to_dict())
    }

    return response


def update_location(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        location_id = event["pathParameters"]["location_id"]

    location = Location.from_dict(json.loads(event["body"]))

    loc, retcode = location_controller.update_location(location_id, location, user)

    response = {
        "statusCode": retcode,
        "headers": {
            "Access-Control-Allow-Origin" : "*"
        },
        "body": str(loc)
    }

    return response

def download_gps_location(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        latitude = event["pathParameters"]["latitude"]
        longitude = event["pathParameters"]["longitude"]

    lat = Decimal(latitude)
    lng = Decimal(longitude)

    loc, retcode = location_controller.download_gps_location(lat, lng, user)

    response = {
        "statusCode": retcode,
        "headers": {
            "Access-Control-Allow-Origin" : "*"
        },
        "body": str(loc)
    }

    return response
