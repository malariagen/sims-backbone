from test_base import TestBase


import json

from uploader import Uploader
from upload_roma import Upload_ROMA

import swagger_client
from swagger_client.rest import ApiException

class TestMerge(TestBase):



    """
    """
    @classmethod
    def setUpClass(self):

        super(TestMerge, self).setUpClass()
        sd = Uploader(self._config_file)
        sd.use_message_buffer = True

        json_data = json.loads('''{
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
}''')
        sd.load_data_file(json_data, 'merge_oxford.tsv')

        self._messages = sd.message_buffer

    """
    """
    @classmethod
    def tearDownClass(self):

        event_api_instance = swagger_client.SamplingEventApi(self._api_client)

        looked_up = event_api_instance.download_sampling_event_by_identifier('oxford_id',
                                                                             'EXTST000002')

        event_api_instance.delete_sampling_event(looked_up.sampling_event_id)

    """
    """
    def test_merge(self):

        el = Upload_ROMA(self._config_file)
        el.use_message_buffer = True
        el.load_data_file('roma_dump.20180116103346.json')


        sd = Uploader(self._config_file)
        sd.use_message_buffer = True

        json_data = json.loads('''{
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
}''')
        sd.load_data_file(json_data, 'merge_sanger_lims.tsv')

        event_api_instance = swagger_client.SamplingEventApi(self._api_client)

        looked_up = event_api_instance.download_sampling_event_by_identifier('oxford_id',
                                                                             'EXTST000002')

        msg = "Merging into {} ".format(looked_up.sampling_event_id) +\
                "[{'identifier_source': 'merge_oxford',\n 'identifier_type': 'oxford_id',\n 'identifier_value': 'EXTST000002',\n 'study_name': None}, {'identifier_source': 'merge_oxford',\n 'identifier_type': 'alt_oxford_id',\n 'identifier_value': '216714',\n 'study_name': None}, {'identifier_source': 'merge_oxford',\n 'identifier_type': 'partner_id',\n 'identifier_value': '53920',\n 'study_name': None}] using oxford_id\t[('sample_lims_id', 'TEAM112_0000000001'), ('sample_source_id', 'TST00002'), ('sample_source_id1', 'EXTST000002'), ('sample_source_id2', 'OX0001-C'), ('sample_source_type', 'roma_id'), ('sample_source_type1', 'oxford_id'), ('sample_source_type2', 'oxford_id'), ('study_id', '0000-Unknown'), ('unique_id', '19465')]"
        self.assertIn(msg, sd.message_buffer)

        self.assertEquals(looked_up.study_id, '9030')

        ident = swagger_client.Identifier(identifier_source='roma_dump',
                                          identifier_type='oxford_id', identifier_value='OX0001-C')

        self.assertIn(ident, looked_up.identifiers)

        ident = swagger_client.Identifier(identifier_source='roma_dump',
                                          identifier_type='partner_id',
                                          identifier_value='EXTST000002')

        self.assertIn(ident, looked_up.identifiers)

        ident = swagger_client.Identifier(identifier_source='merge_oxford',
                                          identifier_type='alt_oxford_id',
                                          identifier_value='216714')

        self.assertIn(ident, looked_up.identifiers)

        ident = swagger_client.Identifier(identifier_source='merge_sanger_lims',
                                          identifier_type='oxford_id',
                                          identifier_value='EXTST000002')

        self.assertIn(ident, looked_up.identifiers)

        self.assertEquals(looked_up.partner_species, 'Plasmodium falciparum')

        self.assertEquals(looked_up.location.latitude, 12.5)
