import swagger_client
from swagger_client.rest import ApiException
from test_base import TestBase
from datetime import date

import uuid

class TestTaxa(TestBase):


    """
    """
    def test_create_partner_species(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:

            samp = swagger_client.SamplingEvent(None, '3000-MD-UP', date(2017, 10, 10),
                                                doc_accuracy = 'month',
                                                partner_species = 'P. falciparum')
            created = api_instance.create_sampling_event(samp)
            fetched = api_instance.download_sampling_event(created.sampling_event_id)
            self.assertEqual(created, fetched, "create response != download response")
            fetched.sampling_event_id = None
            self.assertEqual(samp, fetched, "upload != download response")
            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.fail("test_create: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)


    """
    """
    def test_update_partner_species(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:

            samp = swagger_client.SamplingEvent(None, '3001-MD-UP', date(2017, 10, 10),
                                                partner_species = 'P. falciparum')
            created = api_instance.create_sampling_event(samp)
            new_samp = swagger_client.SamplingEvent(None, '3001-MD-UP', date(2017, 10, 10),
                                                partner_species = 'P. vivax')
            updated = api_instance.update_sampling_event(created.sampling_event_id, new_samp)
            fetched = api_instance.download_sampling_event(created.sampling_event_id)
            self.assertEqual(updated, fetched, "update response != download response")
            fetched.sampling_event_id = None
            self.assertEqual(new_samp, fetched, "update != download response")
            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.fail("test_update: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)

    """
    """
    def test_get_taxonomies(self):

        api_instance = swagger_client.MetadataApi(self._api_client)

        try:
            taxas = api_instance.get_taxonomy_metadata()

        except ApiException as error:
            self.fail("test_update: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)
