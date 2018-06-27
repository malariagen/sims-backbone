from test_base import TestBase


import json

from uploader import Uploader
from upload_roma import Upload_ROMA

import swagger_client
from swagger_client.rest import ApiException

class TestMerge(TestBase):

    _locations = []

    _oxford_config = '''{
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
}'''

    _pv_3_config = '''
{
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
            "column": 9,
            "type": "string"
        },
        "latitude": {
            "column": 14,
            "type": "float",
            "regex": "^\\\s*([-0-9]*\\\.?\\\d{0,9})"
        },
        "longitude": {
            "column": 14,
            "type": "float",
            "regex": "([-0-9]*\\\.?\\\d{0,9})(\\\d*)$"
        },
        "country": {
            "column": 5,
            "type": "string",
            "replace": [
                        [ "Vietnam", "VNM" ]
                    ]

        },
        "proxy_location_name": {
            "column": 6,
            "type": "string"
        },
        "proxy_latitude": {
            "column": 7,
            "type": "float",
            "regex": "^\\\s*([-0-9]*\\\.?\\\d{0,9})"
        },
        "proxy_longitude": {
            "column": 7,
            "type": "float",
            "regex": "([-0-9]*\\\.?\\\d{0,9})\\\d*$"
        },
        "doc": {
            "column": 8,
            "type": "datetime",
            "date_format": "%Y-%m-%d"
        }

    }
}
    '''

    _sanger_lims_config = '''{
    "values": {
        "sample_lims_id": {
            "column": 0,
            "type": "string"
        },
        "unique_id": {
            "column": 1,
            "type": "string"
        },
        "sample_source_id": {
            "column": 3,
            "type": "string"
        },
        "sample_source_type": {
            "column": 4,
            "type": "string",
            "replace": [
               [ "parner_id", "partner_id" ]
            ]
        },
        "sample_source_id1": {
            "column": 6,
            "type": "string"
        },
        "sample_source_type1": {
            "column": 7,
            "type": "string",
            "replace": [
               [ "parner_id", "partner_id" ]
            ]
        },
        "sample_source_id2": {
            "column": 8,
            "type": "string"
        },
        "sample_source_type2": {
            "column": 9,
            "type": "string",
            "replace": [
               [ "parner_id", "partner_id" ]
            ]
        }
    }
}'''

    """
    """
    @classmethod
    def setUpClass(self):

        super(TestMerge, self).setUpClass()

        sd = Uploader(self._config_file)
        sd.use_message_buffer = True

        json_data = json.loads(self._oxford_config)

        sd.load_data_file(json_data, 'merge_oxford.tsv')

        self._messages = sd.message_buffer

        self.setUpSSR()

        sd = Uploader(self._config_file)
        sd.use_message_buffer = True

        json_data = json.loads('''{
    "values":
    {
        "sample_oxford_id": {
            "column": 0,
            "type": "string",
            "id": true
        },
        "sample_partner_id": {
            "column": 1,
            "type": "string"
        },
        "study_id": {
            "column": 4,
            "type": "string"
        },
        "type": {
            "column": 5,
            "type": "string"
        },
        "location_name": {
            "column": 6,
            "type": "string"
        },
       "latitude": {
            "column": 7,
            "type": "float"
        },
        "longitude": {
            "column": 8,
            "type": "float"
        },
        "doc": {
            "column": 9,
            "type": "datetime",
            "date_format": "%Y-%m-%d",
            "comment": "inconsistent date format"
        },
        "year": {
            "column": 10,
            "type": "datetime",
            "date_format": "%Y"
        }
    }
}''')

        sd.load_data_file(json_data, 'merge_pf_6.tsv')
        sd1 = Uploader(self._config_file)
        sd1.use_message_buffer = True

        json_data = json.loads(self._pv_3_config)

        sd1.load_data_file(json_data, 'merge_pv_3.tsv')

        el = Upload_ROMA(self._config_file)
        el.use_message_buffer = True
        el.load_data_file('roma_dump.20180116103346.json')

        sd = Uploader(self._config_file)
        sd.use_message_buffer = True

        json_data = json.loads(self._sanger_lims_config)

        sd.load_data_file(json_data, 'merge_sanger_lims.tsv')
    """
    """
    @classmethod
    def tearDownClass(self):

        locations = TestMerge._locations

        event_api_instance = swagger_client.SamplingEventApi(TestBase.getApiClient())
        os_api_instance = swagger_client.OriginalSampleApi(TestBase.getApiClient())

        for oxid in ['EXTST000002', 'OF0093-C', 'OV0050-C', 'CT0001-C', 'CT0002-C']:
            try:
                looked_up = event_api_instance.download_sampling_events_by_os_attr('oxford_id',
                                                                                 oxid)
                looked_up = looked_up.sampling_events[0]

                self.deleteSamplingEvent(looked_up, locations)

                looked_up = os_api_instance.download_original_samples_by_attr('oxford_id', oxid)
                looked_up = looked_up.original_samples[0]

                os_api_instance.delete_original_sample(looked_up.original_sample_id)

            except ApiException as err:
                print(err)
                pass

        self.deleteStudies(['9030','9031'], locations)

        self.deleteEventSets(['merge_oxford', 'merge_pf_6', 'merge_pv_3', 'roma_dump',
                          'merge_sanger_lims'], locations)

        self.tearDownSSR(locations)
        self.tearDownLocations(locations)

    """
    """
    def test_merge(self):


        os_api_instance = swagger_client.OriginalSampleApi(self._api_client)

        looked_up = os_api_instance.download_original_samples_by_attr('oxford_id',
                                                                             'EXTST000002')
        looked_up = looked_up.original_samples[0]

