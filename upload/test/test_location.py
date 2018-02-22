from test_base import TestBase

import difflib

import datetime
import json

from uploader import Uploader

import swagger_client
from swagger_client.rest import ApiException

class TestLocation(TestBase):


    _locations = []

    """
    """
    @classmethod
    def setUpClass(self):

        super(TestLocation, self).setUpClass()
        sd = Uploader(self._config_file)
        sd.use_message_buffer = True
        json_data = json.loads('''{
            "values": {
                "sample_oxford_id": {
                    "column": 0,
                    "type": "string"
                },
                "study_id": {
                    "column": 1,
                    "type": "string"
                },
                "latitude": {
                    "column": 2,
                    "type": "float"
                },
                "longitude": {
                    "column": 3,
                    "type": "float"
                },
                "location_name": {
                    "column": 4,
                    "type": "string"
                },
                "country": {
                    "column": 5,
                    "type": "string"
                },
                "proxy_latitude": {
                    "column": 6,
                    "type": "float"
                },
                "proxy_longitude": {
                    "column": 7,
                    "type": "float"
                },
                "proxy_location_name": {
                    "column": 8,
                    "type": "string"
                }
            }
        }''')
        sd.load_data_file(json_data, 'locations.tsv')

        self._messages = sd.message_buffer


    """
    """
    @classmethod
    def tearDownClass(self):

        event_api_instance = swagger_client.SamplingEventApi(self._api_client)

        for study in ['9040', '9041', '9042']:
            test_events = event_api_instance.download_sampling_events_by_study(study)

            for event in test_events.sampling_events:
                event_api_instance.delete_sampling_event(event.sampling_event_id)

        location_api_instance = swagger_client.LocationApi(self._api_client)

        api_instance = swagger_client.EventSetApi(self._api_client)

        api_instance.delete_event_set('locations')

        for loc in self._locations:
            location_api_instance.delete_location(loc)


    """
    """
    def test_location_duplicate_name(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:
            looked_up = api_instance.download_sampling_event_by_identifier('oxford_id', '22345')
            looked_up = looked_up.sampling_events[0]
            errmsg = "Location name conflict\t9040\tRatanakiri\t{'accuracy': None,\n 'country': 'KHM',\n 'curated_name': None,\n 'curation_method': None,\n 'identifiers': [" +\
                    "{'identifier_source': 'locations',\n                  " +\
                    "'identifier_type': 'partner_name',\n                  " +\
                    "'identifier_value': 'Ratanakiri',\n                  'study_name': '9040'}" +\
                "],\n 'latitude': 13.86208,\n " +\
"'location_id': '{}'".format(looked_up.location_id) +\
",\n 'longitude': 107.097015,\n 'notes': 'locations.tsv'}\t13.9\t107.1\t[('country', 'KHM'), ('latitude', '13.86208'), ('location_name', 'Ratanakiri'), ('longitude', '107.097015'), ('proxy_latitude', '13.9'), ('proxy_location_name', 'Ratanakiri'), ('proxy_longitude', '107.1'), ('sample_oxford_id', '22345'), ('study_id', '9040 Upload location test study')]"
            #Used for diagnosis - may not be _messages[0]
            #print('\n'.join(difflib.context_diff(errmsg.split('\n'), self._messages[0].split('\n'))))
            self.assertIn(errmsg, self._messages)
            self.assertIsNone(looked_up.proxy_location_id)
            self.assertIsNone(looked_up.proxy_location)

            if looked_up.location_id not in self._locations:
                self._locations.append(looked_up.location_id)

        except ApiException as error:
            self.fail("test_location_duplicate_name: Exception when calling download_sampling_event_by_identifier {}"
                        .format(error))


    """
    """
    def test_location_duplicate_name_ok(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:
            looked_up = api_instance.download_sampling_event_by_identifier('oxford_id', '22346')
            looked_up = looked_up.sampling_events[0]

            self.assertIsNotNone(looked_up.location_id)

            if looked_up.location_id not in self._locations:
                self._locations.append(looked_up.location_id)

            looked_up = api_instance.download_sampling_event_by_identifier('oxford_id', '22347')
            looked_up = looked_up.sampling_events[0]

            self.assertIsNotNone(looked_up.location_id)

            if looked_up.location_id not in self._locations:
                self._locations.append(looked_up.location_id)

        except ApiException as error:
            self.fail("test_location_duplicate_name: Exception when calling download_sampling_event_by_identifier {}"
                        .format(error))

    """
    """
    def test_location_duplicate_gps_simple(self):

        errmsg = '''duplicate location      9040    Not Ratanakiri  13.86208        107.097015      13.86208        107.097015
Probable conflict with {'accuracy': None,
 'country': 'KHM',
 'curated_name': None,
 'curation_method': None,
 'identifiers': [{'identifier_source': 'locations',
                  'identifier_type': 'partner_name',
                  'identifier_value': 'Not Ratanakiri',
                  'study_name': '9042'},
                 {'identifier_source': 'locations',
                  'identifier_type': 'partner_name',
                  'identifier_value': 'Ratanakiri',
                  'study_name': '9040'}],
 'latitude': 13.86208,
 'location_id': '6a33d4e8-3e3a-4a3d-88c6-3a3de1e578e7',
 'longitude': 107.097015,
 'notes': 'locations.tsv'}      [('country', 'KHM'), ('latitude', '13.86208'), ('location_name', 'Not Ratanakiri'), ('longitude', '107.097015'), ('proxy_latitude', ''), ('proxy_longitude', ''), ('sample_oxford_id', '22349'), ('study_id', '9040 Upload location test study')]'''
        self.assertIn(errmsg, self._messages)

    """
    """
    def test_location_duplicate_gps_simple(self):
        errmsg = '''duplicate location\t9040\tDuplicate GPS Ratanakiri\t13.86208\t107.097015\tRatanakiri\t[('country', 'KHM'), ('latitude', '13.86208'), ('location_name', 'Duplicate GPS Ratanakiri'), ('longitude', '107.097015'), ('proxy_latitude', ''), ('proxy_longitude', ''), ('sample_oxford_id', '22350'), ('study_id', '9040 Upload location test study')]'''
        self.assertIn(errmsg, self._messages)
