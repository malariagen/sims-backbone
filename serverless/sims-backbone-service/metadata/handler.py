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

from swagger_server.models.taxonomy import Taxonomy

import logging

from decimal import *

from backbone_server.controllers.metadata_controller import MetadataController

from util.response_util import create_response

metadata_controller = MetadataController()

def create_taxonomy(event, context):

    user = event['requestContext']['authorizer']['principalId']

    taxa = Taxonomy.from_dict(json.loads(event["body"]))

    value, retcode = metadata_controller.create_taxonomy(taxa, user,
                                                         metadata_controller.authorizer(event['requestContext']['authorizer']))

    return create_response(event, retcode, value)


def get_country_metadata(event, context):

    user = event['requestContext']['authorizer']['principalId']

    if 'pathParameters' in event:
        country_id = event["pathParameters"]["country_id"]

    value, retcode = metadata_controller.get_country_metadata(country_id, user,
                                                              metadata_controller.authorizer(event['requestContext']['authorizer']))

    return create_response(event, retcode, value)

def get_attr_types(event, context):

    user = event['requestContext']['authorizer']['principalId']

    value, retcode = metadata_controller.get_attr_types(user,
                                                               metadata_controller.authorizer(event['requestContext']['authorizer']))

    return create_response(event, retcode, value)

def get_location_attr_types(event, context):

    user = event['requestContext']['authorizer']['principalId']

    value, retcode = metadata_controller.get_location_attr_types(user,
                                                               metadata_controller.authorizer(event['requestContext']['authorizer']))

    return create_response(event, retcode, value)

def get_taxonomy_metadata(event, context):

    user = event['requestContext']['authorizer']['principalId']

    value, retcode = metadata_controller.get_taxonomy_metadata(user,
                                                               metadata_controller.authorizer(event['requestContext']['authorizer']))

    return create_response(event, retcode, value)

