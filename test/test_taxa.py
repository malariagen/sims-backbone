import swagger_client
from swagger_client.rest import ApiException
from test_base import TestBase
from datetime import date

import uuid
import pytest


class TestTaxa(TestBase):

    _taxa_post_count = 0

    """
    """

    def test_create_partner_species(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp = swagger_client.OriginalSample(None, study_name='3000-MD-UP',
                                                 partner_species='P. falciparum')
            created = api_instance.create_original_sample(samp)
            fetched = api_instance.download_original_sample(
                created.original_sample_id)
            assert created == fetched, "create response != download response"
            fetched.original_sample_id = None
            assert samp == fetched, "upload != download response"
            api_instance.delete_original_sample(created.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory,
                                     "OriginalSampleApi->create_original_sample", error)

    """
    """

    def test_update_partner_species(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp = swagger_client.OriginalSample(None, study_name='3001-MD-UP',
                                                 partner_species='P. falciparum')
            created = api_instance.create_original_sample(samp)
            new_samp = swagger_client.OriginalSample(None, study_name='3001-MD-UP',
                                                     partner_species='P. vivax')
            updated = api_instance.update_original_sample(
                created.original_sample_id, new_samp)
            fetched = api_instance.download_original_sample(
                created.original_sample_id)
            assert updated == fetched, "update response != download response"
            fetched.original_sample_id = None
            assert new_samp == fetched, "update != download response"
            api_instance.delete_original_sample(created.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory,
                                     "OriginalSampleApi->create_original_sample", error)

    """
    """

    def test_get_taxonomies(self, api_factory):

        api_instance = api_factory.MetadataApi()

        try:
            if api_factory.is_authorized(None):
                taxas = api_instance.get_taxonomy_metadata()
            else:
                with pytest.raises(ApiException, status=403):
                    taxas = api_instance.get_taxonomy_metadata()

        except ApiException as error:
            self.check_api_exception(
                api_factory, "MetadataApi->get_taxonomy_metadata", error)

    """
    """

    def test_post_taxonomies(self, api_factory):

        api_instance = api_factory.MetadataApi()

        try:
            taxa = swagger_client.Taxonomy(taxonomy_id=7227, name='Drosophila melanogaster',
                                           rank='species')
            if api_factory.is_authorized(None):

                # No API to delete taxonomies so need to be a bit creative about testing creation
                if not api_factory.isLocal():
                    if TestTaxa._taxa_post_count == 0:
                        created_taxa = api_instance.create_taxonomy(taxa)
                    else:
                        with pytest.raises(ApiException, status=422):
                            created_taxa = api_instance.create_taxonomy(taxa)
                    TestTaxa._taxa_post_count = TestTaxa._taxa_post_count + 1
                else:
                    created_taxa = api_instance.create_taxonomy(taxa)

                taxas = api_instance.get_taxonomy_metadata()

                assert taxa in taxas.taxonomies

                if api_factory.isLocal():
                    conn = api_factory.base_controller.get_connection()
                    with conn:
                        with conn.cursor() as cursor:

                            stmt = "DELETE FROM taxonomies WHERE id=%s;"

                            cursor.execute(stmt, (taxa.taxonomy_id,))

            else:
                with pytest.raises(ApiException, status=403):
                    created_taxa = api_instance.create_taxonomy(taxa)

        except ApiException as error:
            self.check_api_exception(
                api_factory, "MetadataApi->create_taxonomy", error)
