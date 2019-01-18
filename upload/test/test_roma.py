from test_base import TestBase

import datetime
import json

from upload_roma import Upload_ROMA

import swagger_client
from swagger_client.rest import ApiException

class TestROMA(TestBase):


    _locations = []

    """
    """
    @classmethod
    def setUpClass(self):

        super(TestROMA, self).setUpClass()
        el = Upload_ROMA(self._config_file)
        el.use_message_buffer = True
        el.load_data_file('roma_dump.20180116103346.json')

        self._messages = el.message_buffer

    """
    """
    @classmethod
    def tearDownClass(self):

        self.deleteStudies(['9030'], TestROMA._locations)

        self.tearDownLocations(TestROMA._locations)


    """
    """
    def test_strip(self):


        try:
            looked_up = self._dao.download_sampling_events_by_os_attr('roma_id', 'TST00003')
            looked_up = looked_up.sampling_events[0]
            self.assertEquals(looked_up.location.attrs[0].attr_value,
                              'Test name with spaces')
            if looked_up.location.location_id not in TestROMA._locations:
                TestROMA._locations.append(looked_up.location.location_id)
        except ApiException as error:
            self.fail("test_year_accuracy: Exception when calling download_sampling_event_by_attr {}"
                        .format(error))


    """
    """
    def test_partner_id(self):


        try:
            r_looked_up = self._dao.download_sampling_events_by_os_attr('roma_id', 'TST00002')
            r_looked_up = r_looked_up.sampling_events[0]
            p_looked_up = self._dao.download_sampling_events_by_os_attr('partner_id', 'EXTST000002')
            p_looked_up = p_looked_up.sampling_events[0]
            self.assertEquals(r_looked_up.sampling_event_id, p_looked_up.sampling_event_id)
        except ApiException as error:
            self.fail("test_year_accuracy: Exception when calling download_sampling_event_by_attr {}"
                        .format(error))



    """
    """
    def test_oxford_id(self):


        try:
            r_looked_up = self._dao.download_sampling_events_by_os_attr('roma_id', 'TST00002')
            r_looked_up = r_looked_up.sampling_events[0]
            ox_looked_up = self._dao.download_sampling_events_by_os_attr('oxford_id', 'OX0001-C')
            ox_looked_up = ox_looked_up.sampling_events[0]
            self.assertEquals(r_looked_up.sampling_event_id, ox_looked_up.sampling_event_id)

        except ApiException as error:
            self.fail("test_year_accuracy: Exception when calling download_sampling_event_by_attr {}"
                        .format(error))

    """
    """
    def test_species(self):


        try:
            looked_up = self._dao.download_original_samples_by_attr('roma_id', 'TST00002')
            looked_up = looked_up.original_samples[0]
            self.assertEquals(looked_up.partner_species, 'Plasmodium falciparum')
        except ApiException as error:
            self.fail("test_year_accuracy: Exception when calling download_sampling_event_by_os_attr {}"
                        .format(error))

    """
    """
    def test_date_of_collection(self):


        try:
            looked_up = self._dao.download_sampling_events_by_os_attr('roma_id', 'TST00002')
            looked_up = looked_up.sampling_events[0]
            self.assertEqual(looked_up.doc, datetime.date(2012, 11, 22))
        except ApiException as error:
            self.fail("test_year_accuracy: Exception when calling download_sampling_event_by_os_attr {}"
                        .format(error))


    """
    """
    def test_roma_location(self):


        try:
            looked_up = self._dao.download_sampling_events_by_os_attr('roma_id', 'TST00001')

            looked_up = looked_up.sampling_events[0]
            self.assertEqual(looked_up.location.latitude, 12.5)
            self.assertEqual(looked_up.location.longitude, 103.9)
            self.assertEqual(looked_up.location.country, 'KHM')
            self.assertEqual(looked_up.location.attrs[0].attr_value,
                             'Cambodia(Country)')
            self.assertEqual(looked_up.location.attrs[0].attr_source,
                             'roma_dump')
            self.assertEqual(looked_up.location.attrs[0].study_name,
                             '9030')
#            self.assertEqual(looked_up.location.notes, 'roma_dump.20180116103346.json')
            self.assertEqual(looked_up.location.notes, 'roma_dump')

            self.assertEqual(looked_up.proxy_location.latitude, 12.51)
            self.assertEqual(looked_up.proxy_location.longitude, 103.91)
            self.assertEqual(looked_up.proxy_location.country, 'KHM')
            self.assertEqual(looked_up.proxy_location.attrs[0].attr_value,
                             ' Test name with spaces ')
            self.assertEqual(looked_up.proxy_location.attrs[0].attr_source,
                             'roma_dump')
            self.assertEqual(looked_up.proxy_location.attrs[0].study_name,
                             '9030')
            if looked_up.location.location_id not in TestROMA._locations:
                TestROMA._locations.append(looked_up.location.location_id)
            if looked_up.proxy_location.location_id not in TestROMA._locations:
                TestROMA._locations.append(looked_up.proxy_location.location_id)
        except ApiException as error:
            self.fail("test_year_accuracy: Exception when calling download_sampling_event_by_os_attr {}"
                        .format(error))

