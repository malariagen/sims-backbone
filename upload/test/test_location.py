from test_base import TestBase

import difflib

import datetime
import json

from uploader import Uploader

import openapi_client
from openapi_client.rest import ApiException

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

        self.tearDownSSR(['locations', 'loc_no_study'], locations)
        self.deleteStudies(['9040', '9041', '9042'], locations)

        self.tearDownLocations(locations)


    """
    """
    def test_location_duplicate_name(self):


        try:
            conflict_loc = self._dao.download_gps_location('13.86208','107.097015')
            results = self._dao.download_sampling_events_by_os_attr('oxford_id', '22345')
            looked_up = results.sampling_events[0]
            assert looked_up.location_id != looked_up.proxy_location_id
            location = results.locations[looked_up.location_id]
            proxy_location = results.locations[looked_up.proxy_location_id]
            assert location.attrs[0].attr_value == 'Ratanakiri'
            assert proxy_location.attrs[0].attr_value == 'Ratanakiri'

            assert location.latitude == 13.86208
            assert proxy_location.latitude == 13.9

            if looked_up.location_id not in TestLocation._locations:
                TestLocation._locations.append(looked_up.location_id)
            if looked_up.proxy_location_id not in TestLocation._locations:
                TestLocation._locations.append(looked_up.proxy_location_id)

        except ApiException as error:
            self.fail("test_location_duplicate_name: Exception when calling download_sampling_event_by_attr {}"
                        .format(error))


    """
    """
    def test_location_duplicate_name_ok(self):


        try:
            looked_up = self._dao.download_sampling_events_by_os_attr('oxford_id', '22346')
            looked_up = looked_up.sampling_events[0]

            self.assertIsNotNone(looked_up.location_id)

            if looked_up.location_id not in TestLocation._locations:
                TestLocation._locations.append(looked_up.location_id)

            looked_up = self._dao.download_sampling_events_by_os_attr('oxford_id', '22347')
            looked_up = looked_up.sampling_events[0]

            self.assertIsNotNone(looked_up.location_id)

            if looked_up.location_id not in TestLocation._locations:
                TestLocation._locations.append(looked_up.location_id)
            if looked_up.proxy_location_id not in TestLocation._locations:
                TestLocation._locations.append(looked_up.proxy_location_id)

        except ApiException as error:
            self.fail("test_location_duplicate_name_ok: Exception when calling download_sampling_event_by_attr {}"
                        .format(error))

    """
    """
    def test_location_duplicate_gps_simple(self):


        locs = self._dao.download_gps_location(str(13.86208),str(107.097015))

        assert locs.count == 4

        #print(locs)

        for looked_up in locs.locations:
            if looked_up.location_id not in TestLocation._locations:
                TestLocation._locations.append(looked_up.location_id)

    """
    """
    def test_location_name_study(self):

        try:
            original_sample = self._dao.download_original_samples_by_attr('oxford_id',
                                                                          'AG0001-C').original_samples[0]
            looked_up = self._dao.download_sampling_event(original_sample.sampling_event_id)

            self.assertIsNotNone(looked_up.location)

            self.assertEqual(looked_up.location.attrs[0].study_name[:4], original_sample.study_name[:4])

            if looked_up.location_id not in TestLocation._locations:
                TestLocation._locations.append(looked_up.location_id)

        except ApiException as error:
            self.fail("test_location_name_study: Exception when calling download_sampling_events_by_attr {}"
                        .format(error))

