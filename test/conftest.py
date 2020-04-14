import json
import os
import requests

import pytest
from api_factory import ApiFactory

import openapi_client
import logging

auth_test_params=[
    {
        'memberOf': ['cn=editor,ou=sims,ou=projects,ou=groups,dc=malariagen,dc=net',
                     'cn=editor,ou=otherproject,ou=projects,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=0000,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=0001,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=1009,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=1010,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=1011,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=1012,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=1013,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=1014,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=1015,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=1020,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=1021,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=1022,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=1023,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=1024,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=1027,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=9100,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=9101,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=9102,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=9103,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=9104,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=9105,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=9106,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=9107,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=9108,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=9109,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=9120,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=9137,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=9138,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=9139,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=9140,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=1234,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=2000,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=2001,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=2002,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=2004,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=2005,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=2006,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=2007,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=2008,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=2100,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=3000,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=3001,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=4000,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=4001,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=4002,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=4003,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=4004,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=4005,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=4006,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=4008,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=4020,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=4021,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=4022,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=4023,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=4024,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=4025,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=4029,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=4031,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=4032,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=4033,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=4034,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=4035,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=4036,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=4037,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=4038,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=4039,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=5000,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=5002,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=5004,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=6003,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=7000,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=7001,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=7002,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=7003,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=7004,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=7005,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=7006,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=7007,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=7008,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=7009,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=7010,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=7011,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=7012,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=7013,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=7014,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=7015,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=7016,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=7017,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=7018,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=7019,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=8004,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=8100,ou=studies,ou=groups,dc=malariagen,dc=net',
                     'cn=pi,ou=9999,ou=studies,ou=groups,dc=malariagen,dc=net',
                    ],
        'scope': ['editor'],
        'uid': ['testuid'],
    },
    {
        'memberOf': ['group1', 'group2'],
        'scope': ['editor'],
        'uid': ['testuid'],
    },
    {
        'memberOf': [
            'cn=editor,ou=sims,ou=projects,ou=groups,dc=malariagen,dc=net',
            'cn=all_studies,ou=sims,ou=projects,ou=groups,dc=malariagen,dc=net'
        ],
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
]

if os.getenv('TOKEN_URL') and not os.getenv('LOCAL_TEST'):

    with open('../upload/config_dev.json') as json_file:
        args = json.load(json_file)
        token_request = requests.get(os.getenv('TOKEN_URL'),
                                     args,
                                     headers={'service': 'http://localhost/'})
        token_response = token_request.text.split('=')
        token = token_response[1].split('&')[0]

    auth_test_params = [
        {
            'auth_token': token
        }
    ]

@pytest.fixture(params=['user1'])
def user(request):
    yield request.param


"""
"""


@pytest.fixture(params=auth_test_params)
def auths(request):
    yield request.param

# Not used


@pytest.fixture()
def method(request):
    yield 'custom'


@pytest.fixture()
def api_factory(request, user, auths, method):

    configuration = openapi_client.Configuration()

    # Not allowed to be None
    configuration.access_token = 'abcd'

    if 'auth_token' in auths:
        configuration.access_token = auths['auth_token']

    if os.getenv('REMOTE_HOST_URL'):
        configuration.host = os.getenv('REMOTE_HOST_URL')

    api_client = openapi_client.ApiClient(configuration)

    yield ApiFactory(user, auths, method, api_client)
