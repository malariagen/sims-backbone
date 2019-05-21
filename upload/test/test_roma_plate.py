from test_base import TestBase

import datetime
import json

from upload_roma import Upload_ROMA

import openapi_client
from openapi_client.rest import ApiException

class TestROMAPlate(TestBase):


    _locations = []

    """
    """
    @classmethod
    def setUpClass(self):

        super(TestROMAPlate, self).setUpClass()

        el = Upload_ROMA(self._config_file)
        el.use_message_buffer = True
        el.load_data_file('roma_dump.201903.json')
        self._messages = el.message_buffer

    """
    """
    @classmethod
    def tearDownClass(self):

        TestBase.deleteStudies(['3030'], TestROMAPlate._locations)

        TestBase.tearDownLocations(TestROMAPlate._locations)

        TestBase.deleteEventSets(['roma_MNF00004'],
                                 TestROMAPlate._locations)



    """
    """
    def test_roma_plate(self):

        try:

            looked_up = self._dao.download_derivative_samples_by_os_attr('roma_id', 'TST30001')
            looked_up = looked_up.derivative_samples[0]

            name = False
            pos = False
            for attr in looked_up.attrs:
                if attr.attr_type == 'plate_position':
                    assert attr.attr_value == 'A01'
                    pos = True
                if attr.attr_type == 'plate_name':
                    assert attr.attr_value == 'PLATE_PLT_00001'
                    name = True

            assert pos, 'Plate position not set'
            assert name, 'Plate name not set'

        except ApiException as error:
            self.fail("test_species: Exception when calling download_sampling_event_by_os_attr {}"
                        .format(error))


    """
    """
    def test_roma_plate_2_plates_2_wells(self):

        try:

            samples = self._dao.download_derivative_samples_by_os_attr('roma_id', 'TST30003')

            for looked_up in samples.derivative_samples:
                plate_pos = None
                plate_name = None
                for attr in looked_up.attrs:
                    if attr.attr_type == 'plate_position':
                        plate_pos = attr.attr_value
                    if attr.attr_type == 'plate_name':
                        plate_name = attr.attr_value

                if plate_name == 'PLATE_PLT_00001':
                    assert plate_pos == 'A04'
                elif plate_name == 'PLATE_PLT_00002':
                    assert plate_pos == 'A01'
                else:
                    self.fail(f'Unknown plate {looked_up}')


        except ApiException as error:
            self.fail("test_species: Exception when calling download_sampling_event_by_os_attr {}"
                        .format(error))


    """
    """
    def test_roma_plate_2_wells(self):

        try:

            samples = self._dao.download_derivative_samples_by_os_attr('roma_id', 'TST30002')

            wells = []
            for looked_up in samples.derivative_samples:
                plate_pos = None
                plate_name = None
                for attr in looked_up.attrs:
                    if attr.attr_type == 'plate_position':
                        wells.append(attr.attr_value)
                    if attr.attr_type == 'plate_name':
                        plate_name = attr.attr_value
                        assert plate_name == 'PLATE_PLT_00001'

            assert 'A02' in wells
            assert 'A03' in wells
            assert len(wells) == 2


        except ApiException as error:
            self.fail("test_species: Exception when calling download_sampling_event_by_os_attr {}"
                        .format(error))


