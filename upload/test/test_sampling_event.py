from test_base import TestBase


import json

from uploader import Uploader

import swagger_client
from swagger_client.rest import ApiException

class TestSampling_Event(TestBase):

    _locations = []

    """
    """
    @classmethod
    def setUpClass(self):

        super(TestSampling_Event, self).setUpClass()
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
                }
            }
        }''')
        sd.load_data_file(json_data, 'multiple_study.tsv')

        self._messages = sd.message_buffer

    """
    """
    @classmethod
    def tearDownClass(self):

        event_api_instance = swagger_client.SamplingEventApi(TestBase.getApiClient())

        looked_up = event_api_instance.download_sampling_events_by_identifier('oxford_id', '123456')
        looked_up = looked_up.sampling_events[0]

        event_api_instance.delete_sampling_event(looked_up.sampling_event_id)

        self.deleteEventSets(['multiple_study'], TestSampling_Event._locations)

    """
    """
    def test_multiple_study(self):


        event_api_instance = swagger_client.SamplingEventApi(self._api_client)
        event_set_api_instance = swagger_client.EventSetApi(self._api_client)

        looked_up = event_api_instance.download_sampling_events_by_identifier('oxford_id', '123456')
        looked_up = looked_up.sampling_events[0]

        for study in ["9011 Upload test study", "9012 Upload test study 3"]:
            eset = "Additional events: {}".format(study)
            fetched_set = event_set_api_instance.download_event_set(eset)
            found = False
            for member in fetched_set.members.sampling_events:
                if member.sampling_event_id == looked_up.sampling_event_id:
                    found = True
            self.assertTrue(found, "Not added to additional events")
            event_set_api_instance.delete_event_set(eset)

        self.assertEqual(looked_up.study_name, '9010 Upload test study 2', 'Not lowest study code')

        for study in ["0000 Upload test study", "1089 R&D special study"]:
            eset = "Additional events: {}".format(study)
            with self.assertRaises(Exception) as context:
                event_set_api_instance.delete_event_set(eset)

            self.assertEqual(context.exception.status, 404)

        messages = [ 
            "Conflicting Study value\t\t{}\t9011 Upload test study\t9011 Upload test study\t9010 Upload test study 2\t[('sample_oxford_id', '123456'), ('study_id', '9010 Upload test study 2')]",
            "Conflicting Study value\t\t{}\t9010 Upload test study 2\t9010 Upload test study 2\t9012 Upload test study 3\t[('sample_oxford_id', '123456'), ('study_id', '9012 Upload test study 3')]",
            "Conflicting Study value\t\t{}\t9010 Upload test study 2\t9010 Upload test study 2\t1089 R&D special study\t[('sample_oxford_id', '123456'), ('study_id', '1089 R&D special study')]"
            ]
        for msg in messages:
            msg = msg.format(looked_up.sampling_event_id)
            self.assertIn(msg, self._messages)
