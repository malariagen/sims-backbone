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
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
#from ..util import deserialize_date, deserialize_datetime

from decimal import *

import logging

from backbone_server.location.post import LocationPost

from backbone_server.location.put import LocationPut

from backbone_server.location.get import LocationGetById

from backbone_server.location.gets import LocationsGet

from backbone_server.location.delete import LocationDelete
from backbone_server.location.get_by_name import LocationGetByPartnerName
from backbone_server.location.get_by_gps import LocationGetByGPS

from backbone_server.connect  import get_connection

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException


def create_location(event, context):

    location = Location.from_dict(json.loads(event["body"]))

    retcode = 200
    loc = None

    try:
        post = LocationPost(get_connection())

        loc = post.post(location)
    except DuplicateKeyException as dke:
        logging.getLogger(__name__).error("create_location: {}".format(repr(dke)))
        retcode = 422

    response = {
        "statusCode": retcode,
        "body": str(loc)
    }

    return response

def download_location(event, context):

    if 'pathParameters' in event:
        location_id = event["pathParameters"]["location_id"]

    get = LocationGetById(get_connection())

    retcode = 200
    loc = None

    try:
        loc = get.get(location_id)
    except MissingKeyException as dme:
        logging.getLogger(__name__).error("download_location: {}".format(repr(dme)))
        retcode = 404

    response = {
        "statusCode": retcode,
        "body": str(loc)
    }

    return response


def download_locations(event, context):

    print((event['requestContext']['authorizer']['key']))
    print((event['requestContext']['authorizer']['principalId']))

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

    get = LocationsGet(get_connection())

    retcode = 200
    loc = None

    try:
        loc = get.get(study_name, start, count, orderby)
    except MissingKeyException as dme:
        logging.getLogger(__name__).error("download_location: {}".format(repr(dme)))
        retcode = 404

    response = {
        "statusCode": retcode,
        "headers": {
            "Access-Control-Allow-Origin" : "*"
        },
        "body": json.dumps(loc.to_dict())
    }

    return response


def update_location(event, context):

    if 'pathParameters' in event:
        location_id = event["pathParameters"]["location_id"]

    location = Location.from_dict(json.loads(event["body"]))

    retcode = 200
    loc = None

    try:
        put = LocationPut(get_connection())

        loc = put.put(location_id, location)
    except DuplicateKeyException as dke:
        logging.getLogger(__name__).error("update_location: {}".format(repr(dke)))
        retcode = 422
    except MissingKeyException as dme:
        logging.getLogger(__name__).error("update_location: {}".format(repr(dme)))
        retcode = 404


    body = {
        "message": "Update Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": retcode,
        "body": str(loc)
    }

    return response

def download_gps_location(event, context):

    if 'pathParameters' in event:
        latitude = event["pathParameters"]["latitude"]
        longitude = event["pathParameters"]["longitude"]

    get = LocationGetByGPS(get_connection())

    retcode = 200
    loc = None

    try:
        lat = Decimal(latitude)
        lng = Decimal(longitude)
        loc = get.get(lat, lng)
    except MissingKeyException as dme:
        logging.getLogger(__name__).error("download_partner_location: {}".format(repr(dme)))
        retcode = 404
    except InvalidOperation as nfe:
        logging.getLogger(__name__).error("download_partner_location: {}".format(repr(nfe)))
        retcode = 422

    response = {
        "statusCode": retcode,
        "body": str(loc)
    }

    return response
