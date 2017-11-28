import swagger_client
from swagger_client.rest import ApiException
from test_base import TestBase
from datetime import date

import uuid

class TestStudies(TestBase):


    """
    """
    def test_download_studies(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)
        study_api = swagger_client.StudyApi(self._api_client)

        try:

            samp = swagger_client.SamplingEvent(None, '2000-MD-UP', date(2017, 10, 10),
                                                doc_accuracy = 'month',
                                                partner_species = 'P. falciparum')
            created = api_instance.create_sampling_event(samp)

            studies = study_api.download_studies()

            found = False
            for study in studies.studies:
                if study.name == '2000-MD-UP' and study.code == '2000':
                    found = True

            self.assertTrue(found, 'Study does not exist')

            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.fail("test_create: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)


    """
    """
    def test_location_study(self):

        api_instance = swagger_client.LocationApi(self._api_client)
        study_api = swagger_client.StudyApi(self._api_client)

        try:

            loc = swagger_client.Location(None, 27.46362, 90.49542, 'country',
                                          'Trongsa, Trongsa, Bhutan', 'pv_3_locations.txt', 'BHU')
            loc.identifiers = [
                swagger_client.Identifier('partner_name', 'bhutan', '2001-MD-UP')
            ]
            created = api_instance.create_location(loc)
            studies = study_api.download_studies()

            found = False
            for study in studies.studies:
                if study.name == '2001-MD-UP' and study.code == '2001':
                    found = True

            self.assertTrue(found, 'Study does not exist')

            api_instance.delete_location(created.location_id)

        except ApiException as error:
            self.fail("test_location_study: Exception when calling LocationApi->create_location: %s\n" % error)

    """
    """
    def test_download_study(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)
        study_api = swagger_client.StudyApi(self._api_client)

        try:

            samp = swagger_client.SamplingEvent(None, '2002-MD-UP', date(2017, 10, 10),
                                                doc_accuracy = 'month',
                                                partner_species = 'P. falciparum')
            created = api_instance.create_sampling_event(samp)

            study1 = study_api.download_study('2002-MD-UP')
            study2 = study_api.download_study('2002')

            self.assertEqual(study1, study2, 'Study does not match')
            self.assertEqual(study1.partner_species[0].partner_species, 'P. falciparum', 'Species not set')
            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.fail("test_create: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)


    """
    """
    def test_download_study_fail(self):

        study_api = swagger_client.StudyApi(self._api_client)

        try:

            with self.assertRaises(Exception) as context:
                study1 = study_api.download_study('7777-MD-UP')
            self.assertEqual(context.exception.status, 404)

        except ApiException as error:
            self.fail("test_create: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)

    """
    """
    def test_update_study(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)
        study_api = swagger_client.StudyApi(self._api_client)

        try:

            samp = swagger_client.SamplingEvent(None, '0003-MD-UP', date(2017, 10, 10),
                                                doc_accuracy = 'month',
                                                partner_species = 'P. falciparum')
            created = api_instance.create_sampling_event(samp)

            study1 = study_api.download_study('0003-MD-UP')

            self.assertEqual(study1.partner_species[0].partner_species, 'P. falciparum', 'Species not set')
            #Taxa or study name are the only things you can update
            #partner_species belong to the sampling event
            study1.name = '0003-PF-MD-UP'
            taxa = swagger_client.Taxonomy(5833)

            study1.partner_species[0].taxa = [ taxa ]
            study2 = study_api.update_study('0003-MD-UP', study1)
            self.assertEqual(study2.name,'0003-PF-MD-UP')
            self.assertEqual(study2.partner_species[0].taxa[0].taxonomy_id, 5833, 'taxa not updated')

            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.fail("test_create: Exception when calling StudyApi->update_study: %s\n" % error)

    """
    """
    def test_update_study_bad_taxa(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)
        study_api = swagger_client.StudyApi(self._api_client)

        try:

            samp = swagger_client.SamplingEvent(None, '0004-MD-UP', date(2017, 10, 10),
                                                doc_accuracy = 'month',
                                                partner_species = 'P. falciparum')
            created = api_instance.create_sampling_event(samp)

            study1 = study_api.download_study('0004-MD-UP')

            self.assertEqual(study1.partner_species[0].partner_species, 'P. falciparum', 'Species not set')
            #Taxa or study name are the only things you can update
            #partner_species belong to the sampling event
            taxa = swagger_client.Taxonomy(999999)

            study1.partner_species[0].taxa = [ taxa ]
            with self.assertRaises(Exception) as context:
                study2 = study_api.update_study('0004-MD-UP', study1)
            self.assertEqual(context.exception.status, 422)
            #self.assertEqual(study2.partner_species[0].taxa[0].taxonomy_id, 999999, 'taxa not updated')

            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.fail("test_create: Exception when calling StudyApi->update_study: %s\n" % error)

    """
    """
    def test_download_samples_by_study(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)
        study_api = swagger_client.StudyApi(self._api_client)

        try:

            samp = swagger_client.SamplingEvent(None, '0005-MD-UP', date(2017, 10, 10),
                                                doc_accuracy = 'month',
                                                partner_species = 'P. falciparum')
            created = api_instance.create_sampling_event(samp)

            events = api_instance.download_sampling_events_by_study('0005-MD-UP')

            self.assertEqual(events.count, 1, "Event expected")

            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.fail("test_create: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)



    """
    """
    def test_download_samples_by_study_fail(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)
        study_api = swagger_client.StudyApi(self._api_client)

        try:

            with self.assertRaises(Exception) as context:
                events = api_instance.download_sampling_events_by_study('0006-MD-UP')
            self.assertEqual(context.exception.status, 404)


        except ApiException as error:
            self.fail("test_create: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)


