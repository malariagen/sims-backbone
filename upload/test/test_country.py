from test_base import TestBase

import difflib
import urllib

import datetime
import json

from uploader import Uploader
from set_country import SetCountry
from upload_ssr import Upload_SSR

import openapi_client
from openapi_client.rest import ApiException

class TestCountry(TestBase):

    _locations = []

    """
    """
    @classmethod
    def setUpClass(self):

        super(TestCountry, self).setUpClass()

        sd = Uploader(self._config_file)
        json_data = json.loads('''
{
    "values": {
        "unique_id": {
            "column": 2,
            "type": "string"
        },
        "sample_oxford_id": {
            "column": 3,
            "type": "string"
        },
        "sample_alternate_oxford_id": {
            "column": 4,
            "type": "string"
        },
        "sample_source_id": {
            "column": 6,
            "type": "string"
        },
        "sample_source_type": {
            "column": 8,
            "type": "string"
        },
        "species": {
            "column": 11,
            "type": "string"
        }
    }
}
        ''')
        sd.load_data_file(json_data, 'oxford_country.tsv')


        self.setUpSSR()

        sd = Uploader(self._config_file)
        json_data = json.loads('''{
    "values":
    {
        "sample_oxford_id": {
            "column": 0,
            "type": "string",
            "id": true
        },
        "study_id": {
            "column": 1,
            "type": "string"
        },
        "sample_partner_id": {
            "column": 2,
            "type": "string"
        },
        "location_name": {
            "column": 13,
            "type": "string"
        },
        "latitude": {
            "column": 14,
            "type": "float",
            "regex": "^\\\\s*([-0-9]*\\\\.?\\\\d{0,7})"
        },
        "longitude": {
            "column": 14,
            "type": "float",
            "regex": "([-0-9]*\\\\.?\\\\d{0,7})(\\\\d*)$"
        },
        "country": {
            "column": 5,
            "type": "string",
            "replace": [
                        [ "Madagascar", "MDG" ]
                    ]

        },
        "proxy_country": {
            "column": 5,
            "type": "string",
            "replace": [
                        [ "Madagascar", "MDG" ]
                    ]

        },
        "proxy_location_name": {
            "column": 6,
            "type": "string"
        },
        "proxy_latitude": {
            "column": 7,
            "type": "float",
            "regex": "^\\\\s*([-0-9]*\\\\.?\\\\d{0,7})"
        },
        "proxy_longitude": {
            "column": 7,
            "type": "float",
            "regex": "([-0-9]*\\\\.?\\\\d{0,7})\\\\d*$"
        },
        "doc": {
            "column": 8,
            "type": "datetime",
            "date_format": "%Y-%m-%d"
        }

    }
}''')

        sd.load_data_file(json_data, 'countries.tsv')

        sd = SetCountry(self._config_file)
        sd.use_message_buffer = True
        sd._countries_file = '../' + sd._countries_file

        id_type = 'oxford_id'
        input_file = 'oxford_country.tsv'
        id_column = 3
        country_column = 10
        ssr = 'TestSSR.xls'
        sd.load_location_cache()
        sd.set_countries(input_file, id_type, id_column, country_column)

        sheets = None
        sd.load_data_file(ssr, sheets)

        self._messages = sd.message_buffer
        #print('\n'.join(self._messages))
    """
    """
    @classmethod
    def tearDownClass(self):

        locations = TestCountry._locations

        self.tearDownSSR(['countries', 'oxford_country'], locations)
        self.deleteStudies(['9052', '0000', '9060'], locations)

        self.tearDownLocations(locations)
        pass

    """
    """
    def test_country_specific(self):

        try:
            original_sample = self._dao.download_original_samples('attr:partner_id:MDG/TST_0001').original_samples[0]
            looked_up = self._dao.download_sampling_event(original_sample.sampling_event_id)

            #print(looked_up)
            self.assertEqual(looked_up.proxy_location.country, 'MDG')
            self.assertEqual(looked_up.proxy_location.latitude, -19.0)
            self.assertEqual(looked_up.proxy_location.longitude, 47.0)
            self.assertEqual(looked_up.proxy_location.attrs[0].attr_value, 'Madagascar')
            self.assertEqual(looked_up.location.country, 'MDG')
            self.assertEqual(looked_up.location.latitude, -16.94223)
            self.assertEqual(looked_up.location.longitude, 46.83144)
            for ident in looked_up.location.attrs:
                if ident.study_name[:4] == original_sample.study_name[:4]:
                    self.assertEqual(ident.attr_value, 'Maevatanana')
            self.assertEqual(original_sample.study_name[:4], '9050')

            if looked_up.location_id not in TestCountry._locations:
                TestCountry._locations.append(looked_up.location_id)
            if looked_up.proxy_location_id not in TestCountry._locations:
                TestCountry._locations.append(looked_up.proxy_location_id)

        except ApiException as error:
            self.fail("test_location_duplicate_name: Exception when calling download_sampling_events_by_attr {}"
                        .format(error))

    """
    """
    def test_country_from_oxford(self):

        try:
            looked_up = self._dao.download_sampling_events_by_os_attr('oxford_id',
                                                                      'CT0003-C')
            locations = looked_up.locations
            looked_up = looked_up.sampling_events[0]
            location = locations[looked_up.location_id]

            self.assertEqual(location.country, 'BEN')
            self.assertEqual(location.latitude, 9.30769)
            self.assertEqual(location.longitude, 2.315834)
            if looked_up.location_id not in TestCountry._locations:
                TestCountry._locations.append(looked_up.location_id)
        except ApiException as error:
            self.fail("test_location_duplicate_name: Exception when calling download_sampling_events_by_attr {}"
                        .format(error))

    """
    """
    def test_country_from_ssr(self):

        try:
            looked_up = self._dao.download_sampling_events_by_os_attr('oxford_id',
                                                                           'CT0002-C')

            locations = looked_up.locations
            looked_up = looked_up.sampling_events[0]
            location = locations[looked_up.location_id]