#        msg = "Merging into {} ".format(looked_up.sampling_event_id) +\
#                "using oxford_id\t[('sample_lims_id', 'TEAM112_0000000001'), ('sample_source_id', 'TST00002'), ('sample_source_id1', 'EXTST000002'), ('sample_source_id2', 'OX0001-C'), ('sample_source_type', 'roma_id'), ('sample_source_type1', 'oxford_id'), ('sample_source_type2', 'oxford_id'), ('study_id', '0000-Unknown'), ('unique_id', '19465')]"
#        self.assertIn(msg, self._messages)
#

        self.assertEquals(looked_up.study_name, '9030')

        ident = swagger_client.Attr(attr_source='roma_dump',
                                          attr_type='oxford_id', attr_value='OX0001-C')

        self.assertIn(ident, looked_up.attrs)

        ident = swagger_client.Attr(attr_source='roma_dump',
                                          attr_type='partner_id',
                                          attr_value='EXTST000002')

        self.assertIn(ident, looked_up.attrs)

        ident = swagger_client.Attr(attr_source='merge_oxford',
                                          attr_type='alt_oxford_id',
                                          attr_value='216714')

        self.assertIn(ident, looked_up.attrs)

        ident = swagger_client.Attr(attr_source='merge_sanger_lims',
                                          attr_type='oxford_id',
                                          attr_value='EXTST000002')

        self.assertIn(ident, looked_up.attrs)

        es_api_instance = swagger_client.SamplingEventApi(self._api_client)

        looked_up = es_api_instance.download_sampling_events_by_os_attr('oxford_id',
                                                                             'EXTST000002')

        looked_up = looked_up.sampling_events[0]

        self.assertEquals(looked_up.partner_species, 'Plasmodium falciparum')

        self.assertEquals(looked_up.location.latitude, 12.5)


    def test_merge_on_partner_id(self):

        event_api_instance = swagger_client.OriginalSampleApi(self._api_client)


#        with self.assertRaises(Exception) as context:
#            looked_up = event_api_instance.download_sampling_event_by_attr('partner_id',
#                                                                             'EXTST000003')

        looked_up1 = event_api_instance.download_original_samples_by_attr('roma_id',
                                                                             'TST00003')
        looked_up1 = looked_up1.original_samples[0]

        looked_up2 = event_api_instance.download_original_samples_by_attr('oxford_id',
                                                                             'OX0008-C')
        looked_up2 = looked_up2.original_samples[0]

        looked_up3 = event_api_instance.download_original_samples_by_attr('oxford_id',
                                                                             'OX0009-C')
        looked_up3 = looked_up3.original_samples[0]

        self.assertEqual(looked_up1.original_sample_id, looked_up2.original_sample_id)

        self.assertNotEqual(looked_up1.original_sample_id, looked_up3.original_sample_id)


    """
    """
    def test_not_merge(self):

        event_api_instance = swagger_client.SamplingEventApi(self._api_client)

        looked_up = event_api_instance.download_sampling_events_by_os_attr('oxford_id',
                                                                             'OF0093-C')
        looked_up = looked_up.sampling_events[0]
        looked_up1 = event_api_instance.download_sampling_events_by_os_attr('oxford_id',
                                                                             'OV0050-C')
        looked_up1 = looked_up1.sampling_events[0]

        self.assertNotEqual(looked_up.sampling_event_id, looked_up1.sampling_event_id)

    """
    """
    def test_not_merge_se(self):

        os_api_instance = swagger_client.OriginalSampleApi(self._api_client)
        looked_up1 = os_api_instance.download_original_samples_by_attr('oxford_id',
                                                                             'OX0009-C')
        looked_up2 = os_api_instance.download_original_samples_by_attr('oxford_id',
                                                                             'OX0010-C')
        looked_up1 = looked_up1.original_samples[0]
        looked_up2 = looked_up2.original_samples[0]

        print(looked_up1)
        print(looked_up2)

        se_api = swagger_client.SamplingEventApi(self._api_client)

        print(se_api.download_sampling_event(looked_up1.sampling_event_id))
        print(se_api.download_sampling_event(looked_up2.sampling_event_id))

        assert looked_up1.sampling_event_id == looked_up2.sampling_event_id

