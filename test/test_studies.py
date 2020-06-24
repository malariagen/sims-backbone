import openapi_client
from openapi_client.rest import ApiException
from test_base import TestBase
from datetime import date

import uuid
import pytest


class TestStudies(TestBase):

    """
    """
    def test_download_studies(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        study_api = api_factory.StudyApi()

        samp = openapi_client.OriginalSample(None,
                                             study_name='2000-MD-UP')
        try:
            created = api_instance.create_original_sample(samp)

            studies = study_api.download_studies()

            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to download_studies succeeded')

            found = False
            for study in studies.studies:
                if study.name == '2000-MD-UP' and study.code == '2000':
                    found = True

            if api_factory.is_filtered('2000'):
                assert found, 'Study does not exist'

            api_instance.delete_original_sample(created.original_sample_id)

        except ApiException as error:
            self.check_api_exception(
                api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_download_studies_filtered(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        study_api = api_factory.StudyApi()

        samp = openapi_client.OriginalSample(None,
                                             study_name='2008-MD-UP')
        try:
            created = api_instance.create_original_sample(samp)

            studies = study_api.download_studies()

            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to download_studies succeeded')

            for study in studies.studies:
                if not api_factory.is_filtered('2008'):
                    assert not study.code == '2008', 'No permission for study'


            api_instance.delete_original_sample(created.original_sample_id)

        except ApiException as error:
            self.check_api_exception(
                api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_download_studies_permission(self, api_factory):

        study_api = api_factory.StudyApi()

        try:

            if not api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=403):
                    studies = study_api.download_studies()

        except ApiException as error:
            self.check_api_exception(
                api_factory, "StudyApi->download_studies", error)

    """
    """
    def test_location_study(self, api_factory):

        api_instance = api_factory.LocationApi()
        study_api = api_factory.StudyApi()

        loc = openapi_client.Location(None, latitude=27.46362,
                                      longitude=90.49542,
                                      accuracy='country',
                                      curated_name='Trongsa, Trongsa, Bhutan',
                                      notes='pv_3_locations.txt',
                                      country='BTN')
        loc.attrs = [
            openapi_client.Attr(attr_type='partner_name',
                                attr_value='bhutan', study_name='2001-MD-UP')
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
            self.check_api_exception(
                api_factory, "LocationApi->create_location", error)

    """
    """

    def test_download_study(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        study_api = api_factory.StudyApi()

        samp = openapi_client.OriginalSample(None, study_name='2002-MD-UP',
                                             partner_species='P. falciparum')

        try:
            created = api_instance.create_original_sample(samp)

            if not api_factory.is_authorized('2002'):
                with pytest.raises(ApiException, status=403):
                    study1 = study_api.download_study('2002-MD-UP')
                    study2 = study_api.download_study('2002')

            else:
                study1 = study_api.download_study('2002-MD-UP')
                study2 = study_api.download_study('2002')
                assert study1 == study2, 'Study does not match'
                assert study1.partner_species[0].partner_species == 'P. falciparum', 'Species not set'

            api_instance.delete_original_sample(created.original_sample_id)

        except ApiException as error:
            self.check_api_exception(
                api_factory, "LocationApi->create_location", error)

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
            self.check_api_exception(
                api_factory, "StudyApi->download_study", error)

    """
    """

    def test_update_study(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        study_api = api_factory.StudyApi()

        try:

            study1 = openapi_client.Study(name='2004-MD-UP',
                                          code='2004')

            if not api_factory.is_authorized('2004'):
                with pytest.raises(ApiException, status=403):
                    study_api.update_study('2004-MD-UP', study1)
            else:
                samp = openapi_client.OriginalSample(None, study_name='2004-MD-UP',
                                                     partner_species='P. falciparum')
                created = api_instance.create_original_sample(samp)

                study1 = study_api.download_study('2004-MD-UP')

                assert study1.partner_species[0].partner_species == 'P. falciparum', 'Species not set'
                # Taxa or study name are the only things you can update
                # partner_species belong to the sampling event
                study1.name = '2004-PF-MD-UP'
                taxa = openapi_client.Taxonomy(5833)

                study1.partner_species[0].taxa = [taxa]
                study1.ethics_expiry = date(2019, 11, 4)
                study1.sequencescape_code = ['1234', '1235']

                shipment = openapi_client.Batch(None, date_of_arrival=date(2019, 1, 4),
                                                          sample_count=42,
                                                          expected_species='P.  vivax',
                                                          expected_taxonomies=[])
                study1.batches = [shipment]

                study1.countries = [openapi_client.Country(alpha3='AFG')]
                study1.title = 'Title of study'
                study1.status = 'enquiry'
                study1.study_ethics = 'ethics hsaighignsfg'
                study1.rag_status = 'amber'
                study1.legacy_id = 'PV3'
                study1.description = 'vnasvnafnvf'
                study1.description_approved = True
                study1.web_title = 'vnasvnafnvf'
                study1.web_title_approved = True
                study1.sample_types = 'DBS'
                study1.notes = 'Some notes'
                # Shouldn't really reference ourself but we know that it
                # exists
                study1.web_study = study1.name
                study1.num_collections = None
                study1.num_original_samples = None
                study1.num_derivative_samples = None
                study1.num_original_derivative_samples = None
                study1.num_assay_data = None
                study1.num_original_assay_data = None
                study1.num_released = None

                study2 = study_api.update_study('2004-MD-UP', study1)

                assert study2.version > study1.version
                assert study2.name == '2004-PF-MD-UP'
                assert study2.partner_species[0].taxa[0].taxonomy_id == 5833, 'taxa not updated'

                assert study1.ethics_expiry == study2.ethics_expiry

                study3 = study_api.download_study('2004-MD-UP')
                # print(study3)

                study2.batches[0].batch_id = None
                study2.batches[0].version = None
                assert study1.batches[0] == study2.batches[0]

                assert study1.sequencescape_code == study2.sequencescape_code

                assert len(study2.partner_species) == 2

                api_instance.delete_original_sample(created.original_sample_id)
                # Need to reset for test to work next time as it's not possible
                # to delete studies
                study2.batches = []
                study2.partner_species[0].taxa = []
                study2.ethics_expiry = None
                study2.num_collections = None
                study2.num_original_samples = None
                study2.num_derivative_samples = None
                study2.num_original_derivative_samples = None
                study2.num_assay_data = None
                study2.num_original_assay_data = None
                study2.num_released = None
                study_api.update_study('2004-MD-UP', study2)

        except ApiException as error:
            self.check_api_exception(
                api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """

    def test_update_missing_study(self, api_factory):

        study_api = api_factory.StudyApi()

        try:
            study = openapi_client.Study('404')

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    study2 = study_api.update_study('404', study)
            else:
                with pytest.raises(ApiException, status=403):
                    study2 = study_api.update_study('404', study)

        except ApiException as error:
            self.check_api_exception(
                api_factory, "StudyApi->update_study", error)

    """
    """

    def test_update_study_bad_taxa(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        study_api = api_factory.StudyApi()

        try:

            samp = openapi_client.OriginalSample(None, study_name='2005-MD-UP',
                                                partner_species='P. falciparum')
            created = api_instance.create_original_sample(samp)

            study1 = study_api.download_study('2005-MD-UP')

            assert study1.partner_species[0].partner_species == 'P. falciparum', 'Species not set'
            # Taxa or study name are the only things you can update
            # partner_species belong to the sampling event
            taxa = openapi_client.Taxonomy(999999)

            study1.partner_species[0].taxa = [taxa]
            with pytest.raises(ApiException, status=422):
                study1.num_collections = None
                study1.num_original_samples = None
                study1.num_derivative_samples = None
                study1.num_original_derivative_samples = None
                study1.num_assay_data = None
                study1.num_original_assay_data = None
                study1.num_released = None

                study2 = study_api.update_study('2005-MD-UP', study1)
            #assert study2.partner_species[0].taxa[0].taxonomy_id == 999999, 'taxa not updated'

            api_instance.delete_original_sample(created.original_sample_id)

        except ApiException as error:
            self.check_api_exception(
                api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """

    def test_download_samples_by_study(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        os_api_instance = api_factory.OriginalSampleApi()
        study_api = api_factory.StudyApi()

        try:

            samp = openapi_client.SamplingEvent(None,
                                                doc_accuracy='month')
            created = api_instance.create_sampling_event(samp)
            osamp = openapi_client.OriginalSample(None,
                                                  study_name='2006-MD-UP')
            osamp.sampling_event_id = created.sampling_event_id
            os_created = os_api_instance.create_original_sample(osamp)

            events = api_instance.download_sampling_events_by_study(
                '2006-MD-UP')

            assert events.count == 1, "Event expected"

            os_api_instance.delete_original_sample(os_created.original_sample_id)
            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(
                api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """

    def test_download_samples_by_study_fail(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    events = api_instance.download_sampling_events_by_study(
                        '2007-MD-UP')
            else:
                with pytest.raises(ApiException, status=403):
                    events = api_instance.download_sampling_events_by_study(
                        '2007-MD-UP')

        except ApiException as error:
            self.check_api_exception(api_factory,
                                     "SamplingEventApi->download_sampling_events_by_study", error)

    """
    """
    def test_location_study_lookup(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        os_api_instance = api_factory.OriginalSampleApi()
        loc_api_instance = api_factory.LocationApi()
        study_api = api_factory.StudyApi()

        try:
            study_code = '2008-MD-UP'
            loc = openapi_client.Location(None, latitude=27.46362,
                                          longitude=90.49542, accuracy='country',
                                          curated_name='Trongsa, Trongsa, Bhutan',
                                          notes='pv_3_locations.txt', country='BTN')
            loc.attrs = [
                openapi_client.Attr(attr_type='partner_name',
                                    attr_value='bhutan', study_name=study_code)
            ]
            loc_created = loc_api_instance.create_location(loc)

            from datetime import date
            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 14))
            samp.location_id = loc_created.location_id
            created_se = api_instance.create_sampling_event(samp)
            samp = openapi_client.OriginalSample(None, study_name=study_code,
                                                 partner_species='PF')
            samp.sampling_event_id = created_se.sampling_event_id
            created_os = os_api_instance.create_original_sample(samp)

            fetched = study_api.download_study(study_code)

            assert fetched.locations, "Study locations not found"

            assert loc_created == fetched.locations.locations[0], "create response != download response"

            os_api_instance.delete_original_sample(created_os.original_sample_id)

            api_instance.delete_sampling_event(created_se.sampling_event_id)
            loc_api_instance.delete_location(loc_created.location_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)
