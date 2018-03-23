from __future__ import print_function
import unittest
import swagger_client
import json
import requests
import os

class TestBase(unittest.TestCase):


    _auth_token = None
    _configuration = None
    _api_client = None

    """
    """
    def setUp(self):

        self._configuration = swagger_client.Configuration()
        if os.getenv('TOKEN_URL'):
            with open('../upload/config_dev.json') as json_file:
                args = json.load(json_file)
                r = requests.get(os.getenv('TOKEN_URL'), args, headers = { 'service': 'http://localhost/' })
                at = r.text.split('=')
                token = at[1].split('&')[0]
                self._auth_token = token
            self._configuration.access_token = self._auth_token

        self._api_client = swagger_client.ApiClient(self._configuration)


    """
    """
    def tearDown(self):
        pass


