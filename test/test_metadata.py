import openapi_client
from openapi_client.rest import ApiException

from test_base import TestBase
from datetime import date

import urllib
import pytest


class TestMetadata(TestBase):


    """
    """
    def test_get_country_metadata(self, api_factory):

        api_instance = api_factory.MetadataApi()

        try:
            country = api_instance.get_country_metadata('CI')

            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to get_country_metadata succeeded')

            assert country.english =="Côte d'Ivoire"
            assert country.alpha2 =='CI'
            assert country.alpha3 =='CIV'

            country = api_instance.get_country_metadata('CIV')

            assert country.english =="Côte d'Ivoire"
            assert country.alpha2 =='CI'
            assert country.alpha3 =='CIV'

            country = api_instance.get_country_metadata(urllib.parse.quote_plus("Côte d'Ivoire"))

            assert country.english =="Côte d'Ivoire"
            assert country.alpha2 =='CI'
            assert country.alpha3 =='CIV'

        except ApiException as error:
            self.check_api_exception(api_factory, "MetadataApi->get_country_metadata", error)

    """
    """
    def test_missing_country_metadata(self, api_factory):

        api_instance = api_factory.MetadataApi()

        try:

            with pytest.raises(ApiException, status=404):
                country = api_instance.get_country_metadata('INDOCHINA')

        except ApiException as error:
            self.check_api_exception(api_factory, "MetadataApi->get_country_metadata", error)

