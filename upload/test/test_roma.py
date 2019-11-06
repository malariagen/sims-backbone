from test_base import TestBase

import datetime
import json

from upload_roma import Upload_ROMA

import openapi_client
from openapi_client.rest import ApiException

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

        TestBase.deleteStudies(['9030','9032','9033'], TestROMA._locations)

        TestBase.tearDownLocations(TestROMA._locations)

        TestBase.deleteEventSets(['roma_dump', 'roma_MNF00001'],
                                 TestROMA._locations)


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
            self.fail("test_species: Exception when calling download_sampling_event_by_os_attr {}"
                        .format(error))

    """
    """
    def test_date_of_collection(self):


        try:
            looked_up = self._dao.download_sampling_events_by_os_attr('roma_id', 'TST00002')
            looked_up = looked_up.sampling_events[0]
            self.assertEqual(looked_up.doc, datetime.date(2012, 11, 22))
        except ApiException as error:
            self.fail("test_year_of_collection: Exception when calling download_sampling_event_by_os_attr {}"
                        .format(error))

    """
    """
    def test_date_of_accession(self):


        try:
            looked_up = self._dao.download_sampling_events_by_os_attr('roma_id', 'TST00002')
            looked_up = looked_up.sampling_events[0]
            self.assertEqual(looked_up.acc_date, datetime.date(2015, 9, 7))
        except ApiException as error:
            self.fail("test_year_of_accession: Exception when calling download_sampling_event_by_os_attr {}"
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
                             'Test name with spaces')
            self.assertEqual(looked_up.proxy_location.attrs[0].attr_source,
                             'roma_dump')
            self.assertEqual(looked_up.proxy_location.attrs[0].study_name,
                             '9030')
            if looked_up.location.location_id not in TestROMA._locations:
                TestROMA._locations.append(looked_up.location.location_id)
            if looked_up.proxy_location.location_id not in TestROMA._locations:
                TestROMA._locations.append(looked_up.proxy_location.location_id)
        except ApiException as error:
            self.fail("test_roma_location: Exception when calling download_sampling_event_by_os_attr {}"
                        .format(error))

    """
    """
    def test_roma_individual(self):


        try:
            looked_up = self._dao.download_sampling_events_by_os_attr('roma_id', 'TST00001')

            looked_up = looked_up.sampling_events[0]

            assert looked_up.individual_id

            indiv = self._dao.download_individual(looked_up.individual_id)

            assert indiv.attrs[0].attr_type == 'patient_id'
            assert indiv.attrs[0].attr_value == '103335'
            assert indiv.attrs[0].attr_source == 'roma_dump'
            assert indiv.attrs[0].study_name == '9030'

        except ApiException as error:
            self.fail("test_roma_individual : Exception when download_sampling_events_by_os_attr{}"
                        .format(error))

    """
    """
    def test_roma_no_individual(self):


        try:
            looked_up = self._dao.download_sampling_events_by_os_attr('roma_id', 'TST00003')

            looked_up = looked_up.sampling_events[0]

            assert looked_up.individual_id is None

        except ApiException as error:
            self.fail("test_no_roma_individual : Exception when download_sampling_events_by_os_attr{}"
                        .format(error))


    """
    """
    def test_roma_event_set(self):

        try:
            looked_up = self._dao.download_sampling_events_by_os_attr('roma_id', 'TST00001')
            looked_up = looked_up.sampling_events[0]

            assert 'roma_dump' in looked_up.event_sets

            assert 'roma_MNF00001' in looked_up.event_sets

        except ApiException as error:
            self.fail("test_species: Exception when calling download_sampling_event_by_os_attr {}"
                        .format(error))

    """
    """
    def test_roma_well(self):


        try:
            looked_up = self._dao.download_derivative_samples_by_os_attr('roma_id', 'TST00001')

            ds_looked_up = looked_up.derivative_samples[0]

            assert looked_up.count == 1

            assert len(ds_looked_up.attrs) == 2

            if ds_looked_up.attrs[0].attr_type == 'plate_position':
                pl_attr = ds_looked_up.attrs[0]
                pn_attr = ds_looked_up.attrs[1]
            else:
                pl_attr = ds_looked_up.attrs[1]
                pn_attr = ds_looked_up.attrs[0]

            assert pn_attr.attr_type == 'plate_name'
            assert pn_attr.attr_value == 'PLATE_ROM_00001'
            assert pn_attr.attr_source == 'roma_dump'
            assert pn_attr.study_name  is None

            assert pl_attr.attr_type == 'plate_position'
            assert pl_attr.attr_value == 'A01'
            assert pl_attr.attr_source == 'roma_dump'
            assert pl_attr.study_name is None

            assert 'plate_position' in looked_up.attr_types
            assert 'plate_name' in looked_up.attr_types

        except ApiException as error:
            self.fail("test_roma_individual : Exception when download_derivative_samples_by_os_attr{}"
                        .format(error))

    """
    """
    def test_roma_os_history(self):

        username = 'person1@example.org'

        if TestBase.username:
            username = TestBase.username

        try:
            looked_up = self._dao.download_original_samples_by_attr('roma_id', 'TST00002')
            looked_up = looked_up.original_samples[0]
            history = self._dao.download_history('original_sample',
                                                 looked_up.original_sample_id)
            assert history.log_items[0].submitter == username
        except ApiException as error:
            self.fail("test_roma_os_history: Exception {}".format(error))

    """
    """
    def test_roma_ds_history(self):

        username = 'person1@example.org'

        if TestBase.username:
            username = TestBase.username

        try:
            looked_up = self._dao.download_derivative_samples_by_os_attr('roma_id', 'TST00001')

            ds_looked_up = looked_up.derivative_samples[0]

            history = self._dao.download_history('derivative_sample',
                                                 ds_looked_up.derivative_sample_id)
            assert history.log_items[0].submitter == username
        except ApiException as error:
            self.fail("test_roma_ds_history: Exception {}".format(error))

    """
    """
    def test_roma_se_history(self):

        username = 'person1@example.org'

        if TestBase.username:
            username = TestBase.username

        try:
            looked_up = self._dao.download_sampling_events_by_os_attr('roma_id', 'TST00001')

            looked_up = looked_up.sampling_events[0]

            history = self._dao.download_history('sampling_event',
                                                 looked_up.sampling_event_id)
            assert history.log_items[0].submitter == username
            assert looked_up.individual_id

            history = self._dao.download_history('individual',
                                                 looked_up.individual_id)
            assert history.log_items[0].submitter == username

            history = self._dao.download_history('location',
                                                 looked_up.location_id)
            assert history.log_items[0].submitter == username

        except ApiException as error:
            self.fail("test_roma_se_history : Exception {}".format(error))
