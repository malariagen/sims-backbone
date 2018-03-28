import swagger_client
from swagger_client.rest import ApiException
from api_factory import ApiFactory
from test_base import TestBase
from datetime import date

import urllib

class TestMetadata(TestBase):


    """
    """
    def test_get_country_metadata(self):

        api_instance = ApiFactory.MetadataApi(self._api_client)

        try:
            country = api_instance.get_country_metadata('CI')

            self.assertEqual(country.english,"Côte d'Ivoire")
            self.assertEqual(country.alpha2,'CI')
            self.assertEqual(country.alpha3,'CIV')

            country = api_instance.get_country_metadata('CIV')
            
            self.assertEqual(country.english,"Côte d'Ivoire")
            self.assertEqual(country.alpha2,'CI')
            self.assertEqual(country.alpha3,'CIV')

            country = api_instance.get_country_metadata(urllib.parse.quote_plus("Côte d'Ivoire"))

            self.assertEqual(country.english,"Côte d'Ivoire")
            self.assertEqual(country.alpha2,'CI')
            self.assertEqual(country.alpha3,'CIV')

        except ApiException as error:
            self.fail("test_get_country_metadata: Exception when calling MetadataApi->get_country_metadata: %s\n" % error)

    """
    """
    def test_missing_country_metadata(self):

        api_instance = ApiFactory.MetadataApi(self._api_client)

        try:

            with self.assertRaises(Exception) as context:
                country = api_instance.get_country_metadata('INDOCHINA')
            self.assertEqual(context.exception.status, 404)


        except ApiException as error:
            self.fail("test_get_country_metadata: Exception when calling MetadataApi->get_country_metadata: %s\n" % error)

