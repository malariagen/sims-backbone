from test_base import TestBase


import json

from uploader import Uploader

import swagger_client
from swagger_client.rest import ApiException

class TestSampling_Event(TestBase):



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

        event_api_instance = swagger_client.SamplingEventApi(self._api_client)

        looked_up = event_api_instance.download_sampling_event_by_identifier('oxford_id', '123456')

        event_api_instance.delete_sampling_event(looked_up.sampling_event_id)

    """
    """
    def test_multiple_study(self):


        event_api_instance = swagger_client.SamplingEventApi(self._api_client)
        event_set_api_instance = swagger_client.EventSetApi(self._api_client)

        looked_up = event_api_instance.download_sampling_event_by_identifier('oxford_id', '123456')

        for study in ["9011 Upload test study", "9012 Upload test study 3"]:
            eset = "Additional events: {}".format(study)
            fetched_set = event_set_api_instance.download_event_set(eset)
            found = False
            for member in fetched_set.members.sampling_events:
                if member.sampling_event_id == looked_up.sampling_event_id:
                    found = True
            self.assertTrue(found, "Not added to additional events")
            event_set_api_instance.delete_event_set(eset)

        self.assertEqual(looked_up.study_id, '9010 Upload test study 2', 'Not lowest study code')

        for study in ["0000 Upload test study", "1089 R&D special study"]:
            eset = "Additional events: {}".format(study)
            with self.assertRaises(Exception) as context:
                event_set_api_instance.delete_event_set(eset)

            self.assertEqual(context.exception.status, 404)

        self.assertIn("Conflicting study_id value 9010 " +
                      "Upload test study 2 9011 Upload test study\t" +
                      "[('sample_oxford_id', '123456'), " +
                      "('study_id', '9010 Upload test study 2')]", self._messages)

        self.assertIn("Conflicting study_id value 9012 " +
                      "Upload test study 3 9010 Upload test study 2\t" +
                      "[('sample_oxford_id', '123456'), " +
                      "('study_id', '9012 Upload test study 3')]", self._messages)

        self.assertIn("Conflicting study_id value 1089 " +
                      "R&D special study 9010 Upload test study 2\t" +
                      "[('sample_oxford_id', '123456'), " +
                      "('study_id', '1089 R&D special study')]",
                      self._messages)