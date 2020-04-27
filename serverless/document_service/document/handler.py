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

from requests_toolbelt.multipart import decoder
from rfc6266 import parse_headers

from openapi_server.models.document import Document

import logging


from backbone_server.controllers.document_controller import DocumentController

from util.response_util import create_response
from util.request_util import get_body, get_user, get_auths, get_body_raw

document_controller = DocumentController()

def get_document_from_multipart(event):

    postdata = get_body_raw(event)
    content_type_header = event['headers']['content-type']
    content = None
    doc1 = Document()

    for part in decoder.MultipartDecoder(postdata, content_type_header).parts:

        headers = part.headers
        content_type = 'Unknown'
        if b'Content-Type' in headers:
            content_type = part.headers[b'Content-Type'].decode("utf-8")
        dispo = None
        if b'Content-Disposition' in headers:
            dispo = part.headers[b'Content-Disposition']
            dispo_vals = parse_headers(dispo)
            var_name = dispo_vals.assocs['name']
            if 'filename' not in dispo_vals.assocs:
                setattr(doc1, var_name, part.text)
            elif var_name == 'document':
                doc1.content_type = content_type
                filename = dispo_vals.filename_unsafe
                doc1.doc_name = filename

                content = part.content

    return doc1, content

def create_document(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(document_controller, event)

    study_code = None
    if 'pathParameters' in event:
        study_code = event["pathParameters"]["study_code"]
    #document = Document.from_dict(get_body(event))

    doc1, content = get_document_from_multipart(event)

    value, retcode = document_controller.create_document(study_code, doc1,
                                                         doc_content=content,
                                                         user=user,
                                                         auths=auths)

    #value.location_id = str(value.location_id)

    return create_response(event, retcode, value)

def update_document(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(document_controller, event)

    if 'pathParameters' in event:
        document_id = event["pathParameters"]["document_id"]

    doc1, content = get_document_from_multipart(event)
    doc1.document_id = document_id
    doc1.version = int(doc1.version)
    value, retcode = document_controller.update_document(document_id, doc1,
                                                         doc_content=content,
                                                         user=user,
                                                         auths=auths)

    return create_response(event, retcode, value)

def delete_document(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(document_controller, event)

    if 'pathParameters' in event:
        document_id = event["pathParameters"]["document_id"]

    value, retcode = document_controller.delete_document(document_id, user=user,
                                                         auths=auths)

    return create_response(event, retcode, value)

def download_document(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(document_controller, event)

    if 'pathParameters' in event:
        document_id = event["pathParameters"]["document_id"]

    value, retcode = document_controller.download_document(document_id, user=user,
                                                           auths=auths)

    value.document_id = str(value.document_id)

    return create_response(event, retcode, value)

def download_document_content(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(document_controller, event)

    if 'pathParameters' in event:
        document_id = event["pathParameters"]["document_id"]

    value, retcode, headers = document_controller.download_document_content(document_id, user=user, auths=auths)

    return {
        "statusCode": retcode,
        "headers": headers
    }

def download_documents_by_study(event, context):

    user = get_user(event)

    if user is None:
        return create_response(event, 401, {})

    auths = get_auths(document_controller, event)

    study_code = None
    start = None
    count = None
    orderby = None

    if 'pathParameters' in event:
        study_code = event["pathParameters"]["study_code"]

    if 'queryStringParameters' in event and event["queryStringParameters"]:
        if 'start' in event["queryStringParameters"]:
            start = int(event["queryStringParameters"]["start"])
        if 'count' in event["queryStringParameters"]:
            count = int(event["queryStringParameters"]["count"])
        if 'orderby' in event["queryStringParameters"]:
            orderby = event["queryStringParameters"]["orderby"]

    value, retcode = document_controller.download_documents_by_study(study_code,
                                                                     user=user,
                                                                     auths=auths)

    return create_response(event, retcode, value)
