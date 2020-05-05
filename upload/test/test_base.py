from __future__ import print_function
import unittest
import json
import requests
import os

from upload_ssr import Upload_SSR

import openapi_client
from openapi_client.rest import ApiException

from openapi_client.rest import RESTResponse

from openapi_client.api_client import ApiClient

from remote_backbone_dao import RemoteBackboneDAO
from local_backbone_dao import LocalBackboneDAO


class MockResponse:
    def __init__(self, json_data, status_code):
        self.data = json_data
        self.status = status_code
        self.reason = ''

class TestBase(unittest.TestCase):


    username = None
    _api_client = None
    _auth_token = None
    _configuration = None
    _dao = None

    _config_file = '../config_dev.json'

    _locations = []

    @classmethod
    def getApiClient(self):
        auth_token = None
        configuration = openapi_client.Configuration()

        if os.getenv('TOKEN_URL') and not os.getenv('BB_NOAUTH'):
            if TestBase._auth_token:
                configuration.access_token = TestBase._auth_token
            else:
                try:
                    with open(self._config_file) as json_file:
                        args = json.load(json_file)
                        r = requests.get(os.getenv('TOKEN_URL'), args, headers = { 'service': 'http://localhost/' })
                        at = r.text.split('=')
                        token = at[1].split('&')[0]
                        auth_token = token
                        if 'debug' in args:
                            configuration.debug = args['debug']
                        if 'dao_type' in args:
                            if args['dao_type'] == 'remote':
                                TestBase.username = args['uid']
                    configuration.access_token = auth_token
                    TestBase._auth_token = auth_token
                except FileNotFoundError as fnfe:
                    print('No config file found: {}'.format(TestBase._config_file))
                    pass

        if os.getenv('REMOTE_HOST_URL'):
            configuration.host = os.getenv('REMOTE_HOST_URL')

        TestBase._configuration = configuration

        api_client = openapi_client.ApiClient(configuration)

        return api_client

    @classmethod
    def getDAO(self):
        dao = RemoteBackboneDAO()

        if os.getenv('LOCAL_TEST'):
            dao = LocalBackboneDAO('upload_test',
                                   ['cn=editor,ou=sims,ou=projects,ou=groups,dc=malariagen,dc=net',
                                    'cn=all_studies,ou=sims,ou=projects,ou=groups,dc=malariagen,dc=net'])
        else:
            dao.create_apis(TestBase._configuration)

        return dao

    """
    """
    def setUp(self):

        self._api_client = TestBase.getApiClient()
        self._dao = TestBase.getDAO()

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
        event_api_instance = openapi_client.SamplingEventApi(TestBase.getApiClient())
        if event.location_id and event.location_id not in locations:
            locations.append(event.location_id)

        if event.proxy_location_id:
            if event.proxy_location_id in locations:
                #Need to ensure proxy locations are at the end
                locations.remove(event.proxy_location_id)
                locations.append(event.proxy_location_id)
            else:
                locations.append(event.proxy_location_id)
        TestBase.getDAO().delete_sampling_event(event.sampling_event_id)

    """
    """
    @classmethod
    def deleteEventSets(self, event_sets, locations):

        sampling_events = []
        sampling_event_ids = []
        original_sample_ids = []
        original_samples = []
        for event_set in event_sets:
            test_os = TestBase.getDAO().download_original_samples_by_event_set(event_set)
            for os in test_os.original_samples:
                if os.sampling_event_id not in sampling_event_ids:
                    event = test_os.sampling_events[os.sampling_event_id]
                    if event.event_sets and len(event.event_sets) == 1:
                        sampling_events.append(event)
                        sampling_event_ids.append(os.sampling_event_id)
                if os.original_sample_id not in original_sample_ids:
                    original_sample_ids.append(os.original_sample_id)
                    original_samples.append(os)

            test_events = TestBase.getDAO().download_sampling_events_by_event_set(event_set)

            for event in test_events.sampling_events:
                TestBase.getDAO().delete_event_set_item(event_set,
                                                        event.sampling_event_id)
                if event.event_sets and len(event.event_sets) == 1:
                    if event.sampling_event_id not in sampling_event_ids:
                        sampling_events.append(event)
                        sampling_event_ids.append(event.sampling_event_id)

        for os in original_samples:
            TestBase.getDAO().delete_original_sample(os.original_sample_id)

        for event in sampling_events:
            TestBase.deleteSamplingEvent(event, locations)

        for event_set in event_sets:
            TestBase.getDAO().delete_event_set(event_set)

    """
    """
    @classmethod
    def removeManifestItems(self, manifests):

        for manifest in manifests:
            manifest_detail = TestBase.getDAO().download_manifest(manifest)
            for mi in manifest_detail.members.manifest_items:
                TestBase.getDAO().delete_manifest_item(manifest,
                                                       mi.manifest_item_id)

            TestBase.getDAO().delete_manifest(manifest)

    """
    """
    @classmethod
    def deleteStudies(self, studies, locations):

        event_api_instance = openapi_client.SamplingEventApi(TestBase.getApiClient())

        for study in studies:
            test_events = TestBase.getDAO().download_sampling_events_by_study(study)

            for event in test_events.sampling_events:
                TestBase.deleteSamplingEvent(event, locations)
    """
    """
    @classmethod
    def tearDownSSR(self, event_sets, locations):

        TestBase.deleteEventSets(event_sets + ['TestSSR', 'Report', 'Sequencescape', 'PV4', 'PF27', 'Ag'],
                                 locations)

        TestBase.deleteStudies(['9050', '9051'], locations)

    """
    """
    @classmethod
    def tearDownLocations(self, locations):
        location_api_instance = openapi_client.LocationApi(TestBase.getApiClient())

        for loc in locations:
            if loc:
                TestBase.getDAO().delete_location(loc)
