import openapi_client
from openapi_client.rest import ApiException
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

            samp = openapi_client.OriginalSample(None, study_name='3000-MD-UP',
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

            samp = openapi_client.OriginalSample(None, study_name='3001-MD-UP',
                                                 partner_species='P. falciparum')
            created = api_instance.create_original_sample(samp)
            new_samp = openapi_client.OriginalSample(None, study_name='3001-MD-UP',
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
            taxa = openapi_client.Taxonomy(taxonomy_id=7227, name='Drosophila melanogaster',
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

    """
    """
    def test_multiple_partner_species(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        study_api_instance = api_factory.StudyApi()

        study_ident = '3000-MD-UP'
        try:

            samp1 = openapi_client.OriginalSample(None, study_name=study_ident,
                                                  partner_species='P. falciparum')
            created1 = api_instance.create_original_sample(samp1)
            fetched1 = api_instance.download_original_sample(created1.original_sample_id)
            assert created1 == fetched1, "create response != download response"
            fetched1.original_sample_id = None
            assert samp1 == fetched1, "upload != download response"

            samp2 = openapi_client.OriginalSample(None, study_name=study_ident,
                                                  partner_species='P. falciparum')
            created2 = api_instance.create_original_sample(samp2)
            fetched2 = api_instance.download_original_sample(created2.original_sample_id)
            assert created2 == fetched2, "create response != download response"
            fetched2.original_sample_id = None
            assert samp2 == fetched2, "upload != download response"

            samp3 = openapi_client.OriginalSample(None, study_name=study_ident,
                                                  partner_species='P. falciparum + P. vivax')
            created3 = api_instance.create_original_sample(samp3)
            fetched3 = api_instance.download_original_sample(created3.original_sample_id)
            assert created3 == fetched3, "create response != download response"
            fetched3.original_sample_id = None
            assert samp3 == fetched3, "upload != download response"

            samp4 = openapi_client.OriginalSample(None, study_name=study_ident,
                                                  partner_species='P. falciparum + P. vivax')
            created4 = api_instance.create_original_sample(samp4)
            fetched4 = api_instance.download_original_sample(created4.original_sample_id)
            assert created4 == fetched4, "create response != download response"
            fetched4.original_sample_id = None
            assert samp4 == fetched4, "upload != download response"

            study_detail = study_api_instance.download_study(study_ident)

            for species in study_detail.partner_species:
                if species.partner_species == 'P. falciparum':
                    species.taxa = [openapi_client.Taxonomy(taxonomy_id=5833)]
                else:
                    species.taxa = [openapi_client.Taxonomy(taxonomy_id=5833),
                                    openapi_client.Taxonomy(taxonomy_id=5855)]

            study_api_instance.update_study(study_ident, study_detail)

            fetched1 = api_instance.download_original_sample(created1.original_sample_id)

            assert len(fetched1.partner_taxonomies) == 1
            assert (int)(fetched1.partner_taxonomies[0].taxonomy_id) == 5833

            fetched3 = api_instance.download_original_sample(created3.original_sample_id)

            assert len(fetched3.partner_taxonomies) == 2
            assert (int)(fetched3.partner_taxonomies[0].taxonomy_id) == 5833 and (int)(fetched3.partner_taxonomies[1].taxonomy_id) == 5855

            fetched = api_instance.download_original_samples_by_taxa(5833)

            assert len(fetched.original_samples) == 4

            for original_sample in fetched.original_samples:
                if original_sample.original_sample_id == fetched1.original_sample_id:
                    assert original_sample == fetched1
                if original_sample.original_sample_id == fetched2.original_sample_id:
                    assert original_sample == fetched2
                if original_sample.original_sample_id == fetched3.original_sample_id:
                    assert original_sample == fetched3
                if original_sample.original_sample_id == fetched4.original_sample_id:
                    assert original_sample == fetched4

            api_instance.delete_original_sample(created1.original_sample_id)
            api_instance.delete_original_sample(created2.original_sample_id)
            api_instance.delete_original_sample(created3.original_sample_id)
            api_instance.delete_original_sample(created4.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory,
                                     "OriginalSampleApi->test_multiple_partner_species", error)