#            print(looked_up)
            self.assertEqual(location.country, 'MDG')
            self.assertEqual(location.latitude, -18.766947)
            self.assertEqual(location.longitude, 46.869107)
            if looked_up.location_id not in TestCountry._locations:
                TestCountry._locations.append(looked_up.location_id)
        except ApiException as error:
            self.fail("test_country_from_ssr: Exception when calling download_sampling_event_by_attr {}"
                        .format(error))

    """
    """
    def test_country_mismatch(self):

        try:

            original_samples = self._dao.download_original_samples('attr:partner_id:MDG/TST_0004')
            original_sample = original_samples.original_samples[0]
            looked_up = original_samples.sampling_events[original_sample.sampling_event_id]

            self.assertEqual(looked_up.proxy_location.country, 'MDG')
            self.assertEqual(looked_up.proxy_location.latitude, -19.0)
            self.assertEqual(looked_up.proxy_location.longitude, 47.0)
            self.assertEqual(looked_up.proxy_location.attrs[0].attr_value, 'Madagascar')

            msgs = [
                "Conflicting Country value\tnot updated {{'accuracy': None, 'attrs': [{{'attr_source': 'countries', 'attr_type': 'partner_name', 'attr_value': 'Maevatanana', 'study_name': '9052'}}], 'country': 'MDG', 'curated_name': None, 'curation_method': None, 'latitude': -16.94223, 'location_id': '{location_id}', 'longitude': 46.83144, 'notes': 'countries', 'proxy_location': {proxy_location}, 'proxy_location_id': '{proxy_location_id}', 'version': 1}}\t{event_id}\t\tMDG\tIN\t[('id_value', 'CT0004-C')]".format(location_id=looked_up.location_id,
                event_id=looked_up.sampling_event_id, proxy_location=None,
                proxy_location_id=looked_up.proxy_location_id),
                "Conflicting Country value\tproxy not updated {{'accuracy': None, 'attrs': [{{'attr_source': 'countries', 'attr_type': 'partner_name', 'attr_value': 'Madagascar', 'study_name': '9052'}}], 'country': 'MDG', 'curated_name': None, 'curation_method': None, 'latitude': -19.0, 'location_id': '{location_id}', 'longitude': 47.0, 'notes': 'countries', 'proxy_location': None, 'proxy_location_id': None, 'version': 1}}\t{event_id}\t\tMDG\tIN\t[('id_value', 'CT0004-C')]".format(location_id=looked_up.proxy_location_id, event_id=looked_up.sampling_event_id)
            ]

            for msg in msgs:
                self.assertIn(msg, self._messages)

            self.assertEqual(looked_up.location.country, 'MDG')
            self.assertEqual(looked_up.location.latitude, -16.94223)
            self.assertEqual(looked_up.location.longitude, 46.83144)
            for ident in looked_up.location.attrs:
                if ident.study_name[:4] == original_sample.study_name[:4]:
                    self.assertNotEqual(ident.attr_value, 'India')
            self.assertEqual(original_sample.study_name[:4], '9052')
            if looked_up.location_id not in TestCountry._locations:
                TestCountry._locations.append(looked_up.location_id)
        except ApiException as error:
            self.fail("test_country_mismatch: Exception when calling download_sampling_event_by_attr {}"
                      .format(error))
