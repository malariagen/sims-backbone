from io import BytesIO
import base64
import gzip
import json
import ujson

import logging

from openapi_server.encoder import JSONEncoder

from openapi_server.models.base_model_ import Model

def gzip_b64encode(data):
    compressed = BytesIO()
    with gzip.GzipFile(fileobj=compressed, mode='w') as f:
        json_response = json.dumps(data, ensure_ascii=False, cls=JSONEncoder)
        f.write(json_response.encode('utf-8'))
    return base64.b64encode(compressed.getvalue()).decode('ascii')

def create_response(event, retcode, value):

    response_dict = {}
    if value:
        if isinstance(value, Model):
            response_dict = value.to_dict()
        else:
            response_dict = value

    gzip = False
    if 'headers' in event and event['headers'] is not None:
        if 'Accept-Encoding' in event['headers']:
            if 'gzip' in event['headers']['Accept-Encoding']:
                if 'Accept' in event['headers']:
                    #Otherwise base64 decoding doesn't happen
                    #See gateway settings in serverless.yml
                    if 'application/json' in event['headers']['Accept']:
                        gzip = True

    gzip = False

    if gzip:
        return {
            "statusCode": retcode,
            "isBase64Encoded": True,
            "headers": {
                "Access-Control-Allow-Origin" : "*",
                'Content-Type': 'application/json',
                'Content-Encoding': 'gzip'
            },
            "body": gzip_b64encode(response_dict)
        }
    else:
        return {
            "statusCode": retcode,
            "headers": {
                "Access-Control-Allow-Origin" : "*",
                'Content-Type': 'application/json'
            },
            "body": json.dumps(response_dict, ensure_ascii=False, cls=JSONEncoder)
        }

