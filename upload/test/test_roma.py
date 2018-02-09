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

        event_api_instance = swagger_client.SamplingEventApi(self._api_client)

        test_events = event_api_instance.download_sampling_events_by_study('9030')

        for event in test_events.sampling_events:
            event_api_instance.delete_sampling_event(event.sampling_event_id)

        location_api_instance = swagger_client.LocationApi(self._api_client)

        for loc in self._locations:
            location_api_instance.delete_location(loc)


    """
    """
    def test_strip(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:
            looked_up = api_instance.download_sampling_event_by_identifier('roma_id', 'TST00003')
            self.assertEquals(looked_up.location.identifiers[0].identifier_value,
                              'Test name with spaces')
            if looked_up.location.location_id not in self._locations:
                self._locations.append(looked_up.location.location_id)
        except ApiException as error:
            self.fail("test_year_accuracy: Exception when calling download_sampling_event_by_identifier {}"
                        .format(error))


    """
    """
    def test_partner_id(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:
            r_looked_up = api_instance.download_sampling_event_by_identifier('roma_id', 'TST00002')
            p_looked_up = api_instance.download_sampling_event_by_identifier('partner_id', 'EXTST000002')
            self.assertEquals(r_looked_up.sampling_event_id, p_looked_up.sampling_event_id)
        except ApiException as error:
            self.fail("test_year_accuracy: Exception when calling download_sampling_event_by_identifier {}"
                        .format(error))



    """
    """
    def test_oxford_id(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:
            r_looked_up = api_instance.download_sampling_event_by_identifier('roma_id', 'TST00002')
            ox_looked_up = api_instance.download_sampling_event_by_identifier('oxford_id', 'OX0001-C')
            self.assertEquals(r_looked_up.sampling_event_id, ox_looked_up.sampling_event_id)

        except ApiException as error:
            self.fail("test_year_accuracy: Exception when calling download_sampling_event_by_identifier {}"
                        .format(error))

    """
    """
    def test_species(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:
            looked_up = api_instance.download_sampling_event_by_identifier('roma_id', 'TST00002')
            self.assertEquals(looked_up.partner_species, 'Plasmodium falciparum')
        except ApiException as error:
            self.fail("test_year_accuracy: Exception when calling download_sampling_event_by_identifier {}"
                        .format(error))


    """
    """
    def test_location(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:
            looked_up = api_instance.download_sampling_event_by_identifier('roma_id', 'TST00001')
            self.assertEquals(looked_up.location.latitude, 12.5)
            self.assertEquals(looked_up.location.longitude, 103.9)
            self.assertEquals(looked_up.location.country, 'KHM')
            self.assertEquals(looked_up.location.identifiers[0].identifier_value,
                              'Cambodia(Country)')
            self.assertEquals(looked_up.location.identifiers[0].identifier_source,
                              'roma_dump')
            self.assertEquals(looked_up.location.identifiers[0].study_name,
                              '9030')
            self.assertEquals(looked_up.location.notes, 'roma_dump.20180116103346.json')
            if looked_up.location.location_id not in self._locations:
                self._locations.append(looked_up.location.location_id)
        except ApiException as error:
            self.fail("test_year_accuracy: Exception when calling download_sampling_event_by_identifier {}"
                        .format(error))
