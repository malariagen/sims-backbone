import swagger_client
from swagger_client.rest import ApiException

from test_base import TestBase
from datetime import date
import urllib

import uuid
import pytest

class TestDerivativeSample(TestBase):


    """
    """
    def test_ds_create(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()

        try:

            samp = swagger_client.DerivativeSample(None)
            created = api_instance.create_derivative_sample(samp)
            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to create_derivative_sample succeeded')

            fetched = api_instance.download_derivative_sample(created.derivative_sample_id)
            assert created == fetched, "create response != download response"
            fetched.derivative_sample_id = None
            assert samp == fetched, "upload != download response"
            api_instance.delete_derivative_sample(created.derivative_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->create_derivative_sample", error)

    """
    """
    def test_ds_delete(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()

        try:

            samp = swagger_client.DerivativeSample(None)
            created = api_instance.create_derivative_sample(samp)
            api_instance.delete_derivative_sample(created.derivative_sample_id)
            with pytest.raises(ApiException, status=404):
                fetched = api_instance.download_derivative_sample(created.derivative_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->create_derivative_sample", error)


    """
    """
    def test_ds_delete_missing(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()

        try:

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    api_instance.delete_derivative_sample(str(uuid.uuid4()))
            else:
                with pytest.raises(ApiException, status=403):
                    api_instance.delete_derivative_sample(str(uuid.uuid4()))

        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->delete_derivative_sample", error)

    """
    """
    def test_ds_duplicate_key(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()

        try:

            samp = swagger_client.DerivativeSample(None)
            samp.attrs = [
                swagger_client.Attr (attr_type='oxford', attr_value='1234',
                                     attr_source='same')
            ]
            created = api_instance.create_derivative_sample(samp)

            with pytest.raises(ApiException, status=422):
                created = api_instance.create_derivative_sample(samp)

            api_instance.delete_derivative_sample(created.derivative_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->create_derivative_sample", error)


    """
    """
    def test_ds_attr_lookup(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()

        try:

            samp = swagger_client.DerivativeSample(None)
            samp.attrs = [
                swagger_client.Attr (attr_type='oxford', attr_value='123456')
            ]
            created = api_instance.create_derivative_sample(samp)
            results = api_instance.download_derivative_samples_by_attr('oxford', '123456')
            looked_up = results.derivative_samples[0]

            fetched = api_instance.download_derivative_sample(looked_up.derivative_sample_id)

            assert created == fetched, "create response != download response"

            fetched.derivative_sample_id = None
            assert samp == fetched, "upload != download response"

            api_instance.delete_derivative_sample(created.derivative_sample_id)

            with pytest.raises(ApiException, status=404):
                results = api_instance.download_derivative_samples_by_attr('asdfghjk', '123456')
        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->create_derivative_sample", error)

    """
    """
    def test_ds_attr_merge(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()

        try:

            ident1 = swagger_client.Attr(attr_type='oxford_id', attr_value='1234')
            ident2 = swagger_client.Attr(attr_type='roma_id', attr_value='12345')
            ident3 = swagger_client.Attr(attr_type='lims_id', attr_value='123456')
            samp1 = swagger_client.DerivativeSample(None)
            samp1.attrs = [
                ident1
            ]
            created1 = api_instance.create_derivative_sample(samp1)

            samp2 = swagger_client.DerivativeSample(None)
            samp2.attrs = [
                ident2
            ]
            created2 = api_instance.create_derivative_sample(samp2)


            samp3 = swagger_client.DerivativeSample(None)
            samp3.attrs = [
                ident1,
                ident2,
                ident3
            ]
            with pytest.raises(ApiException, status=422):
                created3 = api_instance.create_derivative_sample(samp3)

            api_instance.delete_derivative_sample(created1.derivative_sample_id)
            api_instance.delete_derivative_sample(created2.derivative_sample_id)


        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->create_derivative_sample", error)

    """
    """
    def test_ds_update(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()

        try:

            samp = swagger_client.DerivativeSample(None)
            samp.attrs = [
                swagger_client.Attr (attr_type='oxford', attr_value='1234567')
            ]
            created = api_instance.create_derivative_sample(samp)
            looked_up = api_instance.download_derivative_samples_by_attr('oxford', '1234567')
            looked_up = looked_up.derivative_samples[0]
            new_samp = swagger_client.DerivativeSample(None)
            updated = api_instance.update_derivative_sample(looked_up.derivative_sample_id, new_samp)
            fetched = api_instance.download_derivative_sample(looked_up.derivative_sample_id)
            assert updated == fetched, "update response != download response"
            fetched.derivative_sample_id = None
            assert new_samp == fetched, "update != download response"
            api_instance.delete_derivative_sample(looked_up.derivative_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->create_derivative_sample", error)

    """
    """
    def test_ds_update_duplicate(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()

        try:

            samp = swagger_client.DerivativeSample(None)
            samp.attrs = [
                swagger_client.Attr (attr_type='oxford', attr_value='12345678',
                                     attr_source='upd')
            ]
            created = api_instance.create_derivative_sample(samp)
            looked_up = api_instance.download_derivative_samples_by_attr('oxford', '12345678')
            looked_up = looked_up.derivative_samples[0]
            new_samp = swagger_client.DerivativeSample(None)
            new_samp.attrs = [
                swagger_client.Attr (attr_type='oxford', attr_value='123456789',
                                     attr_source='upd')
            ]
            new_created = api_instance.create_derivative_sample(new_samp)
            with pytest.raises(ApiException, status=422):
                updated = api_instance.update_derivative_sample(looked_up.derivative_sample_id, new_samp)

            api_instance.delete_derivative_sample(looked_up.derivative_sample_id)
            api_instance.delete_derivative_sample(new_created.derivative_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->create_derivative_sample", error)

    """
    """
    def test_ds_update_missing(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()

        try:

            new_samp = swagger_client.DerivativeSample(None)
            fake_id = uuid.uuid4()
            new_samp.derivative_sample_id = str(fake_id)


            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    updated = api_instance.update_derivative_sample(new_samp.derivative_sample_id, new_samp)
            else:
                with pytest.raises(ApiException, status=403):
                    updated = api_instance.update_derivative_sample(new_samp.derivative_sample_id, new_samp)

        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->update_derivative_sample", error)

    """
    """
    def test_ds_attr_lookup_encode(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()

        try:

            test_id = 'MDG/DK_0005'
            samp = swagger_client.DerivativeSample(None)
            samp.attrs = [
                swagger_client.Attr (attr_type='partner_id', attr_value=test_id,
                                     attr_source='encode')
            ]
            created = api_instance.create_derivative_sample(samp)

            fetched = api_instance.download_derivative_sample(created.derivative_sample_id)

            assert created == fetched, "create response != download response"
            fetched.derivative_sample_id = None
            assert samp == fetched, "upload != download response"

            results = api_instance.download_derivative_samples_by_attr('partner_id',
                                                                       urllib.parse.quote_plus(test_id))
            looked_up = results.derivative_samples[0]
            fetched = api_instance.download_derivative_sample(looked_up.derivative_sample_id)

            assert created == fetched, "create response != download response"
            fetched.derivative_sample_id = None
            assert samp == fetched, "upload != download response"

            api_instance.delete_derivative_sample(created.derivative_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->create_derivative_sample", error)




    """
    """
    def test_ds_download_derivative_sample_permission(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()

        try:
            if not api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=403):
                    api_instance.download_derivative_sample(str(uuid.uuid4()))
        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->download_derivative_sample", error)

    """
    """
    def test_ds_download_derivative_sample_by_attr_permission(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()

        try:
            if not api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=403):
                    api_instance.download_derivative_samples_by_attr('partner_id','404')
        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->download_derivative_samples_by_attr", error)


    """
    """
    def test_ds_os_attr_lookup(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        ds_api_instance = api_factory.DerivativeSampleApi()

        try:

            samp = swagger_client.OriginalSample(None, study_name='5000-MD-UP')
            samp.attrs = [
                swagger_client.Attr (attr_type='ds_os_attr', attr_value='123456')
            ]
            created = api_instance.create_original_sample(samp)
            samp1 = swagger_client.DerivativeSample(None)
            samp2 = swagger_client.DerivativeSample(None)

            samp1.attrs = [
                swagger_client.Attr (attr_type='test1', attr_value='test1',
                                     attr_source='ds_os_attr')
            ]
            samp2.attrs = [
                swagger_client.Attr (attr_type='test2', attr_value='test2',
                                     attr_source='ds_os_attr')
            ]
            samp1.original_sample_id = created.original_sample_id
            samp2.original_sample_id = created.original_sample_id
            created1 = ds_api_instance.create_derivative_sample(samp1)
            created2 = ds_api_instance.create_derivative_sample(samp2)
            results = ds_api_instance.download_derivative_samples_by_os_attr('ds_os_attr', '123456')

            assert results.count == 2
            assert results.derivative_samples[0].derivative_sample_id != results.derivative_samples[1].derivative_sample_id
            assert results.derivative_samples[0].original_sample_id == results.derivative_samples[1].original_sample_id
            assert results.derivative_samples[0].original_sample_id == created.original_sample_id

            ds_api_instance.delete_derivative_sample(created1.derivative_sample_id)
            ds_api_instance.delete_derivative_sample(created2.derivative_sample_id)
            api_instance.delete_original_sample(created.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_ds_os_attr_lookup_missing(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        ds_api_instance = api_factory.DerivativeSampleApi()

        with pytest.raises(ApiException, status=404):
            results = ds_api_instance.download_derivative_samples_by_os_attr('ds_os_attr', 'm123456')


    """
    """
    def test_ds_taxa_lookup(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        ds_api_instance = api_factory.DerivativeSampleApi()
        study_api = api_factory.StudyApi()

        try:

            samp = swagger_client.OriginalSample(None, study_name='5001-MD-UP',
                                                 partner_species='PF')
            samp.attrs = [
                swagger_client.Attr (attr_type='ds_os_attr', attr_value='123456')
            ]
            created = api_instance.create_original_sample(samp)
            study_detail = study_api.download_study('5001')
            study_detail.partner_species[0].taxa = [ swagger_client.Taxonomy(taxonomy_id=5833) ]
            study_api.update_study('5001', study_detail)

            samp1 = swagger_client.DerivativeSample(None)
            samp2 = swagger_client.DerivativeSample(None)

            samp1.attrs = [
                swagger_client.Attr (attr_type='test1', attr_value='test1',
                                     attr_source='ds_os_attr')
            ]
            samp2.attrs = [
                swagger_client.Attr (attr_type='test2', attr_value='test2',
                                     attr_source='ds_os_attr')
            ]
            samp1.original_sample_id = created.original_sample_id
            samp2.original_sample_id = created.original_sample_id
            created1 = ds_api_instance.create_derivative_sample(samp1)
            created2 = ds_api_instance.create_derivative_sample(samp2)
            results = ds_api_instance.download_derivative_samples_by_taxa(5833)

            assert results.count == 2
            assert results.derivative_samples[0].derivative_sample_id != results.derivative_samples[1].derivative_sample_id
            assert results.derivative_samples[0].original_sample_id == results.derivative_samples[1].original_sample_id
            assert results.derivative_samples[0].original_sample_id == created.original_sample_id

            results1 = ds_api_instance.download_derivative_samples_by_taxa(5833,start=0,count=1)

            assert results1.count == 2
            assert len(results1.derivative_samples) == 1
            assert results1.derivative_samples[0].derivative_sample_id == results.derivative_samples[0].derivative_sample_id

            results2 = ds_api_instance.download_derivative_samples_by_taxa(5833,start=1,count=1)

            assert results2.count == 2
            assert len(results2.derivative_samples) == 1
            assert results2.derivative_samples[0].derivative_sample_id == results.derivative_samples[1].derivative_sample_id

            results3 = ds_api_instance.download_derivative_samples(search_filter='taxa:5833')

            assert results3 == results

            ds_api_instance.delete_derivative_sample(created1.derivative_sample_id)
            ds_api_instance.delete_derivative_sample(created2.derivative_sample_id)
            api_instance.delete_original_sample(created.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)


    """
    """
    def test_ds_taxa_lookup_fail(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        se_api_instance = api_factory.SamplingEventApi()
        ds_api_instance = api_factory.DerivativeSampleApi()
        study_api = api_factory.StudyApi()

        try:
            with pytest.raises(ApiException, status=404):
                results = ds_api_instance.download_derivative_samples_by_taxa(5833)

            with pytest.raises(ApiException, status=404):
                results = ds_api_instance.download_derivative_samples_by_taxa(123456)

        except ApiException as error:
            self.check_api_exception(api_factory,
                                     "DerivativeSampleApi->download_derivative_samples_by_taxa", error)

    """
    """
    def test_ds_filter_fail(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()

        try:

            with pytest.raises(ApiException, status=422):
                ffetched = api_instance.download_derivative_samples(search_filter='xxxxx')

            with pytest.raises(ApiException, status=422):
                ffetched = api_instance.download_derivative_samples(search_filter='xxxxx:xxxxx')

            with pytest.raises(ApiException, status=422):
                ffetched = api_instance.download_derivative_samples(search_filter='attr:oxford_id')

        except ApiException as error:
            self.check_api_exception(api_factory, "derivativeSampleApi->download_derivative_samples", error)

