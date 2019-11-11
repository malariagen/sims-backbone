from datetime import date
import urllib

import uuid
import pytest

import openapi_client
from openapi_client.rest import ApiException

from test_base import TestBase

class TestDerivativeSample(TestBase):


    """
    """
    def test_ds_create(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()
        os_api_instance = api_factory.OriginalSampleApi()

        try:

            o_samp = openapi_client.OriginalSample(None, study_name='7007-MD-UP')
            orig_samp = os_api_instance.create_original_sample(o_samp)
            samp = openapi_client.DerivativeSample(None,
                                                   original_sample_id=orig_samp.original_sample_id)

            created = api_instance.create_derivative_sample(samp)
            if not api_factory.is_authorized(orig_samp.study_name[:4]):
                pytest.fail('Unauthorized call to create_derivative_sample succeeded')

            fetched = api_instance.download_derivative_sample(created.derivative_sample_id)
            assert created == fetched, "create response != download response"
            fetched.derivative_sample_id = None
            assert samp == fetched, "upload != download response"
            api_instance.delete_derivative_sample(created.derivative_sample_id)
            os_api_instance.delete_original_sample(orig_samp.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->create_derivative_sample", error)

    """
    """
    def test_ds_create_acc_date(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()
        os_api_instance = api_factory.OriginalSampleApi()

        try:

            o_samp = openapi_client.OriginalSample(None, study_name='7008-MD-UP')
            orig_samp = os_api_instance.create_original_sample(o_samp)
            samp = openapi_client.DerivativeSample(None,
                                                   acc_date=date(2019, 11, 6),
                                                   original_sample_id=orig_samp.original_sample_id)

            created = api_instance.create_derivative_sample(samp)
            if not api_factory.is_authorized(orig_samp.study_name[:4]):
                pytest.fail('Unauthorized call to create_derivative_sample succeeded')

            fetched = api_instance.download_derivative_sample(created.derivative_sample_id)
            assert created == fetched, "create response != download response"
            fetched.derivative_sample_id = None
            assert samp == fetched, "upload != download response"
            api_instance.delete_derivative_sample(created.derivative_sample_id)
            os_api_instance.delete_original_sample(orig_samp.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->create_derivative_sample", error)

    """
    """
    def test_ds_delete(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()
        os_api_instance = api_factory.OriginalSampleApi()

        try:

            o_samp = openapi_client.OriginalSample(None, study_name='7009-MD-UP')
            orig_samp = os_api_instance.create_original_sample(o_samp)

            samp = openapi_client.DerivativeSample(None,
                                                   original_sample_id=orig_samp.original_sample_id)
            created = api_instance.create_derivative_sample(samp)
            api_instance.delete_derivative_sample(created.derivative_sample_id)
            with pytest.raises(ApiException, status=404):
                fetched = api_instance.download_derivative_sample(created.derivative_sample_id)

            os_api_instance.delete_original_sample(orig_samp.original_sample_id)
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
        os_api_instance = api_factory.OriginalSampleApi()

        try:

            o_samp = openapi_client.OriginalSample(None, study_name='7010-MD-UP')
            orig_samp = os_api_instance.create_original_sample(o_samp)

            samp = openapi_client.DerivativeSample(None,
                                                   original_sample_id=orig_samp.original_sample_id)
            samp.attrs = [
                openapi_client.Attr(attr_type='oxford', attr_value='1234',
                                     attr_source='same')
            ]
            created = api_instance.create_derivative_sample(samp)

            with pytest.raises(ApiException, status=422):
                created = api_instance.create_derivative_sample(samp)

            api_instance.delete_derivative_sample(created.derivative_sample_id)
            os_api_instance.delete_original_sample(orig_samp.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->create_derivative_sample", error)


    """
    """
    def test_ds_attr_lookup(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()
        os_api_instance = api_factory.OriginalSampleApi()

        try:

            o_samp = openapi_client.OriginalSample(None, study_name='7011-MD-UP')
            orig_samp = os_api_instance.create_original_sample(o_samp)

            samp = openapi_client.DerivativeSample(None,
                                                   original_sample_id=orig_samp.original_sample_id)
            samp.attrs = [
                openapi_client.Attr(attr_type='oxford', attr_value='123456')
            ]
            created = api_instance.create_derivative_sample(samp)
            results = api_instance.download_derivative_samples_by_attr('oxford', '123456')
            looked_up = results.derivative_samples[0]

            fetched = api_instance.download_derivative_sample(looked_up.derivative_sample_id)

            assert created == fetched, "create response != download response"

            fetched.derivative_sample_id = None
            assert samp == fetched, "upload != download response"

            api_instance.delete_derivative_sample(created.derivative_sample_id)
            os_api_instance.delete_original_sample(orig_samp.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->create_derivative_sample", error)

    """
    """
    def test_ds_attr_lookup_missing(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()

        try:

            results = api_instance.download_derivative_samples_by_attr('asdfghjk', '123456')

            assert not results.derivative_samples
            assert results.count == 0

        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->create_derivative_sample", error)

    """
    """
    def test_ds_attr_merge(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()
        os_api_instance = api_factory.OriginalSampleApi()

        try:

            o_samp = openapi_client.OriginalSample(None, study_name='7012-MD-UP')
            orig_samp = os_api_instance.create_original_sample(o_samp)

            ident1 = openapi_client.Attr(attr_type='oxford_id', attr_value='1234')
            ident2 = openapi_client.Attr(attr_type='roma_id', attr_value='12345')
            ident3 = openapi_client.Attr(attr_type='lims_id', attr_value='123456')
            samp1 = openapi_client.DerivativeSample(None,
                                                    original_sample_id=orig_samp.original_sample_id)
            samp1.attrs = [
                ident1
            ]
            created1 = api_instance.create_derivative_sample(samp1)

            samp2 = openapi_client.DerivativeSample(None,
                                                    original_sample_id=orig_samp.original_sample_id)
            samp2.attrs = [
                ident2
            ]
            created2 = api_instance.create_derivative_sample(samp2)

            samp3 = openapi_client.DerivativeSample(None,
                                                    original_sample_id=orig_samp.original_sample_id)
            samp3.attrs = [
                ident1,
                ident2,
                ident3
            ]
            with pytest.raises(ApiException, status=422):
                created3 = api_instance.create_derivative_sample(samp3)

            api_instance.delete_derivative_sample(created1.derivative_sample_id)
            api_instance.delete_derivative_sample(created2.derivative_sample_id)
            os_api_instance.delete_original_sample(orig_samp.original_sample_id)


        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->create_derivative_sample", error)

    """
    """
    def test_ds_update(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()
        os_api_instance = api_factory.OriginalSampleApi()

        try:

            o_samp = openapi_client.OriginalSample(None, study_name='7013-MD-UP')
            orig_samp = os_api_instance.create_original_sample(o_samp)

            samp = openapi_client.DerivativeSample(None,
                                                   original_sample_id=orig_samp.original_sample_id)
            samp.attrs = [
                openapi_client.Attr(attr_type='oxford', attr_value='1234567')
            ]
            created = api_instance.create_derivative_sample(samp)
            looked_up = api_instance.download_derivative_samples_by_attr('oxford', '1234567')
            looked_up = looked_up.derivative_samples[0]
            new_samp = openapi_client.DerivativeSample(None,
                                                       original_sample_id=orig_samp.original_sample_id)
            updated = api_instance.update_derivative_sample(looked_up.derivative_sample_id, new_samp)
            fetched = api_instance.download_derivative_sample(looked_up.derivative_sample_id)
            assert updated == fetched, "update response != download response"
            fetched.derivative_sample_id = None
            assert new_samp == fetched, "update != download response"
            api_instance.delete_derivative_sample(looked_up.derivative_sample_id)
            os_api_instance.delete_original_sample(orig_samp.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->create_derivative_sample", error)

    """
    """
    def test_ds_update_acc_date(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()
        os_api_instance = api_factory.OriginalSampleApi()

        try:

            o_samp = openapi_client.OriginalSample(None, study_name='7014-MD-UP')
            orig_samp = os_api_instance.create_original_sample(o_samp)

            samp = openapi_client.DerivativeSample(None,
                                                   original_sample_id=orig_samp.original_sample_id)
            samp.attrs = [
                openapi_client.Attr(attr_type='oxford', attr_value='1234567')
            ]
            created = api_instance.create_derivative_sample(samp)
            looked_up = api_instance.download_derivative_samples_by_attr('oxford', '1234567')
            looked_up = looked_up.derivative_samples[0]
            new_samp = openapi_client.DerivativeSample(None,
                                                       original_sample_id=orig_samp.original_sample_id,
                                                       acc_date=date(2019, 11, 6))
            updated = api_instance.update_derivative_sample(looked_up.derivative_sample_id, new_samp)
            fetched = api_instance.download_derivative_sample(looked_up.derivative_sample_id)
            assert updated == fetched, "update response != download response"
            fetched.derivative_sample_id = None
            assert new_samp == fetched, "update != download response"
            api_instance.delete_derivative_sample(looked_up.derivative_sample_id)
            os_api_instance.delete_original_sample(orig_samp.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->create_derivative_sample", error)

    """
    """
    def test_ds_update_duplicate(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()
        os_api_instance = api_factory.OriginalSampleApi()

        try:

            o_samp = openapi_client.OriginalSample(None, study_name='7015-MD-UP')
            orig_samp = os_api_instance.create_original_sample(o_samp)

            samp = openapi_client.DerivativeSample(None,
                                                   original_sample_id=orig_samp.original_sample_id)
            samp.attrs = [
                openapi_client.Attr(attr_type='oxford', attr_value='12345678',
                                    attr_source='upd')
            ]
            created = api_instance.create_derivative_sample(samp)
            looked_up = api_instance.download_derivative_samples_by_attr('oxford', '12345678')
            looked_up = looked_up.derivative_samples[0]
            new_samp = openapi_client.DerivativeSample(None,
                                                       original_sample_id=orig_samp.original_sample_id)
            new_samp.attrs = [
                openapi_client.Attr(attr_type='oxford', attr_value='123456789',
                                    attr_source='upd')
            ]
            new_created = api_instance.create_derivative_sample(new_samp)
            with pytest.raises(ApiException, status=422):
                updated = api_instance.update_derivative_sample(looked_up.derivative_sample_id, new_samp)

            api_instance.delete_derivative_sample(looked_up.derivative_sample_id)
            api_instance.delete_derivative_sample(new_created.derivative_sample_id)
            os_api_instance.delete_original_sample(orig_samp.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->create_derivative_sample", error)

    """
    """
    def test_ds_update_missing(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()

        try:

            new_samp = openapi_client.DerivativeSample(None)
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
        os_api_instance = api_factory.OriginalSampleApi()

        try:

            o_samp = openapi_client.OriginalSample(None, study_name='7016-MD-UP')
            orig_samp = os_api_instance.create_original_sample(o_samp)

            test_id = 'MDG/DK_0005'
            samp = openapi_client.DerivativeSample(None,
                                                   original_sample_id=orig_samp.original_sample_id)
            samp.attrs = [
                openapi_client.Attr (attr_type='partner_id', attr_value=test_id,
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
            os_api_instance.delete_original_sample(orig_samp.original_sample_id)

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

            samp = openapi_client.OriginalSample(None, study_name='7000-MD-UP')
            samp.attrs = [
                openapi_client.Attr (attr_type='ds_os_attr', attr_value='123456')
            ]
            created = api_instance.create_original_sample(samp)
            samp1 = openapi_client.DerivativeSample(None)
            samp2 = openapi_client.DerivativeSample(None)

            samp1.attrs = [
                openapi_client.Attr (attr_type='test1', attr_value='test1',
                                     attr_source='ds_os_attr')
            ]
            samp2.attrs = [
                openapi_client.Attr (attr_type='test2', attr_value='test2',
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

        if api_factory.is_authorized(None):
            results = ds_api_instance.download_derivative_samples_by_os_attr('ds_os_attr', 'm123456')
            assert not results.derivative_samples
            assert results.count == 0
        else:
            with pytest.raises(ApiException, status=403):
                results = ds_api_instance.download_derivative_samples_by_os_attr('ds_os_attr', 'm123456')



    def create_test_samples(self, api_factory, study_name):

        api_instance = api_factory.OriginalSampleApi()
        ds_api_instance = api_factory.DerivativeSampleApi()
        study_api = api_factory.StudyApi()

        samp = openapi_client.OriginalSample(None, study_name=study_name,
                                             partner_species='PF')
        #samp.attrs = [
        #    openapi_client.Attr (attr_type='ds_os_attr', attr_value='123456')
        #]
        created = api_instance.create_original_sample(samp)
        study_detail = study_api.download_study(study_name)
        study_detail.partner_species[0].taxa = [ openapi_client.Taxonomy(taxonomy_id=5833) ]
        study_api.update_study(study_name, study_detail)

        samp1 = openapi_client.DerivativeSample(None)
        samp2 = openapi_client.DerivativeSample(None)

        samp1.attrs = [
            openapi_client.Attr (attr_type='test1', attr_value='test1',
                                 attr_source='ds_os_attr')
        ]
        samp2.attrs = [
            openapi_client.Attr (attr_type='test2', attr_value='test2',
                                 attr_source='ds_os_attr')
        ]
        samp1.original_sample_id = created.original_sample_id
        samp2.original_sample_id = created.original_sample_id
        created1 = ds_api_instance.create_derivative_sample(samp1)
        created2 = ds_api_instance.create_derivative_sample(samp2)

        return created, created1, created2

    """
    """
    def test_ds_taxa_lookup(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        ds_api_instance = api_factory.DerivativeSampleApi()
        study_api = api_factory.StudyApi()

        try:
            study_name = '7001-MD-UP'
            created, created1, created2 = self.create_test_samples(api_factory, study_name)
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
            self.check_api_exception(api_factory, "DerivativeSampleApi->create_derivative_sample", error)


    """
    """
    def test_ds_taxa_lookup_fail(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        se_api_instance = api_factory.SamplingEventApi()
        ds_api_instance = api_factory.DerivativeSampleApi()
        study_api = api_factory.StudyApi()

        try:
            results = ds_api_instance.download_derivative_samples_by_taxa(5833)

            assert not results.derivative_samples
            assert results.count == 0

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

    """
    """
    def test_ds_study_lookup(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        ds_api_instance = api_factory.DerivativeSampleApi()

        try:
            study_code = '7002-MD-UP'
            created, created1, created2 = self.create_test_samples(api_factory,
                                                                   study_code)

            fetched = ds_api_instance.download_derivative_samples_by_study(study_code)

            assert fetched.count == 2, "Study not found"

            assert created1 == fetched.derivative_samples[0] or created1 == fetched.derivative_samples[1], "create response != download response"

            assert not fetched.derivative_samples[0] == fetched.derivative_samples[1], "create response != download response"
            ffetched = ds_api_instance.download_derivative_samples(search_filter='studyId:' + study_code)

            assert ffetched.count == 2, "Study not found"

            assert ffetched == fetched

            ds_api_instance.delete_derivative_sample(created1.derivative_sample_id)
            ds_api_instance.delete_derivative_sample(created2.derivative_sample_id)
            api_instance.delete_original_sample(created.original_sample_id)

            with pytest.raises(ApiException, status=404):
                fetched = ds_api_instance.download_derivative_samples_by_study('asdfhjik')
        except ApiException as error:
            self.check_api_exception(api_factory,
                                     "derivativeSampleApi->create_derivative_sample", error)

    """
    """
    def test_ds_study_lookup_paged(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        ds_api_instance = api_factory.DerivativeSampleApi()

        try:
            study_code = '7003-MD-UP'

            os_samp = openapi_client.OriginalSample(None, study_name=study_code)
            os_created = api_instance.create_original_sample(os_samp)
            for i in range(5):
                samp = openapi_client.DerivativeSample(None)
                samp.original_sample_id = os_created.original_sample_id
                created = ds_api_instance.create_derivative_sample(samp)


            fetched1 = ds_api_instance.download_derivative_samples_by_study(study_code, start=0, count=2)

            assert len(fetched1.derivative_samples) ==2, "Wrong number of original_samples returned"
            assert fetched1.count == 5, "Wrong total of original_samples returned"

            ffetched = ds_api_instance.download_derivative_samples(search_filter='studyId:' + study_code,
                                                              start=0, count=2)

            assert ffetched == fetched1

            fetched2 = ds_api_instance.download_derivative_samples_by_study(study_code, start=2, count=5)

            #Gets second tranche and also attempts to retrieve more than exist
            assert len(fetched2.derivative_samples) ==3, "Wrong number of original_samples returned"
            assert fetched2.count == 5, "Wrong total of original_samples returned"

            ids = []
            for derivative_sample in fetched1.derivative_samples + fetched2.derivative_samples:
                assert not derivative_sample.derivative_sample_id in ids, "derivativeSample returned twice"
                ids.append(derivative_sample.derivative_sample_id)

            #Check that it's the correct number of *unique* events

            #Clean up
            fetch_all = ds_api_instance.download_derivative_samples_by_study(study_code)

            for derivative_sample in fetch_all.derivative_samples:
                ds_api_instance.delete_derivative_sample(derivative_sample.derivative_sample_id)
            api_instance.delete_original_sample(os_created.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_ds_event_set_lookup(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        se_api_instance = api_factory.SamplingEventApi()
        es_api_instance = api_factory.EventSetApi()
        ds_api_instance = api_factory.DerivativeSampleApi()

        try:

            event_set_name = 'test_ds_event_set_lookup'
            study_code = '7004-MD-UP'

            created_es = es_api_instance.create_event_set(event_set_name)

            sampling_event = openapi_client.SamplingEvent(None, date(2017, 10, 10),
                                                          doc_accuracy='month')

            created_se = se_api_instance.create_sampling_event(sampling_event)

            created_set = es_api_instance.create_event_set_item(event_set_name, created_se.sampling_event_id)

            created, created1, created2 = self.create_test_samples(api_factory,
                                                                   study_code)

            created.sampling_event_id = created_se.sampling_event_id

            api_instance.update_original_sample(created.original_sample_id,
                                                created)

            results = ds_api_instance.download_derivative_samples_by_event_set(event_set_name)
            looked_up = results.derivative_samples[0]

            fetched = ds_api_instance.download_derivative_sample(looked_up.derivative_sample_id)

            assert created1 == fetched or created2 == fetched, "create response != download response"

            assert results.attr_types == ['test1', 'test2']

            se_api_instance.delete_sampling_event(created_se.sampling_event_id)

            es_api_instance.delete_event_set(event_set_name)

            ds_api_instance.delete_derivative_sample(created1.derivative_sample_id)
            ds_api_instance.delete_derivative_sample(created2.derivative_sample_id)
            api_instance.delete_original_sample(created.original_sample_id)

            with pytest.raises(ApiException, status=404):
                results = api_instance.download_original_samples_by_event_set(event_set_name)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_ds_event_set_lookup_missing(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            event_set_name = 'test_ds_event_set_lookup'

            with pytest.raises(ApiException, status=404):
                results = api_instance.download_original_samples_by_event_set(event_set_name)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_ds_event_set_lookup_paged(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        se_api_instance = api_factory.SamplingEventApi()
        es_api_instance = api_factory.EventSetApi()
        ds_api_instance = api_factory.DerivativeSampleApi()

        try:

            event_set_name = 'test_ds_event_set_lookup'
            study_code = '7005-MD-UP'

            created_es = es_api_instance.create_event_set(event_set_name)

            sampling_event = openapi_client.SamplingEvent(None, date(2017, 10, 10),
                                                          doc_accuracy='month')

            created_se = se_api_instance.create_sampling_event(sampling_event)

            created_set = es_api_instance.create_event_set_item(event_set_name, created_se.sampling_event_id)

            created, created1, created2 = self.create_test_samples(api_factory,
                                                                   study_code)

            created.sampling_event_id = created_se.sampling_event_id

            api_instance.update_original_sample(created.original_sample_id,
                                                created)

            results = ds_api_instance.download_derivative_samples_by_event_set(event_set_name,
                                                                    start=0,count=1)
            looked_up = results.derivative_samples[0]

            fetched = ds_api_instance.download_derivative_sample(looked_up.derivative_sample_id)

            assert created1 == fetched or created2 == fetched, "create response != download response"

            assert results.attr_types == ['test1', 'test2']

            assert len(results.derivative_samples) == 1
            assert results.count == 2

            se_api_instance.delete_sampling_event(created_se.sampling_event_id)

            es_api_instance.delete_event_set(event_set_name)

            ds_api_instance.delete_derivative_sample(created1.derivative_sample_id)
            ds_api_instance.delete_derivative_sample(created2.derivative_sample_id)
            api_instance.delete_original_sample(created.original_sample_id)

            with pytest.raises(ApiException, status=404):
                results = api_instance.download_original_samples_by_event_set(event_set_name)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_ds_event_set_lookup_no_ds(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        se_api_instance = api_factory.SamplingEventApi()
        es_api_instance = api_factory.EventSetApi()
        ds_api_instance = api_factory.DerivativeSampleApi()

        try:

            event_set_name = 'test_ds_event_set_lookup'
            study_code = '7005-MD-UP'

            created_es = es_api_instance.create_event_set(event_set_name)

            sampling_event = openapi_client.SamplingEvent(None, date(2017, 10, 10),
                                                          doc_accuracy='month')

            created_se = se_api_instance.create_sampling_event(sampling_event)

            created_set = es_api_instance.create_event_set_item(event_set_name, created_se.sampling_event_id)


            if api_factory.is_authorized(None):
                res = ds_api_instance.download_derivative_samples_by_event_set(event_set_name)

                assert not res.derivative_samples
            else:
                with pytest.raises(ApiException, status=403):
                    ds_api_instance.download_derivative_samples_by_event_set(event_set_name)

            se_api_instance.delete_sampling_event(created_se.sampling_event_id)

            es_api_instance.delete_event_set(event_set_name)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_ds_event_set_lookup_missing(self, api_factory):

        ds_api_instance = api_factory.DerivativeSampleApi()

        try:

            with pytest.raises(ApiException, status=404):
                ds_api_instance.download_derivative_samples_by_event_set('does not exist')

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_ds_parent_create(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()
        os_api_instance = api_factory.OriginalSampleApi()

        try:

            o_samp = openapi_client.OriginalSample(None, study_name='7017-MD-UP')
            orig_samp = os_api_instance.create_original_sample(o_samp)

            parent_samp = openapi_client.DerivativeSample(None,
                                                          original_sample_id=orig_samp.original_sample_id)
            parent_created = api_instance.create_derivative_sample(parent_samp)

            samp = openapi_client.DerivativeSample(None,
                                                   original_sample_id=orig_samp.original_sample_id)

            samp.parent_derivative_sample_id = parent_created.derivative_sample_id

            created = api_instance.create_derivative_sample(samp)
            if not api_factory.is_authorized(orig_samp.study_name[:4]):
                pytest.fail('Unauthorized call to create_derivative_sample succeeded')

            fetched = api_instance.download_derivative_sample(created.derivative_sample_id)
            assert created == fetched, "create response != download response"
            fetched.derivative_sample_id = None
            assert samp == fetched, "upload != download response"
            api_instance.delete_derivative_sample(parent_created.derivative_sample_id)
            api_instance.delete_derivative_sample(created.derivative_sample_id)
            os_api_instance.delete_original_sample(orig_samp.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->create_derivative_sample", error)

    """
    """
    def test_ds_parent_update(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()
        os_api_instance = api_factory.OriginalSampleApi()

        try:

            o_samp = openapi_client.OriginalSample(None, study_name='7018-MD-UP')
            orig_samp = os_api_instance.create_original_sample(o_samp)

            parent_samp = openapi_client.DerivativeSample(None,
                                                          original_sample_id=orig_samp.original_sample_id)
            parent_created = api_instance.create_derivative_sample(parent_samp)

            samp = openapi_client.DerivativeSample(None,
                                                   original_sample_id=orig_samp.original_sample_id)
            samp.attrs = [
                openapi_client.Attr (attr_type='oxford', attr_value='1234567')
            ]
            created = api_instance.create_derivative_sample(samp)
            looked_up = api_instance.download_derivative_samples_by_attr('oxford', '1234567')
            looked_up = looked_up.derivative_samples[0]
            new_samp = openapi_client.DerivativeSample(None,
                                                       original_sample_id=orig_samp.original_sample_id)
            new_samp.parent_derivative_sample_id = parent_created.derivative_sample_id
            updated = api_instance.update_derivative_sample(looked_up.derivative_sample_id, new_samp)
            fetched = api_instance.download_derivative_sample(looked_up.derivative_sample_id)
            assert updated == fetched, "update response != download response"
            fetched.derivative_sample_id = None
            assert new_samp == fetched, "update != download response"

            assert fetched.parent_derivative_sample_id == new_samp.parent_derivative_sample_id

            api_instance.delete_derivative_sample(parent_created.derivative_sample_id)
            api_instance.delete_derivative_sample(looked_up.derivative_sample_id)
            os_api_instance.delete_original_sample(orig_samp.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->create_derivative_sample", error)

    """
    """
    def test_ds_nested_delete_ds(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()
        os_api_instance = api_factory.OriginalSampleApi()

        try:

            o_samp = openapi_client.OriginalSample(None, study_name='7019-MD-UP')
            orig_samp = os_api_instance.create_original_sample(o_samp)

            parent_samp = openapi_client.DerivativeSample(None,
                                                          orig_samp.original_sample_id)

            parent_created = api_instance.create_derivative_sample(parent_samp)

            samp = openapi_client.DerivativeSample(None,
                                                   orig_samp.original_sample_id)

            samp.parent_derivative_sample_id = parent_created.derivative_sample_id

            created = api_instance.create_derivative_sample(samp)

            child_samp = openapi_client.DerivativeSample(None,
                                                         orig_samp.original_sample_id)

            child_samp.parent_derivative_sample_id = created.derivative_sample_id

            child_created = api_instance.create_derivative_sample(child_samp)

            api_instance.delete_derivative_sample(created.derivative_sample_id)

            fetched = api_instance.download_derivative_sample(child_created.derivative_sample_id)

            assert fetched.parent_derivative_sample_id == parent_created.derivative_sample_id

            api_instance.delete_derivative_sample(child_created.derivative_sample_id)
            api_instance.delete_derivative_sample(parent_created.derivative_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->create_derivative_sample", error)

    """
    """
    def test_ds_nested_delete_os(self, api_factory):

        api_instance = api_factory.DerivativeSampleApi()
        os_api_instance = api_factory.OriginalSampleApi()

        try:

            parent_samp = openapi_client.OriginalSample(None,
                                                        study_name='7006-MD-UP')
            parent_created = os_api_instance.create_original_sample(parent_samp)

            samp = openapi_client.DerivativeSample(None)

            samp.original_sample_id = parent_created.original_sample_id

            created = api_instance.create_derivative_sample(samp)

            child_samp = openapi_client.DerivativeSample(None)

            child_samp.parent_derivative_sample_id = created.derivative_sample_id

            child_created = api_instance.create_derivative_sample(child_samp)

            api_instance.delete_derivative_sample(created.derivative_sample_id)

            fetched = api_instance.download_derivative_sample(child_created.derivative_sample_id)

            assert fetched.original_sample_id == parent_created.original_sample_id

            api_instance.delete_derivative_sample(child_created.derivative_sample_id)
            os_api_instance.delete_original_sample(parent_created.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DerivativeSampleApi->create_derivative_sample", error)
