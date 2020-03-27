from test_base import TestBase

import datetime
import json
import os

from upload_roma import Upload_ROMA
from set_taxa import SetTaxa

import openapi_client
from openapi_client.rest import ApiException

class TestSetTaxa(TestBase):


    _locations = []

    """
    """
    @classmethod
    def setUpClass(self):

        super(TestSetTaxa, self).setUpClass()
        el = Upload_ROMA(self._config_file)
        el.use_message_buffer = True
        el.load_data_file('roma_dump.20180116103346.json')

        self._sd = SetTaxa(self._config_file)
        pwd = os.getcwd()
        os.chdir('..')
        self._sd.load_taxa_map()
        os.chdir(pwd)

    """
    """
    @classmethod
    def tearDownClass(self):

        looked_up = TestBase.getDAO().download_derivative_samples_by_os_attr('roma_id', 'TST00001')

        for derived_sample in looked_up.derivative_samples:
            TestBase.getDAO().delete_derivative_sample(derived_sample.derivative_sample_id)

        TestBase.removeManifestItems(['roma_MNF00001', 'roma_MNF00002', 'roma_MNF00003'])
        TestBase.deleteEventSets(['roma_dump', 'roma_MNF00001', 'roma_MNF00002', 'roma_MNF00003'],
                                 TestSetTaxa._locations)
        TestBase.tearDownLocations(TestSetTaxa._locations)

        TestBase.deleteStudies(['9030', '9032', '9033'], TestSetTaxa._locations)


    """
    """
    def test_taxa_set(self):

        try:

            looked_up = self._dao.download_original_samples_by_attr('roma_id', 'TST00002')
            looked_up = looked_up.original_samples[0]

            assert looked_up.partner_species == 'Plasmodium falciparum'
            assert not looked_up.partner_taxonomies

        except ApiException as error:
            self.fail("test_species: Exception when calling download_original_samples_by_attr {}"
                      .format(error))
        try:
            study = self._dao.download_study('9030')

        except ApiException as error:
            self.fail("test_species: Exception when calling download_study {}"
                      .format(error))
        try:
            assert len(study.partner_species) == 1
            assert study.partner_species[0].partner_species == 'Plasmodium falciparum'
            assert not study.partner_species[0].taxa

            looked_up = self._dao.download_original_samples_by_attr('roma_id', 'TST00004')
            looked_up = looked_up.original_samples[0]

            assert looked_up.partner_species == 'Plasmodium falciparum/vivax mixture'
            assert not looked_up.partner_taxonomies

            looked_up = self._dao.download_original_samples_by_attr('roma_id', 'TST00005')
            looked_up = looked_up.original_samples[0]

            assert looked_up.partner_species == 'Plasmodium non existent'
            assert not looked_up.partner_taxonomies

            self._sd.set_taxa()

            looked_up = self._dao.download_original_samples_by_attr('roma_id', 'TST00002')
            looked_up = looked_up.original_samples[0]

            assert looked_up.partner_species == 'Plasmodium falciparum'
            assert len(looked_up.partner_taxonomies) == 1
            assert looked_up.partner_taxonomies[0].taxonomy_id == 5833

            study = self._dao.download_study('9030')

            assert len(study.partner_species) == 1
            assert study.partner_species[0].partner_species == 'Plasmodium falciparum'
            assert len(study.partner_species[0].taxa) == 1
            assert study.partner_species[0].taxa[0].taxonomy_id == 5833

            looked_up = self._dao.download_original_samples_by_attr('roma_id', 'TST00004')
            looked_up = looked_up.original_samples[0]

            assert looked_up.partner_species == 'Plasmodium falciparum/vivax mixture'
            assert len(looked_up.partner_taxonomies) == 2
            assert (looked_up.partner_taxonomies[0].taxonomy_id == 5833 and looked_up.partner_taxonomies[1].taxonomy_id == 5855) or (looked_up.partner_taxonomies[1].taxonomy_id == 5833 and looked_up.partner_taxonomies[0].taxonomy_id == 5855)

            looked_up = self._dao.download_original_samples_by_attr('roma_id', 'TST00005')
            looked_up = looked_up.original_samples[0]

            assert looked_up.partner_species == 'Plasmodium non existent'
            assert not looked_up.partner_taxonomies

        except ApiException as error:
            self.fail("test_species: Exception when calling download_original_samples_by_attr {}"
                      .format(error))
