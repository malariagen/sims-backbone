from test_base import TestBase

import datetime
import json

from upload_roma import Upload_ROMA

import openapi_client
from openapi_client.rest import ApiException

class TestROMAReplace(TestBase):


    _locations = []

    """
    """
    @classmethod
    def setUpClass(self):

        super(TestROMAReplace, self).setUpClass()
        el = Upload_ROMA(self._config_file)
        el.use_message_buffer = True
        el.load_data_file('roma_dump.20180116103346.json')

        el = Upload_ROMA(self._config_file)
        el.use_message_buffer = True
        el.load_data_file('roma_dump.2019.json')
        self._messages = el.message_buffer

    """
    """
    @classmethod
    def tearDownClass(self):

        TestBase.deleteStudies(['9030','9032','9033'], TestROMAReplace._locations)

        TestBase.tearDownLocations(TestROMAReplace._locations)

        TestBase.deleteEventSets(['roma_dump', 'roma_MNF00002'],
                                 TestROMAReplace._locations)



    """
    """
    def test_roma_replaced(self):

        try:

            looked_up = self._dao.download_sampling_events_by_os_attr('roma_id', 'TST00001')
            looked_up = looked_up.sampling_events[0]

            assert 'roma_dump' in looked_up.event_sets

            assert 'roma_MNF00001' not in looked_up.event_sets
            assert 'roma_MNF00002' in looked_up.event_sets

        except ApiException as error:
            self.fail("test_species: Exception when calling download_sampling_event_by_os_attr {}"
                        .format(error))


