from test_base import TestBase

import datetime
import json

from upload_roma import Upload_ROMA

import openapi_client
from openapi_client.rest import ApiException

class TestROMADelete(TestBase):


    _locations = []

    """
    """
    @classmethod
    def setUpClass(self):

        super(TestROMADelete, self).setUpClass()
        el = Upload_ROMA(self._config_file)
        el.use_message_buffer = True
        el.load_data_file('roma_dump.20180116103346.json')

        el = Upload_ROMA(self._config_file)
        el.use_message_buffer = True
        el.load_data_file('roma_dump.201902.json')
        self._messages = el.message_buffer

    """
    """
    @classmethod
    def tearDownClass(self):

        looked_up = TestBase.getDAO().download_derivative_samples_by_os_attr('roma_id', 'TST00001')

        for derived_sample in looked_up.derivative_samples:
            TestBase.getDAO().delete_derivative_sample(derived_sample.derivative_sample_id)
        TestBase.removeManifestItems(['MNF00003'])

        TestBase.deleteEventSets(['roma_dump', 'MNF00003'],
                                 TestROMADelete._locations)
        TestBase.deleteStudies(['9030', '9032', '9033'], TestROMADelete._locations)

        TestBase.tearDownLocations(TestROMADelete._locations)


    """
    """
    def test_roma_delete_added(self):

        try:

            looked_up = self._dao.download_sampling_events_by_os_attr('roma_id', 'TST20001')
            looked_up = looked_up.sampling_events[0]

            assert 'roma_dump' in looked_up.event_sets

            assert 'MNF00003' in looked_up.event_sets

            if looked_up.location_id not in TestROMADelete._locations:
                TestROMADelete._locations.append(looked_up.location_id)

        except ApiException as error:
            self.fail("test_roma_delete_added: Exception when calling download_sampling_events_by_os_attr {}"
                      .format(error))

    """
    """
    def test_roma_delete_removed(self):

        try:

            looked_up = self._dao.download_sampling_events_by_os_attr('roma_id', 'TST00001')

            assert looked_up.count == 0
            assert not looked_up.sampling_events

        except ApiException as error:
            self.fail("test_roma_delete_removed: Exception when calling download_sampling_event_by_os_attr {}"
                      .format(error))

    """
    """
    def test_roma_delete_loc_removed(self):

        try:

            looked_up = self._dao.download_locations_by_attr('src_location_id',
                                                             'roma_loc_1')

            assert looked_up.count == 0
            assert not looked_up.locations

        except ApiException as error:
            self.fail("test_roma_delete_loc_removed: Exception when calling download_locations_by_attr {}".format(error))
