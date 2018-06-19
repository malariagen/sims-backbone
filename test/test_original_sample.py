import swagger_client
from swagger_client.rest import ApiException

from test_base import TestBase
from datetime import date
import urllib

import uuid
import pytest

class TestOriginalSample(TestBase):


    """
    """
    def test_os_create(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp = swagger_client.OriginalSample(None, study_name='1000-MD-UP')
            created = api_instance.create_original_sample(samp)
            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to create_original_sample succeeded')

            fetched = api_instance.download_original_sample(created.original_sample_id)
            assert created == fetched, "create response != download response"
            fetched.original_sample_id = None
            assert samp == fetched, "upload != download response"
            api_instance.delete_original_sample(created.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_delete(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp = swagger_client.OriginalSample(None, study_name='1001-MD-UP')
            created = api_instance.create_original_sample(samp)
            api_instance.delete_original_sample(created.original_sample_id)
            with pytest.raises(ApiException, status=404):
                fetched = api_instance.download_original_sample(created.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)


    """
    """
    def test_os_delete_missing(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    api_instance.delete_original_sample(str(uuid.uuid4()))
            else:
                with pytest.raises(ApiException, status=403):
                    api_instance.delete_original_sample(str(uuid.uuid4()))

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->delete_original_sample", error)

    """
    """
    def test_os_duplicate_key(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp = swagger_client.OriginalSample(None, study_name='1002-MD-UP')
            samp.attrs = [
                swagger_client.Attr (attr_type='oxford', attr_value='1234',
                                           attr_source='same')
            ]
            created = api_instance.create_original_sample(samp)

            with pytest.raises(ApiException, status=422):
                created = api_instance.create_original_sample(samp)

            api_instance.delete_original_sample(created.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_duplicate_partner_key(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp = swagger_client.OriginalSample(None, study_name='1003-MD-UP')
            samp.attrs = [
                swagger_client.Attr (attr_type='partner_id', attr_value='12345')
            ]
            created = api_instance.create_original_sample(samp)

            created1 = api_instance.create_original_sample(samp)


            api_instance.delete_original_sample(created.original_sample_id)
            api_instance.delete_original_sample(created1.original_sample_id)

            assert created.original_sample_id != created1.original_sample_id

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_duplicate_individual_id(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp = swagger_client.OriginalSample(None, study_name='1025-MD-UP')
            samp.attrs = [
                swagger_client.Attr (attr_type='individual_id', attr_value='12345')
            ]
            created = api_instance.create_original_sample(samp)

            created1 = api_instance.create_original_sample(samp)


            api_instance.delete_original_sample(created.original_sample_id)
            api_instance.delete_original_sample(created1.original_sample_id)

            assert created.original_sample_id != created1.original_sample_id

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)


    """
    """
    def test_os_attr_lookup(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp = swagger_client.OriginalSample(None, study_name='1004-MD-UP')
            samp.attrs = [
                swagger_client.Attr (attr_type='oxford', attr_value='123456')
            ]
            created = api_instance.create_original_sample(samp)
            results = api_instance.download_original_samples_by_attr('oxford', '123456')
            looked_up = results.original_samples[0]

            fetched = api_instance.download_original_sample(looked_up.original_sample_id)

            assert created == fetched, "create response != download response"

            ffetched = api_instance.download_original_samples(filter='attr:oxford:123456')

            assert ffetched == results

            fetched.original_sample_id = None
            assert samp == fetched, "upload != download response"

            api_instance.delete_original_sample(created.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_attr_lookup_by_study(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp = swagger_client.OriginalSample(None, study_name='1022-MD-UP')
            samp.attrs = [
                swagger_client.Attr (attr_type='partner_id', attr_value='123456')
            ]
            created = api_instance.create_original_sample(samp)
            looked_up = api_instance.download_original_samples_by_attr('partner_id', '123456',
                                                                            study_name='1022')
            assert looked_up.count == 1


            with pytest.raises(ApiException, status=404):
                looked_up = api_instance.download_original_samples_by_attr('oxford', '123456',
                                                                            study_name='9999')

            created1 = api_instance.create_original_sample(samp)

            looked_up = api_instance.download_original_samples_by_attr('partner_id', '123456',
                                                                            study_name='1022')
            assert looked_up.count == 2

            ffetched = api_instance.download_original_samples(filter='attr:partner_id:123456:1022')

            assert ffetched == looked_up

            api_instance.delete_original_sample(created.original_sample_id)
            api_instance.delete_original_sample(created1.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_attr_merge(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            ident1 = swagger_client.Attr(attr_type='oxford_id', attr_value='1234')
            ident2 = swagger_client.Attr(attr_type='roma_id', attr_value='12345')
            ident3 = swagger_client.Attr(attr_type='lims_id', attr_value='123456')
            samp1 = swagger_client.OriginalSample(None, study_name='1022-MD-UP')
            samp1.attrs = [
                ident1
            ]
            created1 = api_instance.create_original_sample(samp1)

            samp2 = swagger_client.OriginalSample(None, study_name='1022-MD-UP')
            samp2.attrs = [
                ident2
            ]
            created2 = api_instance.create_original_sample(samp2)


            samp3 = swagger_client.OriginalSample(None, study_name='1022-MD-UP')
            samp3.attrs = [
                ident1,
                ident2,
                ident3
            ]
            with pytest.raises(ApiException, status=422):
                created3 = api_instance.create_original_sample(samp3)

            api_instance.delete_original_sample(created1.original_sample_id)
            api_instance.delete_original_sample(created2.original_sample_id)


        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_update(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp = swagger_client.OriginalSample(None, study_name='1005-MD-UP',)
            samp.attrs = [
                swagger_client.Attr (attr_type='oxford', attr_value='1234567')
            ]
            created = api_instance.create_original_sample(samp)
            looked_up = api_instance.download_original_samples_by_attr('oxford', '1234567')
            looked_up = looked_up.original_samples[0]
            new_samp = swagger_client.OriginalSample(None, study_name='0001-MD-UP')
            updated = api_instance.update_original_sample(looked_up.original_sample_id, new_samp)
            fetched = api_instance.download_original_sample(looked_up.original_sample_id)
            assert updated == fetched, "update response != download response"
            fetched.original_sample_id = None
            assert new_samp == fetched, "update != download response"
            api_instance.delete_original_sample(looked_up.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_update_duplicate(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp = swagger_client.OriginalSample(None, study_name='1006-MD-UP')
            samp.attrs = [
                swagger_client.Attr (attr_type='oxford', attr_value='12345678',
                                           attr_source='upd')
            ]
            created = api_instance.create_original_sample(samp)
            looked_up = api_instance.download_original_samples_by_attr('oxford', '12345678')
            looked_up = looked_up.original_samples[0]
            new_samp = swagger_client.OriginalSample(None, study_name='0001-MD-UP')
            new_samp.attrs = [
                swagger_client.Attr (attr_type='oxford', attr_value='123456789',
                                          attr_source='upd')
            ]
            new_created = api_instance.create_original_sample(new_samp)
            with pytest.raises(ApiException, status=422):
                updated = api_instance.update_original_sample(looked_up.original_sample_id, new_samp)

            api_instance.delete_original_sample(looked_up.original_sample_id)
            api_instance.delete_original_sample(new_created.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_update_missing(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            new_samp = swagger_client.OriginalSample(None, study_name='1007-MD-UP')
            fake_id = uuid.uuid4()
            new_samp.original_sample_id = str(fake_id)


            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    updated = api_instance.update_original_sample(new_samp.original_sample_id, new_samp)
            else:
                with pytest.raises(ApiException, status=403):
                    updated = api_instance.update_original_sample(new_samp.original_sample_id, new_samp)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->update_original_sample", error)

    """
    """
    def test_os_attr_lookup_encode(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            test_id = 'MDG/DK_0005'
            samp = swagger_client.OriginalSample(None, study_name='1008-MD-UP')
            samp.attrs = [
                swagger_client.Attr (attr_type='partner_id', attr_value=test_id,
                                          attr_source='encode')
            ]
            created = api_instance.create_original_sample(samp)

            fetched = api_instance.download_original_sample(created.original_sample_id)

            assert created == fetched, "create response != download response"
            fetched.original_sample_id = None
            assert samp == fetched, "upload != download response"

            results = api_instance.download_original_samples_by_attr('partner_id',
                                                                      urllib.parse.quote_plus(test_id))
            looked_up = results.original_samples[0]
            fetched = api_instance.download_original_sample(looked_up.original_sample_id)

            assert created == fetched, "create response != download response"
            fetched.original_sample_id = None
            assert samp == fetched, "upload != download response"

            ffetched = api_instance.download_original_samples(filter=urllib.parse.quote_plus('attr:partner_id:' + test_id))

            assert ffetched == results

            api_instance.delete_original_sample(created.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)


    """
    """
    def test_os_study_lookup(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:
            study_code = '1020-MD-UP'

            samp = swagger_client.OriginalSample(None, study_name=study_code)
            created = api_instance.create_original_sample(samp)

            fetched = api_instance.download_original_samples_by_study(study_code)

            assert fetched.count == 1, "Study not found"

            assert created == fetched.original_samples[0], "create response != download response"

            ffetched = api_instance.download_original_samples(filter='studyId:' + study_code)

            assert ffetched.count == 1, "Study not found"

            assert ffetched == fetched

            api_instance.delete_original_sample(created.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)


    """
    """
    def test_os_study_lookup_paged(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:
            study_code = '1021-MD-UP'

            for i in range(5):
                samp = swagger_client.OriginalSample(None, study_name=study_code)
                created = api_instance.create_original_sample(samp)


            fetched1 = api_instance.download_original_samples_by_study(study_code, start=0, count=2)

            assert len(fetched1.original_samples) ==2, "Wrong number of original_samples returned"
            assert fetched1.count == 5, "Wrong total of original_samples returned"

            ffetched = api_instance.download_original_samples(filter='studyId:' + study_code,
                                                             start=0, count=2)

            assert ffetched == fetched1

            fetched2 = api_instance.download_original_samples_by_study(study_code, start=2, count=5)

            #Gets second tranche and also attempts to retrieve more than exist
            assert len(fetched2.original_samples) ==3, "Wrong number of original_samples returned"
            assert fetched2.count == 5, "Wrong total of original_samples returned"

            ids = []
            for original_sample in fetched1.original_samples + fetched2.original_samples:
                assert not original_sample.original_sample_id in ids, "OriginalSample returned twice"
                ids.append(original_sample.original_sample_id)

            #Check that it's the correct number of *unique* events

            #Clean up
            fetch_all = api_instance.download_original_samples_by_study(study_code)

            for original_sample in fetch_all.original_samples:
                api_instance.delete_original_sample(original_sample.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)



    """
    """
    def test_os_get_attrs(self, api_factory):

        metadata_api_instance = api_factory.MetadataApi()
        api_instance = api_factory.OriginalSampleApi()

        try:
            samp = swagger_client.OriginalSample(None, study_name='1023-MD-UP')
            samp.attrs = [
                swagger_client.Attr (attr_type='oxford', attr_value='12345678',
                                           attr_source='upd')
            ]
            created = api_instance.create_original_sample(samp)
            idents = metadata_api_instance.get_attr_types()

            assert 'oxford' in idents

            api_instance.delete_original_sample(created.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    Used to test permissions on get_attr_types
    """
    def test_os_get_attr_types(self, api_factory):

        metadata_api_instance = api_factory.MetadataApi()

        try:
            idents = metadata_api_instance.get_attr_types()

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)



    """
    """
    def test_os_download_original_sample_permission(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:
            if not api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=403):
                    api_instance.download_original_sample(str(uuid.uuid4()))
        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->download_original_sample", error)

    """
    """
    def test_os_download_original_sample_by_attr_permission(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:
            if not api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=403):
                    api_instance.download_original_samples_by_attr('partner_id','404')
        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->download_original_samples_by_attr", error)

