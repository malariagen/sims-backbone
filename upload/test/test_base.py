from __future__ import print_function
import unittest
import json
import requests
import os

from upload_ssr import Upload_SSR

import swagger_client
from swagger_client.rest import ApiException

class TestBase(unittest.TestCase):


    _auth_token = None
    _configuration = None
    _api_client = None

    _config_file = '../config_dev.json'

    _locations = []

    """
    """
    def setUp(self):
        self._configuration = swagger_client.Configuration()

        if os.getenv('TOKEN_URL'):
            try:
                with open(self._config_file) as json_file:
                    args = json.load(json_file)
                    r = requests.get(os.getenv('TOKEN_URL'), args, headers = { 'service': 'http://localhost/' })
                    at = r.text.split('=')
                    token = at[1].split('&')[0]
                    self._auth_token = token
                self._configuration.access_token = self._auth_token
            except FileNotFoundError as fnfe:
                print('No config file found: {}'.format(self._config_file))
                pass

        self._api_client = swagger_client.ApiClient(self._configuration)


    """
    """
    def tearDown(self):
        pass


    """
    """
    @classmethod
    def setUpSSR(self):

        el = Upload_SSR(self._config_file)
        sheets = None
        el.load_data_file('TestSSR.xls', sheets)

    """
    """
    @classmethod
    def deleteSamplingEvent(self, event):
        event_api_instance = swagger_client.SamplingEventApi(self._api_client)
        if event.location_id and event.location_id not in self._locations:
            self._locations.append(event.location_id)
        event_api_instance.delete_sampling_event(event.sampling_event_id)

    """
    """
    @classmethod
    def deleteEventSets(self, event_sets):

        api_instance = swagger_client.EventSetApi(self._api_client)
        event_api_instance = swagger_client.SamplingEventApi(self._api_client)

        for event_set in event_sets:
            test_events = event_api_instance.download_sampling_events_by_event_set(event_set)

            for event in test_events.sampling_events:
                self.deleteSamplingEvent(event)

            api_instance.delete_event_set(event_set)

    """
    """
    @classmethod
    def deleteStudies(self, studies):

        event_api_instance = swagger_client.SamplingEventApi(self._api_client)

        for study in studies:
            test_events = event_api_instance.download_sampling_events_by_study(study)

            for event in test_events.sampling_events:
               self.deleteSamplingEvent(event)
    """
    """
    @classmethod
    def tearDownSSR(self):

        self.deleteStudies(['9050', '9051'])

        self.deleteEventSets(['TestSSR', 'Report', 'Sequencescape', 'PV4', 'PF27', 'Ag'])

    """
    """
    @classmethod
    def tearDownLocations(self):
        location_api_instance = swagger_client.LocationApi(self._api_client)

        for loc in self._locations:
            self._locations.remove(loc)
            location_api_instance.delete_location(loc)

