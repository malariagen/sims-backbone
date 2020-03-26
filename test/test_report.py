import openapi_client
from openapi_client.rest import ApiException

from test_base import TestBase
from datetime import date

import urllib
import pytest


class TestReport(TestBase):



    """
    """
    def create_report_data(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        se_api_instance = api_factory.SamplingEventApi()
        location_api_instance = api_factory.LocationApi()

        try:

            sampling_event = openapi_client.SamplingEvent(None, doc=date(2017, 10, 10),
                                                          doc_accuracy='month')
            loc = openapi_client.Location(None, latitude=27.463,
                                          longitude=90.495,
                                          accuracy='country',
                                          curated_name='Bhutan',
                                          notes='test_create_with_locations',
                                          country='BTN')
            loc.attrs = [
                openapi_client.Attr(attr_type='partner_name',
                                    attr_value='Bhutan location',
                                    attr_source='test',
                                    study_name='8100-MD-UP')
            ]
            loc = location_api_instance.create_location(loc)

            sampling_event.location_id = loc.location_id
            created_se = se_api_instance.create_sampling_event(sampling_event)

            samp = openapi_client.OriginalSample(None, study_name='8100-MD-UP',
                                                 partner_species='P. falciparum')
            samp.sampling_event_id = created_se.sampling_event_id

            samp.attrs = [
                openapi_client.Attr(attr_type='oxford', attr_value='12345678',
                                     attr_source='upd')
            ]
            created = api_instance.create_original_sample(samp)

            yield created

            se_api_instance.delete_sampling_event(created_se.sampling_event_id)

            location_api_instance.delete_location(loc.location_id)

            api_instance.delete_original_sample(created.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "create_report_data", error)

    """
    """
    def test_missing_detailed_location(self, api_factory):

        api_instance = api_factory.ReportApi()

        try:
            for data in self.create_report_data(api_factory):
                missing_locations = api_instance.missing_locations(include_country=True)

                assert missing_locations.studies[0].name == data.study_name

                if not api_factory.is_authorized(None):
                    pytest.fail('Unauthorized call to missing_locations succeeded')


        except ApiException as error:
            self.check_api_exception(api_factory,
                                     "test_missing_detailed_location", error)

    """
    """
    def test_missing_location(self, api_factory):

        api_instance = api_factory.ReportApi()
        se_api_instance = api_factory.SamplingEventApi()

        try:
            for data in self.create_report_data(api_factory):

                fetched = se_api_instance.download_sampling_event(data.sampling_event_id)
                fetched.location_id = None
                se_api_instance.update_sampling_event(data.sampling_event_id,
                                                      fetched)
                missing_locations = api_instance.missing_locations(include_country=True)

                assert missing_locations.studies[0].name == data.study_name

                if not api_factory.is_authorized(None):
                    pytest.fail('Unauthorized call to missing_locations succeeded')


        except ApiException as error:
            self.check_api_exception(api_factory,
                                     "test_missing_location", error)
    """
    """
    def test_uncurated_location_country(self, api_factory):

        api_instance = api_factory.ReportApi()
        se_api_instance = api_factory.SamplingEventApi()
        loc_api_instance = api_factory.LocationApi()

        try:
            for data in self.create_report_data(api_factory):
                fetched = se_api_instance.download_sampling_event(data.sampling_event_id)
                fetched = loc_api_instance.download_location(fetched.location_id)
                fetched.country = None
                upd = loc_api_instance.update_location(fetched.location_id,
                                                 fetched)
                missing_locations = api_instance.uncurated_locations()

                assert missing_locations.studies[0].name == data.study_name

                if not api_factory.is_authorized(None):
                    pytest.fail('Unauthorized call to missing_locations succeeded')


        except ApiException as error:
            self.check_api_exception(api_factory,
                                     "test_uncurated_location", error)

    """
    """
    def test_uncurated_location_curated_name(self, api_factory):

        api_instance = api_factory.ReportApi()
        se_api_instance = api_factory.SamplingEventApi()
        loc_api_instance = api_factory.LocationApi()

        try:
            for data in self.create_report_data(api_factory):
                fetched = se_api_instance.download_sampling_event(data.sampling_event_id)
                fetched = loc_api_instance.download_location(fetched.location_id)
                fetched.curated_name = None
                loc_api_instance.update_location(fetched.location_id,
                                                 fetched)
                missing_locations = api_instance.uncurated_locations()

                assert missing_locations.studies[0].name == data.study_name

                if not api_factory.is_authorized(None):
                    pytest.fail('Unauthorized call to missing_locations succeeded')


        except ApiException as error:
            self.check_api_exception(api_factory,
                                     "test_uncurated_location", error)

    """
    """
    def test_multiple_location_gps(self, api_factory):

        api_instance = api_factory.ReportApi()
        se_api_instance = api_factory.SamplingEventApi()
        loc_api_instance = api_factory.LocationApi()

        try:
            for data in self.create_report_data(api_factory):
                fetched = se_api_instance.download_sampling_event(data.sampling_event_id)
                fetched = loc_api_instance.download_location(fetched.location_id)
                fetched.attrs[0].attr_value = 'second name'
                fetched.location_id = None
                new = loc_api_instance.create_location(fetched)
                multiple_locations = api_instance.multiple_location_gps()
                assert multiple_locations.studies[0].name == data.study_name

                if not api_factory.is_authorized(None):
                    pytest.fail('Unauthorized call to multiple_location_names succeeded')

                loc_api_instance.delete_location(new.location_id)

        except ApiException as error:
            self.check_api_exception(api_factory,
                                     "test_multiple_location_gps", error)

    """
    """
    def test_multiple_location_names(self, api_factory):

        api_instance = api_factory.ReportApi()
        se_api_instance = api_factory.SamplingEventApi()
        loc_api_instance = api_factory.LocationApi()

        try:
            for data in self.create_report_data(api_factory):
                fetched = se_api_instance.download_sampling_event(data.sampling_event_id)
                fetched = loc_api_instance.download_location(fetched.location_id)
                fetched.latitude = 27.4631
                fetched.longitude = 90.4951
                fetched.location_id = None
                new = loc_api_instance.create_location(fetched)
                multiple_locations = api_instance.multiple_location_names()
                assert multiple_locations.studies[0].name == data.study_name

                if not api_factory.is_authorized(None):
                    pytest.fail('Unauthorized call to multiple_location_names succeeded')

                loc_api_instance.delete_location(new.location_id)

        except ApiException as error:
            self.check_api_exception(api_factory,
                                     "test_multiple_location_names", error)

    """
    """
    def test_missing_taxon(self, api_factory):

        api_instance = api_factory.ReportApi()

        try:
            for data in self.create_report_data(api_factory):
                missing_taxa = api_instance.missing_taxon()

                studies = [d.name for d in missing_taxa.studies]

                assert data.study_name in studies

                if not api_factory.is_authorized(None):
                    pytest.fail('Unauthorized call to missing_taxon succeeded')


        except ApiException as error:
            self.check_api_exception(api_factory,
                                     "test_missing_taxon", error)
