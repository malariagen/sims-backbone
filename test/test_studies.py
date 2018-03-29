import swagger_client
from swagger_client.rest import ApiException
from test_base import TestBase
from datetime import date

import uuid
import pytest

class TestStudies(TestBase):


    """
    """
    def test_download_studies(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        study_api = api_factory.StudyApi()


        samp = swagger_client.SamplingEvent(None, '2000-MD-UP', date(2017, 10, 10),
                                            doc_accuracy = 'month',
                                            partner_species = 'P. falciparum')
        try:
            created = api_instance.create_sampling_event(samp)

            studies = study_api.download_studies()

            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to download_studies succeeded')

            found = False
            for study in studies.studies:
                if study.name == '2000-MD-UP' and study.code == '2000':
                    found = True

            assert found, 'Study does not exist'

            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)


    """
    """
    def test_location_study(self, api_factory):

        api_instance = api_factory.LocationApi()
        study_api = api_factory.StudyApi()


        loc = swagger_client.Location(None, 27.46362, 90.49542, 'country',
                                      'Trongsa, Trongsa, Bhutan', 'pv_3_locations.txt', 'BTN')
        loc.identifiers = [
            swagger_client.Identifier(identifier_type='partner_name',
                                      identifier_value='bhutan', study_name='2001-MD-UP')
        ]
        try:
            created = api_instance.create_location(loc)
            studies = study_api.download_studies()

            found = False
            for study in studies.studies:
                if study.name == '2001-MD-UP' and study.code == '2001':
                    found = True

            assert found, 'Study does not exist'

            api_instance.delete_location(created.location_id)
        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)


    """
    """
    def test_download_study(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        study_api = api_factory.StudyApi()

        samp = swagger_client.SamplingEvent(None, '2002-MD-UP', date(2017, 10, 10),
                                            doc_accuracy = 'month',
                                            partner_species = 'P. falciparum')

        try:
            created = api_instance.create_sampling_event(samp)

            study1 = study_api.download_study('2002-MD-UP')
            study2 = study_api.download_study('2002')

            assert study1 == study2, 'Study does not match'
            assert study1.partner_species[0].partner_species == 'P. falciparum', 'Species not set'
            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)


    """
    """
    def test_download_study_fail(self, api_factory):

        study_api = api_factory.StudyApi()

        try:

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    study1 = study_api.download_study('2003-MD-UP')
            else:
                with pytest.raises(ApiException, status=403):
                    study1 = study_api.download_study('2003-MD-UP')

        except ApiException as error:
            self.check_api_exception(api_factory, "StudyApi->download_study", error)

    """
    """
    def test_update_study(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        study_api = api_factory.StudyApi()

        try:

            samp = swagger_client.SamplingEvent(None, '2004-MD-UP', date(2017, 10, 10),
                                                doc_accuracy = 'month',
                                                partner_species = 'P. falciparum')
            created = api_instance.create_sampling_event(samp)

            study1 = study_api.download_study('2004-MD-UP')

            assert study1.partner_species[0].partner_species == 'P. falciparum', 'Species not set'
            #Taxa or study name are the only things you can update
            #partner_species belong to the sampling event
            study1.name = '2004-PF-MD-UP'
            taxa = swagger_client.Taxonomy(5833)

            study1.partner_species[0].taxa = [ taxa ]
            study2 = study_api.update_study('2004-MD-UP', study1)
            assert study2.name =='2004-PF-MD-UP'
            assert study2.partner_species[0].taxa[0].taxonomy_id == 5833, 'taxa not updated'

            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_update_missing_study(self, api_factory):

        study_api = api_factory.StudyApi()

        try:
            study = swagger_client.Study('404')

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    study2 = study_api.update_study('404', study)
            else:
                with pytest.raises(ApiException, status=403):
                    study2 = study_api.update_study('404', study)

        except ApiException as error:
            self.check_api_exception(api_factory, "StudyApi->update_study", error)

    """
    """
    def test_update_study_bad_taxa(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        study_api = api_factory.StudyApi()

        try:

            samp = swagger_client.SamplingEvent(None, '2005-MD-UP', date(2017, 10, 10),
                                                doc_accuracy = 'month',
                                                partner_species = 'P. falciparum')
            created = api_instance.create_sampling_event(samp)

            study1 = study_api.download_study('2005-MD-UP')

            assert study1.partner_species[0].partner_species == 'P. falciparum', 'Species not set'
            #Taxa or study name are the only things you can update
            #partner_species belong to the sampling event
            taxa = swagger_client.Taxonomy(999999)

            study1.partner_species[0].taxa = [ taxa ]
            with pytest.raises(ApiException, status=422):
                study2 = study_api.update_study('2004-MD-UP', study1)
            #assert study2.partner_species[0].taxa[0].taxonomy_id == 999999, 'taxa not updated'

            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_download_samples_by_study(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        study_api = api_factory.StudyApi()

        try:

            samp = swagger_client.SamplingEvent(None, '2006-MD-UP', date(2017, 10, 10),
                                                doc_accuracy = 'month',
                                                partner_species = 'P. falciparum')
            created = api_instance.create_sampling_event(samp)

            events = api_instance.download_sampling_events_by_study('2006-MD-UP')

            assert events.count == 1, "Event expected"

            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)



    """
    """
    def test_download_samples_by_study_fail(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    events = api_instance.download_sampling_events_by_study('2007-MD-UP')
            else:
                with pytest.raises(ApiException, status=403):
                    events = api_instance.download_sampling_events_by_study('2007-MD-UP')

        except ApiException as error:
            self.check_api_exception(api_factory,
                                     "SamplingEventApi->download_sampling_events_by_study", error)


