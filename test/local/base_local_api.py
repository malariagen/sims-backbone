import json

from openapi_client.rest import ApiException
from openapi_client.rest import RESTResponse

from openapi_client.api_client import ApiClient

from openapi_server.encoder import JSONEncoder

from openapi_server.models.base_model_ import Model

class MockResponse:
    def __init__(self, json_data, status_code):
        self.data = json_data
        self.status = status_code
        self.reason = ''


class BaseLocalApi():

    def __init__(self, api_client, user, auths, method):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

        self._user = user
        self._auths = auths
        self._method = method

    def auth_tokens(self):
        return self._auths

    def create_response(self, ret, retcode, response_type=None):

        if retcode >= 400:
            raise ApiException(status=retcode, reason=ret)

        if ret and response_type:
            if isinstance(ret, Model):
                response_dict = ret.to_dict()
            else:
                response_dict = ret

            if not response_type == 'LogItems':
                resp_data = json.dumps(response_dict, ensure_ascii=False, cls=JSONEncoder)
                mock = MockResponse(resp_data, retcode)
                response = RESTResponse(mock)
                ret = self.api_client.deserialize(response, response_type)
            else:
                # This whole section is because oneOf isn't properly
                # deserialized when there are required elements
                log_items = response_dict['log_items']
                response_dict['log_items'] = None
                resp_data = json.dumps(response_dict, ensure_ascii=False, cls=JSONEncoder)
                mock = MockResponse(resp_data, retcode)
                response = RESTResponse(mock)
                ret = self.api_client.deserialize(response, response_type)
                new_items = []
                for item in log_items:
                    sub_type = None
                    if 'location' in item['action']:
                        sub_type = 'Location'
                    elif 'event' in item['action']:
                        sub_type = 'SamplingEvent'
                    elif 'original' in item['action']:
                        sub_type = 'OriginalSample'
                    elif 'derivative' in item['action']:
                        sub_type = 'DerivativeSample'
                    sub_item = None
                    if item['result'] < 400:
                        resp_data = json.dumps(item['output_value'], ensure_ascii=False, cls=JSONEncoder)
                        item['output_value'] = None
                        mock = MockResponse(resp_data, retcode)
                        response = RESTResponse(mock)
                        sub_item = self.api_client.deserialize(response,
                                                               sub_type)
                    else:
                        sub_item = item['output_value']
                        item['output_value'] = None
                    resp_data = json.dumps(item, ensure_ascii=False, cls=JSONEncoder)
                    mock = MockResponse(resp_data, retcode)
                    response = RESTResponse(mock)
                    item_val = self.api_client.deserialize(response,
                                                           'LogItem')
                    if sub_item:
                        item_val.output_value = sub_item
                    new_items.append(item_val)
                ret.log_items = new_items


        return ret
