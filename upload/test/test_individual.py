from test_base import TestBase

import datetime
import json

from uploader import Uploader

import swagger_client
from swagger_client.rest import ApiException

class TestIndividual(TestBase):


    _locations = []

    """
    """
    @classmethod
    def setUpClass(self):

        super(TestIndividual, self).setUpClass()
        sd = Uploader(self._config_file)
        sd.use_message_buffer = True
        json_data = json.loads('''{
    "values": {
        "unique_id": {
            "column": 2,
            "type": "string"
        },
        "unique_os_id": {
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
        "donor_source_code": {
            "column": 7,
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
        sd.load_data_file(json_data, 'individual.tsv')

        self._messages = sd.message_buffer

    """
    """
    @classmethod
    def tearDownClass(self):

        self.deleteEventSets(['individual'], TestIndividual._locations)


    """
    """
    def test_individual(self):


        try:
            looked_up = self._dao.download_sampling_events_by_os_attr('oxford_id',
                                                                      'TS0001-C')
            looked_up = looked_up.sampling_events[0]

            individual = self._dao.download_individual(looked_up.individual_id)

            assert individual.attrs
            assert individual.attrs[0].attr_value == '3D7'

            looked_up1 = self._dao.download_sampling_events_by_os_attr('oxford_id',
                                                                       'TS0001-CW7')
            looked_up1 = looked_up1.sampling_events[0]

            individual1 = self._dao.download_individual(looked_up1.individual_id)

            assert individual1.attrs
            assert individual1.attrs[0].attr_value == '3D7'

            assert looked_up.individual_id == looked_up1.individual_id

        except ApiException as error:
            self.fail("test_individual: Exception when calling download_sampling_event_by_attr {}"
                      .format(error))

    """
    """
    def test_no_individual(self):


        try:
            looked_up = self._dao.download_sampling_events_by_os_attr('oxford_id',
                                                                      'TS0001-CW5')
            looked_up = looked_up.sampling_events[0]

            assert looked_up.individual is None


        except ApiException as error:
            self.fail("test_no_individual: Exception when calling download_sampling_event_by_attr {}"
                      .format(error))
