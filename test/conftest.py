from __future__ import print_function
import json
import os
import requests

import pytest
from api_factory import ApiFactory

import openapi_client
@pytest.fixture(params=['user1'])
def user(request):
    yield request.param

"""
"""
@pytest.fixture(params=[
    ['cn=editor,ou=sims,ou=projects,ou=groups,dc=malariagen,dc=net'],
    [],
    None,
    ['group1', 'group2']
])
def auths(request):
    yield request.param

#Not used
@pytest.fixture()
def method(request):
    yield 'custom'

@pytest.fixture()
def api_factory(request, user, auths, method):

    configuration = openapi_client.Configuration()

    #Not allowed to be None
    configuration.access_token = 'abcd'
    if not auths or 'cn=editor,ou=sims,ou=projects,ou=groups,dc=malariagen,dc=net' in auths:
        if os.getenv('TOKEN_URL') and not os.getenv('LOCAL_TEST'):
            with open('../upload/config_dev.json') as json_file:
                args = json.load(json_file)
                token_request = requests.get(os.getenv('TOKEN_URL'),
                                             args,
                                             headers={'service': 'http://localhost/'})
                token_response = token_request.text.split('=')
                token = token_response[1].split('&')[0]
                configuration.access_token = token

    configuration.host = "http://localhost:8080/v1"

    api_client = openapi_client.ApiClient(configuration)

    yield ApiFactory(user, auths, method, api_client)
