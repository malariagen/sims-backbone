from __future__ import print_function
import json
import os
import requests

import pytest
from api_factory import ApiFactory

import openapi_client
import logging


@pytest.fixture(params=['user1'])
def user(request):
    yield request.param


"""
"""


@pytest.fixture(params=[
    {
        'memberOf': ['cn=editor,ou=sims,ou=projects,ou=groups,dc=malariagen,dc=net',
                     'cn=editor,ou=otherproject,ou=projects,ou=groups,dc=malariagen,dc=net'],
        'scope': ['editor'],
        'uid': ['testuid'],
    },
    {
        'memberOf': ['group1', 'group2'],
        'scope': ['editor'],
        'uid': ['testuid'],
    },
    {
        'memberOf': [],
        'scope': ['editor'],
        'uid': ['testuid'],
    },
    {
        'memberOf': None,
        'scope': ['editor'],
        'uid': ['testuid'],
    },
    {
    },
])
def auths(request):
    yield request.param

# Not used


@pytest.fixture()
def method(request):
    yield 'custom'


access_token_cache = {}


@pytest.fixture()
def api_factory(request, user, auths, method):

    configuration = openapi_client.Configuration()

    # Not allowed to be None
    configuration.access_token = 'abcd'
    if not auths or 'editor' in auths:
        if os.getenv('TOKEN_URL') and not os.getenv('LOCAL_TEST'):
            # Could be str(auths) if want separate tokens
            cache_key = 'cache_key'
            if cache_key in access_token_cache:
                configuration.access_token = access_token_cache[cache_key]
            else:
                with open('../upload/config_dev.json') as json_file:
                    args = json.load(json_file)
                    token_request = requests.get(os.getenv('TOKEN_URL'),
                                                 args,
                                                 headers={'service': 'http://localhost/'})
                    token_response = token_request.text.split('=')
                    token = token_response[1].split('&')[0]
                    configuration.access_token = token
                    access_token_cache[cache_key] = token

    if os.getenv('REMOTE_HOST_URL'):
        configuration.host = os.getenv('REMOTE_HOST_URL')

    api_client = openapi_client.ApiClient(configuration)

    yield ApiFactory(user, auths, method, api_client)
