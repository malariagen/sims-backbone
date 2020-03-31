import json
import os, sys, inspect

currentframe = os.path.split(inspect.getfile(inspect.currentframe()))[0]
paths = os.getenv('PYTHON_PATH').split(':')

for include_path in paths:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(currentframe,include_path)))
    if cmd_subfolder not in sys.path:
         sys.path.insert(0, cmd_subfolder)

from openapi_server.models.taxonomy import Taxonomy

import logging


from util.response_util import create_response
from util.request_util import get_body, get_user, get_auths

from backbone_server.controllers.metadata_controller import MetadataController

metadata_controller = MetadataController()

def create_taxonomy(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(metadata_controller, event)

    taxa = Taxonomy.from_dict(get_body(event))

    value, retcode = metadata_controller.create_taxonomy(taxa, user=user,
                                                         auths=auths)

    return create_response(event, retcode, value)


def get_country_metadata(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(metadata_controller, event)

    country_id = None
    if 'pathParameters' in event:
        country_id = event["pathParameters"]["country_id"]

    value, retcode = metadata_controller.get_country_metadata(country_id, user=user,
                                                              auths=auths)

    return create_response(event, retcode, value)

def get_attr_types(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(metadata_controller, event)

    parent_type = None
    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'parent_type' in event["queryStringParameters"]:
            parent_type = event["queryStringParameters"]["parent_type"]

    value, retcode = metadata_controller.get_attr_types(parent_type, user=user,
                                                        auths=auths)

    return create_response(event, retcode, value)

def get_location_attr_types(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(metadata_controller, event)

    value, retcode = metadata_controller.get_location_attr_types(user=user,
                                                                 auths=auths)

    return create_response(event, retcode, value)

def get_taxonomy_metadata(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(metadata_controller, event)

    value, retcode = metadata_controller.get_taxonomy_metadata(user=user,
                                                               auths=auths)

    return create_response(event, retcode, value)
