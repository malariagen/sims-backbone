from test_base import TestBase

import datetime
import json

from uploader import Uploader

import swagger_client
from swagger_client.rest import ApiException

class TestDate(TestBase):


    """
    """
    @classmethod
    def setUpClass(self):

        super(TestDate, self).setUpClass()
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
                "doc": {
                    "column": 2,
                    "type": "datetime",
                    "date_format": "%Y-%m-%d"
                },
                "doc_accuracy": {
                    "column": 3,
                    "type": "string"
                }
            }
        }''')
        sd.load_data_file(json_data, 'dates.tsv')

        self._messages = sd.message_buffer

    """
    """
    @classmethod
    def tearDownClass(self):

        event_api_instance = swagger_client.SamplingEventApi(self._api_client)

        test_events = event_api_instance.download_sampling_events_by_study('9020')

        for event in test_events.sampling_events:
            event_api_instance.delete_sampling_event(event.sampling_event_id)


    """
    """
    def test_year_accuracy(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:
            looked_up = api_instance.download_sampling_event_by_identifier('oxford_id', '12345')
            looked_up = looked_up.sampling_events[0]
            self.assertEqual(looked_up.doc_accuracy, 'year')
            self.assertEqual(looked_up.doc, datetime.date(2017, 1, 1))
        except ApiException as error:
            self.fail("test_year_accuracy: Exception when calling download_sampling_event_by_identifier {}"
                        .format(error))


    """
    """
    def test_year_accuracy_implied(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:
            looked_up = api_instance.download_sampling_event_by_identifier('oxford_id', '12346')
            looked_up = looked_up.sampling_events[0]
            self.assertEqual(looked_up.doc_accuracy, 'year')
            self.assertEqual(looked_up.doc, datetime.date(2017, 1, 1))
        except ApiException as error:
            self.fail("test_year_accuracy: Exception when calling download_sampling_event_by_identifier {}"
                        .format(error))

    """
    """
    def test_parse_default(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:
            looked_up = api_instance.download_sampling_event_by_identifier('oxford_id', '12347')
            looked_up = looked_up.sampling_events[0]
            self.assertEqual(looked_up.doc_accuracy, 'day')
            self.assertEqual(looked_up.doc, datetime.date(2017, 2, 7))
        except ApiException as error:
            self.fail("test_year_accuracy: Exception when calling download_sampling_event_by_identifier {}"
                        .format(error))

    """
    """
    def test_parse_default_uk(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:
            looked_up = api_instance.download_sampling_event_by_identifier('oxford_id', '12348')
            looked_up = looked_up.sampling_events[0]
            self.assertEqual(looked_up.doc_accuracy, 'day')
            self.assertEqual(looked_up.doc, datetime.date(2017, 2, 7))
        except ApiException as error:
            self.fail("test_year_accuracy: Exception when calling download_sampling_event_by_identifier {}"
                        .format(error))

    """
    """
    def test_parse_default_mon(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:
            looked_up = api_instance.download_sampling_event_by_identifier('oxford_id', '12349')
            looked_up = looked_up.sampling_events[0]
            self.assertEqual(looked_up.doc_accuracy, 'day')
            self.assertEqual(looked_up.doc, datetime.date(2017, 2, 7))
        except ApiException as error:
            self.fail("test_year_accuracy: Exception when calling download_sampling_event_by_identifier {}"
                        .format(error))

    """
    """
    def test_month_accuracy(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:
            looked_up = api_instance.download_sampling_event_by_identifier('oxford_id', '12350')
            looked_up = looked_up.sampling_events[0]
            self.assertEqual(looked_up.doc_accuracy, 'month')
            self.assertEqual(looked_up.doc, datetime.date(2017, 2, 1))
        except ApiException as error:
            self.fail("test_year_accuracy: Exception when calling download_sampling_event_by_identifier {}"
                        .format(error))


    """
    The last date is used unless it is a year, and the subsequent date is not 
    - regardless it is the conflict is reported
    """
    def test_precedence(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:
            looked_up = api_instance.download_sampling_event_by_identifier('oxford_id', '12353')
            looked_up = looked_up.sampling_events[0]
            self.assertEqual(looked_up.doc, datetime.date(2017, 2, 7))

            self.assertIn("Conflicting doc value updated 2017-02-07 2017-03-12\t" +
                          "[('doc', datetime.date(2017, 2, 7)), ('doc_accuracy', None), " +
                          "('sample_oxford_id', '12353'), ('study_id', '9020 Upload test study 2')]", self._messages)
        except ApiException as error:
            self.fail("test_year_accuracy: Exception when calling download_sampling_event_by_identifier {}"
                        .format(error))



    """
    """
    def test_precedence_vs_year(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:
            looked_up = api_instance.download_sampling_event_by_identifier('oxford_id', '12352')
            looked_up = looked_up.sampling_events[0]
            self.assertEqual(looked_up.doc_accuracy, 'day')
            self.assertEqual(looked_up.doc, datetime.date(2017, 2, 7))
            self.assertIn("Conflicting doc value updated 2017-02-07 2017-01-01\t" +
                          "[('doc', datetime.date(2017, 2, 7)), ('doc_accuracy', None), " +
                          "('sample_oxford_id', '12352'), " +
                          "('study_id', '9020 Upload test study 2')]", self._messages)

            looked_up = api_instance.download_sampling_event_by_identifier('oxford_id', '12351')
            looked_up = looked_up.sampling_events[0]
            self.assertEqual(looked_up.doc_accuracy, 'day')
            self.assertEqual(looked_up.doc, datetime.date(2017, 2, 7))
            self.assertIn("Conflicting doc value not updated 2017-01-01 2017-02-07\t" +
                          "[('doc', datetime.date(2017, 1, 1)), ('doc_accuracy', 'year'), " +
                          "('sample_oxford_id', '12351'), " +
                          "('study_id', '9020 Upload test study 2')]", self._messages)

        except ApiException as error:
            self.fail("test_year_accuracy: Exception when calling download_sampling_event_by_identifier {}"
                        .format(error))




