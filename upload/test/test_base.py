from __future__ import print_function
import unittest
import json
import requests
import os

from upload_ssr import Upload_SSR

import swagger_client
from swagger_client.rest import ApiException

from swagger_client.rest import RESTResponse

from swagger_client.api_client import ApiClient


class MockResponse:
    def __init__(self, json_data, status_code):
        self.data = json_data
        self.status = status_code
        self.reason = ''

class TestBase(unittest.TestCase):


    _api_client = None

    _config_file = '../config_dev.json'

    _locations = []

    @classmethod
    def getApiClient(self):
        auth_token = None
        configuration = swagger_client.Configuration()

        if os.getenv('TOKEN_URL'):
            try:
                with open(self._config_file) as json_file:
                    args = json.load(json_file)
                    r = requests.get(os.getenv('TOKEN_URL'), args, headers = { 'service': 'http://localhost/' })
                    at = r.text.split('=')
                    token = at[1].split('&')[0]
                    auth_token = token
                configuration.access_token = auth_token
            except FileNotFoundError as fnfe:
                print('No config file found: {}'.format(TestBase._config_file))
                pass

        if os.getenv('REMOTE_HOST_URL'):
          configuration.host = "http://localhost:8080/v1"

        api_client = swagger_client.ApiClient(configuration)

        return api_client

    """
    """
    def setUp(self):

        self._api_client = TestBase.getApiClient()

    """
    """
    def tearDown(self):
        pass


    """
    """
    @classmethod
    def setUpSSR(self):

        el = Upload_SSR(TestBase._config_file)
        sheets = None
        el.load_data_file('TestSSR.xls', sheets)

    """
    """
    @classmethod
    def deleteSamplingEvent(self, event, locations):
        event_api_instance = swagger_client.SamplingEventApi(TestBase.getApiClient())
        if event.location_id and event.location_id not in locations:
            locations.append(event.location_id)
        if event.proxy_location_id and event.proxy_location_id not in locations:
            locations.append(event.proxy_location_id)
        event_api_instance.delete_sampling_event(event.sampling_event_id)

    """
    """
    @classmethod
    def deleteEventSets(self, event_sets, locations):

        api_instance = swagger_client.EventSetApi(TestBase.getApiClient())
        event_api_instance = swagger_client.SamplingEventApi(TestBase.getApiClient())

        for event_set in event_sets:
            test_events = event_api_instance.download_sampling_events_by_event_set(event_set)

            for event in test_events.sampling_events:
                TestBase.deleteSamplingEvent(event, locations)

            api_instance.delete_event_set(event_set)

    """
    """
    @classmethod
    def deleteStudies(self, studies, locations):

        event_api_instance = swagger_client.SamplingEventApi(TestBase.getApiClient())

        for study in studies:
            test_events = event_api_instance.download_sampling_events_by_study(study)

            for event in test_events.sampling_events:
                TestBase.deleteSamplingEvent(event, locations)
    """
    """
    @classmethod
    def tearDownSSR(self, locations):

        TestBase.deleteStudies(['9050', '9051'], locations)

        TestBase.deleteEventSets(['TestSSR', 'Report', 'Sequencescape', 'PV4', 'PF27', 'Ag'],
                                 locations)

    """
    """
    @classmethod
    def tearDownLocations(self, locations):
        location_api_instance = swagger_client.LocationApi(TestBase.getApiClient())

        for loc in locations:
            if loc:
                location_api_instance.delete_location(loc)

