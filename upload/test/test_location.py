from test_base import TestBase

import difflib

import datetime
import json

from uploader import Uploader

import swagger_client
from swagger_client.rest import ApiException

class TestLocation(TestBase):

    _locations = []

    _ag_json = '''
{
    "values": {
        "sample_oxford_id": {
            "column": 1,
            "type": "string"
        },
        "sample_partner_id": {
            "column": 2,
            "type": "string"
        },
        "doc": {
            "column": 9,
            "type": "datetime",
            "date_format": "%Y"
        },
        "location_name": {
            "column": 6,
            "type": "string"
        },
        "country": {
            "column": 5,
            "type": "string"
        },
       "latitude": {
            "column": 14,
            "type": "float"
        },
        "longitude": {
            "column": 15,
            "type": "float"
        }
    }
}
    '''

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

        self.setUpSSR()

        sd = Uploader(self._config_file)
#        sd.use_message_buffer = True
        json_data = json.loads(self._ag_json)
        sd.load_data_file(json_data, 'loc_no_study.tsv')

    """
    """
    @classmethod
    def tearDownClass(self):

        locations = TestLocation._locations

        event_api_instance = swagger_client.SamplingEventApi(self._api_client)

        self.deleteStudies(['9040', '9041', '9042'], locations)

        self.deleteEventSets(['locations', 'loc_no_study'], locations)

        self.tearDownSSR(locations)
        self.tearDownLocations(locations)


    """
    """
    def test_location_duplicate_name(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:
            looked_up = api_instance.download_sampling_events_by_identifier('oxford_id', '22345')
            looked_up = looked_up.sampling_events[0]

            errmsg = "Conflicting Location name value\tRatanakiri\t\t\t{'accuracy': None, 'country': None, 'curated_name': None, 'curation_method': None, 'identifiers': [{'identifier_source': 'locations', 'identifier_type': 'partner_name', 'identifier_value': 'Ratanakiri', 'study_name': '9040'}], 'latitude': 13.9, 'location_id': None, 'longitude': 107.1, 'notes': 'locations.tsv'}\t{'accuracy': None, 'country': 'KHM', 'curated_name': None, 'curation_method': None, 'identifiers': [{'identifier_source': 'locations', 'identifier_type': 'partner_name', 'identifier_value': 'Ratanakiri', 'study_name': '9040'}], 'latitude': 13.86208, " +\
                     "'location_id': '{}',".format(looked_up.location_id) +\
                     " 'longitude': 107.097015, 'notes': 'locations.tsv'}\t[('country', 'KHM'), ('latitude', '13.86208'), ('location_name', 'Ratanakiri'), ('longitude', '107.097015'), ('proxy_latitude', '13.9'), ('proxy_location_name', 'Ratanakiri'), ('proxy_longitude', '107.1'), ('sample_oxford_id', '22345'), ('study_id', '9040 Upload location test study')]"

            #Used for diagnosis
            #for msg in self._messages:
            #    if msg.startswith(errmsg[:25]):
            #        print('\n'.join(difflib.context_diff(errmsg.split('\n'), msg.split('\n'))))
            self.assertIn(errmsg, self._messages)
            self.assertIsNone(looked_up.proxy_location_id)
            self.assertIsNone(looked_up.proxy_location)

            if looked_up.location_id not in TestLocation._locations:
                TestLocation._locations.append(looked_up.location_id)

        except ApiException as error:
            self.fail("test_location_duplicate_name: Exception when calling download_sampling_event_by_identifier {}"
                        .format(error))


    """
    """
    def test_location_duplicate_name_ok(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:
            looked_up = api_instance.download_sampling_events_by_identifier('oxford_id', '22346')
            looked_up = looked_up.sampling_events[0]

            self.assertIsNotNone(looked_up.location_id)

            if looked_up.location_id not in TestLocation._locations:
                TestLocation._locations.append(looked_up.location_id)

            looked_up = api_instance.download_sampling_events_by_identifier('oxford_id', '22347')
            looked_up = looked_up.sampling_events[0]

            self.assertIsNotNone(looked_up.location_id)

            if looked_up.location_id not in TestLocation._locations:
                TestLocation._locations.append(looked_up.location_id)

        except ApiException as error:
            self.fail("test_location_duplicate_name_ok: Exception when calling download_sampling_event_by_identifier {}"
                        .format(error))

    """
    """
    def test_location_duplicate_gps_simple(self):

        api_instance = swagger_client.LocationApi(self._api_client)

        loc = api_instance.download_gps_location(str(13.86208),str(107.097015))

        errmsg = "Conflicting Location name value\tduplicate location::Duplicate GPS Ratanakiri:Ratanakiri\t\t\t{'accuracy': None, 'country': 'KHM', 'curated_name': None, 'curation_method': None, 'identifiers': [{'identifier_source': 'locations', 'identifier_type': 'partner_name', 'identifier_value': 'Not Ratanakiri', 'study_name': '9042'}, {'identifier_source': 'locations', 'identifier_type': 'partner_name', 'identifier_value': 'Ratanakiri', 'study_name': '9040'}, {'identifier_source': 'locations', 'identifier_type': 'partner_name', 'identifier_value': 'Duplicate GPS Ratanakiri', 'study_name': '9040'}], 'latitude': 13.86208, " +\
                 "'location_id': '{}',".format(loc.location_id) +\
                 " 'longitude': 107.097015, 'notes': 'locations.tsv'}\t{'accuracy': None, 'country': 'KHM', 'curated_name': None, 'curation_method': None, 'identifiers': [{'identifier_source': 'locations', 'identifier_type': 'partner_name', 'identifier_value': 'Not Ratanakiri', 'study_name': '9042'}, {'identifier_source': 'locations', 'identifier_type': 'partner_name', 'identifier_value': 'Ratanakiri', 'study_name': '9040'}], 'latitude': 13.86208, " +\
                 "'location_id': '{}',".format(loc.location_id) +\
                 " 'longitude': 107.097015, 'notes': 'locations.tsv'}\t[('country', 'KHM'), ('latitude', '13.86208'), ('location_name', 'Duplicate GPS Ratanakiri'), ('longitude', '107.097015'), ('proxy_latitude', ''), ('proxy_longitude', ''), ('sample_oxford_id', '22350'), ('study_id', '9040 Upload location test study')]"
            #Used for diagnosis
        for msg in self._messages:
            if msg.startswith(errmsg[:71]):
                print('\n'.join(difflib.context_diff(errmsg.split('[\n\t\{]'), msg.split('[\n\t\{]'))))

        self.assertIn(errmsg, self._messages)


    """
    """
    def test_location_name_study(self):
        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:
            looked_up = api_instance.download_sampling_events_by_identifier('oxford_id', 'AG0001-C')
            looked_up = looked_up.sampling_events[0]

            self.assertIsNotNone(looked_up.location)

            self.assertEqual(looked_up.location.identifiers[0].study_name[:4], looked_up.study_name[:4])

            if looked_up.location_id not in TestLocation._locations:
                TestLocation._locations.append(looked_up.location_id)

        except ApiException as error:
            self.fail("test_location_name_study: Exception when calling download_sampling_events_by_identifier {}"
                        .format(error))

