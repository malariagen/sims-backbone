import openapi_client
from openapi_client.rest import ApiException

from test_base import TestBase
from datetime import date
import urllib

import uuid
import pytest

class TestAssayDatum(TestBase):


    def create_assay_datum(self, api_factory):

        api_instance = api_factory.AssayDataApi()
        ds_api_instance = api_factory.DerivativeSampleApi()
        os_api_instance = api_factory.OriginalSampleApi()

        try:

            o_samp = openapi_client.OriginalSample(None, study_name='5004-MD-UP')
            orig_samp = os_api_instance.create_original_sample(o_samp)

            samp1 = openapi_client.DerivativeSample(None,
                                                    original_sample_id=orig_samp.original_sample_id)
            created1 = ds_api_instance.create_derivative_sample(samp1)

            samp = openapi_client.AssayDatum(None,
                                             derivative_sample_id=created1.derivative_sample_id,
                                             derivative_sample=created1)

            return samp

        except ApiException as error:
            self.check_api_exception(api_factory, "AssayDataApi->create_assay_datum", error)

    def delete_assay_datum(self, api_factory, samp):

        api_instance = api_factory.AssayDataApi()
        ds_api_instance = api_factory.DerivativeSampleApi()
        os_api_instance = api_factory.OriginalSampleApi()

        try:

            api_instance.delete_assay_datum(samp.assay_datum_id)
            ds_api_instance.delete_derivative_sample(samp.derivative_sample_id)
            os_api_instance.delete_original_sample(samp.derivative_sample.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "AssayDataApi->create_assay_datum", error)
    """
    """
    def test_ad_create(self, api_factory):

        api_instance = api_factory.AssayDataApi()

        try:

            samp = self.create_assay_datum(api_factory)
            created = api_instance.create_assay_datum(assay_datum=samp)
            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to create_assay_datum succeeded')

            fetched = api_instance.download_assay_datum(created.assay_datum_id)
            assert created == fetched, "create response != download response"
            fetched.assay_datum_id = None
            assert samp == fetched, "upload != download response"
            self.delete_assay_datum(api_factory, created)

        except ApiException as error:
            self.check_api_exception(api_factory, "AssayDataApi->create_assay_datum", error)

    """
    """
    def test_ad_create_acc_date(self, api_factory):

        api_instance = api_factory.AssayDataApi()

        try:

            if api_factory.is_authorized(None):
                samp = self.create_assay_datum(api_factory)
                samp.acc_date = date(2019, 11, 6)
                created = api_instance.create_assay_datum(assay_datum=samp)

                fetched = api_instance.download_assay_datum(created.assay_datum_id)
                assert created == fetched, "create response != download response"
                fetched.assay_datum_id = None
                assert samp == fetched, "upload != download response"
                self.delete_assay_datum(api_factory, created)

        except ApiException as error:
            self.check_api_exception(api_factory, "AssayDataApi->create_assay_datum", error)

    """
    """
    def test_ad_delete(self, api_factory):

        api_instance = api_factory.AssayDataApi()

        try:

            samp = self.create_assay_datum(api_factory)
            created = api_instance.create_assay_datum(samp)
            self.delete_assay_datum(api_factory, created)
            with pytest.raises(ApiException, status=404):
                fetched = api_instance.download_assay_datum(created.assay_datum_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "AssayDataApi->create_assay_datum", error)


    """
    """
    def test_ad_delete_missing(self, api_factory):

        api_instance = api_factory.AssayDataApi()

        try:

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    api_instance.delete_assay_datum(str(uuid.uuid4()))
            else:
                with pytest.raises(ApiException, status=403):
                    api_instance.delete_assay_datum(str(uuid.uuid4()))

        except ApiException as error:
            self.check_api_exception(api_factory, "AssayDataApi->delete_assay_datum", error)


    """
    """
    def test_ad_duplicate_key(self, api_factory):

        if not api_factory.is_authorized(None):
            return

        api_instance = api_factory.AssayDataApi()

        try:

            samp = self.create_assay_datum(api_factory)
            samp.attrs = [
                openapi_client.Attr(attr_type='assay_datum_id', attr_value='1234',
                                    attr_source='same')
            ]
            created = api_instance.create_assay_datum(samp)

            with pytest.raises(ApiException, status=422):
                created = api_instance.create_assay_datum(samp)

            self.delete_assay_datum(api_factory, created)

        except ApiException as error:
            self.check_api_exception(api_factory, "AssayDataApi->create_assay_datum", error)

    """
    """
    def test_ad_duplicate_key_allowed(self, api_factory):

        if not api_factory.is_authorized(None):
            return

        api_instance = api_factory.AssayDataApi()

        try:

            samp = self.create_assay_datum(api_factory)
            samp.attrs = [
                openapi_client.Attr(attr_type='oxford', attr_value='1234',
                                    attr_source='same')
            ]
            created = api_instance.create_assay_datum(samp)

            created1 = api_instance.create_assay_datum(samp)

            api_instance.delete_assay_datum(created1.assay_datum_id)
            self.delete_assay_datum(api_factory, created)

        except ApiException as error:
            self.check_api_exception(api_factory, "AssayDataApi->create_assay_datum", error)


    """
    """
    def test_ad_attr_lookup(self, api_factory):

        if not api_factory.is_authorized(None):
            return
        api_instance = api_factory.AssayDataApi()

        try:

            samp = self.create_assay_datum(api_factory)
            samp.attrs = [
                openapi_client.Attr(attr_type='oxford', attr_value='123456')
            ]

            created = api_instance.create_assay_datum(samp)
            results = api_instance.download_assay_data_by_attr('oxford', '123456')
            looked_up = results.assay_data[0]

            fetched = api_instance.download_assay_datum(looked_up.assay_datum_id)

            assert created == fetched, "create response != download response"

            fetched.assay_datum_id = None
            assert samp == fetched, "upload != download response"

            self.delete_assay_datum(api_factory, created)

        except ApiException as error:
            self.check_api_exception(api_factory, "AssayDataApi->create_assay_datum", error)


    """
    """
    def test_ad_os_attr_lookup_missing(self, api_factory):

        if not api_factory.is_authorized(None):
            return
        api_instance = api_factory.AssayDataApi()

        try:

            if api_factory.is_authorized(None):
                results = api_instance.download_assay_data_by_os_attr('ds_os_attr',
                                                                      'ad123456_404')
                assert not results.assay_data
            else:
                with pytest.raises(ApiException, status=403):
                    results = api_instance.download_assay_data_by_os_attr('ds_os_attr',
                                                                          'ad123456_403')

        except ApiException as error:
            self.check_api_exception(api_factory, "AssayDataApi->update_assay_datum", error)

    """
    """
    def test_ad_os_attr_lookup(self, api_factory):

        if not api_factory.is_authorized(None):
            return
        api_instance = api_factory.AssayDataApi()

        os_api_instance = api_factory.OriginalSampleApi()
        ds_api_instance = api_factory.DerivativeSampleApi()

        try:


            samp = openapi_client.OriginalSample(None, study_name='5000-MD-UP')
            samp.attrs = [
                openapi_client.Attr(attr_type='ds_os_attr', attr_value='ad123456')
            ]
            created = os_api_instance.create_original_sample(samp)
            samp1 = openapi_client.DerivativeSample(None,
                                                    original_sample_id=created.original_sample_id)
            samp2 = openapi_client.DerivativeSample(None,
                                                    original_sample_id=created.original_sample_id)

            samp1.attrs = [
                openapi_client.Attr(attr_type='test1', attr_value='test1',
                                    attr_source='ds_os_attr')
            ]
            samp2.attrs = [
                openapi_client.Attr(attr_type='test2', attr_value='test2',
                                    attr_source='ds_os_attr')
            ]
            created1 = ds_api_instance.create_derivative_sample(samp1)
            created2 = ds_api_instance.create_derivative_sample(samp2)

            ad_samp = openapi_client.AssayDatum(None,
                                                derivative_sample_id=created1.derivative_sample_id)
            ad_samp.attrs = [
                openapi_client.Attr(attr_type='oxford', attr_value='123456')
            ]
            ad_created = api_instance.create_assay_datum(ad_samp)

            results = ds_api_instance.download_derivative_samples_by_os_attr('ds_os_attr', 'ad123456')

            results = api_instance.download_assay_data_by_os_attr('ds_os_attr', 'ad123456')
            results.assay_data[0].derivative_sample = results.derivative_samples[results.assay_data[0].derivative_sample_id]
            looked_up = results.assay_data[0]

            fetched = api_instance.download_assay_datum(looked_up.assay_datum_id)

            assert ad_created == fetched, "create response != download response"

            fetched.assay_datum_id = None
            fetched.derivative_sample = None
            assert ad_samp == fetched, "upload != download response"

            assert looked_up == ad_created

            api_instance.delete_assay_datum(ad_created.assay_datum_id)
            ds_api_instance.delete_derivative_sample(created1.derivative_sample_id)
            ds_api_instance.delete_derivative_sample(created2.derivative_sample_id)
            os_api_instance.delete_original_sample(created.original_sample_id)


        except ApiException as error:
            self.check_api_exception(api_factory, "AssayDataApi->create_assay_datum", error)

    """
    """
    def test_ad_attr_merge(self, api_factory):

        if not api_factory.is_authorized(None):
            return
        api_instance = api_factory.AssayDataApi()

        try:

            ident1 = openapi_client.Attr(attr_type='oxford_id', attr_value='1234')
            ident2 = openapi_client.Attr(attr_type='roma_id', attr_value='12345')
            ident3 = openapi_client.Attr(attr_type='lims_id', attr_value='123456')
            samp1 = self.create_assay_datum(api_factory)
            samp1.attrs = [
                ident1
            ]
            created1 = api_instance.create_assay_datum(samp1)

            samp2 = self.create_assay_datum(api_factory)
            samp2.attrs = [
                ident2
            ]
            created2 = api_instance.create_assay_datum(samp2)


            samp3 = self.create_assay_datum(api_factory)
            samp3.attrs = [
                ident1,
                ident2,
                ident3
            ]
            with pytest.raises(ApiException, status=422):
                created3 = api_instance.create_assay_datum(samp3)

            self.delete_assay_datum(api_factory, created1)
            self.delete_assay_datum(api_factory, created2)


        except ApiException as error:
            self.check_api_exception(api_factory, "AssayDataApi->create_assay_datum", error)

    """
    """
    def test_ad_update(self, api_factory):

        if not api_factory.is_authorized(None):
            return
        api_instance = api_factory.AssayDataApi()

        try:

            samp = self.create_assay_datum(api_factory)
            samp.attrs = [
                openapi_client.Attr(attr_type='oxford', attr_value='1234567')
            ]
            created = api_instance.create_assay_datum(samp)
            looked_up = api_instance.download_assay_data_by_attr('oxford', '1234567')
            looked_up = looked_up.assay_data[0]
            new_samp = openapi_client.AssayDatum(created.assay_datum_id,
                                                 derivative_sample=created.derivative_sample,
                                                 derivative_sample_id=created.derivative_sample_id)
            updated = api_instance.update_assay_datum(looked_up.assay_datum_id, new_samp)
            fetched = api_instance.download_assay_datum(looked_up.assay_datum_id)
            assert updated == fetched, "update response != download response"
            assert new_samp == fetched, "update != download response"
            self.delete_assay_datum(api_factory, updated)

        except ApiException as error:
            self.check_api_exception(api_factory, "AssayDataApi->create_assay_datum", error)

    """
    """
    def test_ad_update_acc_date(self, api_factory):

        if not api_factory.is_authorized(None):
            return
        api_instance = api_factory.AssayDataApi()

        try:

            samp = self.create_assay_datum(api_factory)
            samp.attrs = [
                openapi_client.Attr(attr_type='oxford', attr_value='1234567')
            ]
            created = api_instance.create_assay_datum(samp)
            looked_up = api_instance.download_assay_data_by_attr('oxford', '1234567')
            looked_up = looked_up.assay_data[0]
            new_samp = openapi_client.AssayDatum(created.assay_datum_id,
                                                 derivative_sample_id=created.derivative_sample_id,
                                                 derivative_sample=created.derivative_sample,
                                                 acc_date=date(2019, 11, 6))
            new_samp.attrs = samp.attrs
            updated = api_instance.update_assay_datum(looked_up.assay_datum_id, new_samp)
            fetched = api_instance.download_assay_datum(looked_up.assay_datum_id)
            assert updated == fetched, "update response != download response"
            assert new_samp == fetched, "update != download response"
            self.delete_assay_datum(api_factory, updated)

        except ApiException as error:
            self.check_api_exception(api_factory, "AssayDataApi->create_assay_datum", error)

    """
    """
    def test_ad_update_duplicate(self, api_factory):

        if not api_factory.is_authorized(None):
            return
        api_instance = api_factory.AssayDataApi()

        try:

            samp = self.create_assay_datum(api_factory)
            samp.attrs = [
                openapi_client.Attr (attr_type='oxford', attr_value='12345678',
                                           attr_source='upd')
            ]
            created = api_instance.create_assay_datum(samp)
            looked_up = api_instance.download_assay_data_by_attr('oxford', '12345678')
            looked_up = looked_up.assay_data[0]
            new_samp = self.create_assay_datum(api_factory)
            new_samp.attrs = [
                openapi_client.Attr (attr_type='oxford', attr_value='123456789',
                                          attr_source='upd')
            ]
            new_created = api_instance.create_assay_datum(new_samp)
            new_samp.assay_datum_id = looked_up.assay_datum_id
            with pytest.raises(ApiException, status=422):
                updated = api_instance.update_assay_datum(looked_up.assay_datum_id, new_samp)

            self.delete_assay_datum(api_factory, created)
            self.delete_assay_datum(api_factory, new_created)

        except ApiException as error:
            self.check_api_exception(api_factory, "AssayDataApi->create_assay_datum", error)

    """
    """
    def test_ad_update_missing(self, api_factory):

        if not api_factory.is_authorized(None):
            return
        api_instance = api_factory.AssayDataApi()

        try:

            fake_id = str(uuid.uuid4())
            new_samp = openapi_client.AssayDatum(fake_id,
                                                derivative_sample_id=fake_id)


            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    updated = api_instance.update_assay_datum(new_samp.assay_datum_id, new_samp)
            else:
                with pytest.raises(ApiException, status=403):
                    updated = api_instance.update_assay_datum(new_samp.assay_datum_id, new_samp)

        except ApiException as error:
            self.check_api_exception(api_factory, "AssayDataApi->update_assay_datum", error)

    """
    """
    def test_ad_attr_lookup_encode(self, api_factory):

        if not api_factory.is_authorized(None):
            return
        api_instance = api_factory.AssayDataApi()

        try:

            test_id = 'MDG/DK_0005'
            samp = self.create_assay_datum(api_factory)
            samp.attrs = [
                openapi_client.Attr(attr_type='partner_id', attr_value=test_id,
                                    attr_source='encode')
            ]
            created = api_instance.create_assay_datum(samp)

            fetched = api_instance.download_assay_datum(created.assay_datum_id)

            assert created == fetched, "create response != download response"
            fetched.assay_datum_id = None
            assert samp == fetched, "upload != download response"

            results = api_instance.download_assay_data_by_attr('partner_id',
                                                               urllib.parse.quote_plus(test_id))
            looked_up = results.assay_data[0]
            fetched = api_instance.download_assay_datum(looked_up.assay_datum_id)

            assert created == fetched, "create response != download response"
            fetched.assay_datum_id = None
            assert samp == fetched, "upload != download response"

            self.delete_assay_datum(api_factory, created)

        except ApiException as error:
            self.check_api_exception(api_factory, "AssayDataApi->create_assay_datum", error)




    """
    """
    def test_ad_download_assay_datum_permission(self, api_factory):

        if not api_factory.is_authorized(None):
            return
        api_instance = api_factory.AssayDataApi()

        try:
            if not api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=403):
                    api_instance.download_assay_datum(str(uuid.uuid4()))
        except ApiException as error:
            self.check_api_exception(api_factory, "AssayDataApi->download_assay_datum", error)

    """
    """
    def test_ad_download_assay_datum_by_attr_permission(self, api_factory):

        if not api_factory.is_authorized(None):
            return
        api_instance = api_factory.AssayDataApi()

        try:
            if not api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=403):
                    api_instance.download_assay_data_by_attr('partner_id','404')
        except ApiException as error:
            self.check_api_exception(api_factory, "AssayDataApi->download_assay_data_by_attr", error)
