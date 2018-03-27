import json

from swagger_client.rest import ApiException
from swagger_client.rest import RESTResponse

from swagger_client.api_client import ApiClient

from swagger_server.encoder import JSONEncoder

from swagger_server.models.base_model_ import Model

class MockResponse:
    def __init__(self, json_data, status_code):
        self.data = json_data
        self.status = status_code
        self.reason = ''


class BaseLocalApi():

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_response(self, ret, retcode, response_type=None):

        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        if ret and response_type:
            if isinstance(ret, Model):
                response_dict = ret.to_dict()
            else:
                response_dict = ret

            resp_data = json.dumps(response_dict, ensure_ascii=False, cls=JSONEncoder)
            mr = MockResponse(resp_data, retcode)
            response = RESTResponse(mr)
            ret = self.api_client.deserialize(response, response_type)

        return ret

