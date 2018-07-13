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

            samp = swagger_client.OriginalSample(None, study_name='4000-MD-UP')
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

            samp = swagger_client.OriginalSample(None, study_name='4001-MD-UP')
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

            samp = swagger_client.OriginalSample(None, study_name='4002-MD-UP')
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

            samp = swagger_client.OriginalSample(None, study_name='4003-MD-UP')
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

            samp = swagger_client.OriginalSample(None, study_name='4029-MD-UP')
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

            samp = swagger_client.OriginalSample(None, study_name='4004-MD-UP')
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

            samp = swagger_client.OriginalSample(None, study_name='4022-MD-UP')
            samp.attrs = [
                swagger_client.Attr (attr_type='partner_id', attr_value='123456')
            ]
            created = api_instance.create_original_sample(samp)
            looked_up = api_instance.download_original_samples_by_attr('partner_id', '123456',
                                                                            study_name='4022')
            assert looked_up.count == 1


            with pytest.raises(ApiException, status=404):
                looked_up = api_instance.download_original_samples_by_attr('oxford', '123456',
                                                                            study_name='9999')

            created1 = api_instance.create_original_sample(samp)

            looked_up = api_instance.download_original_samples_by_attr('partner_id', '123456',
                                                                            study_name='4022')
            assert looked_up.count == 2

            ffetched = api_instance.download_original_samples(filter='attr:partner_id:123456:4022')

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
            samp1 = swagger_client.OriginalSample(None, study_name='4022-MD-UP')
            samp1.attrs = [
                ident1
            ]
            created1 = api_instance.create_original_sample(samp1)

            samp2 = swagger_client.OriginalSample(None, study_name='4022-MD-UP')
            samp2.attrs = [
                ident2
            ]
            created2 = api_instance.create_original_sample(samp2)


            samp3 = swagger_client.OriginalSample(None, study_name='4022-MD-UP')
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

            samp = swagger_client.OriginalSample(None, study_name='4005-MD-UP',)
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

            samp = swagger_client.OriginalSample(None, study_name='4006-MD-UP')
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

            new_samp = swagger_client.OriginalSample(None, study_name='4007-MD-UP')
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
            samp = swagger_client.OriginalSample(None, study_name='4008-MD-UP')
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
            study_code = '4020-MD-UP'

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
            study_code = '4021-MD-UP'

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
            samp = swagger_client.OriginalSample(None, study_name='4023-MD-UP')
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


    """
    """
    def test_os_location_lookup_missing(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        try:

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    api_instance.download_original_samples_by_location(str(uuid.uuid4()))
            else:
                with pytest.raises(ApiException, status=403):
                    api_instance.download_original_samples_by_location(str(uuid.uuid4()))

        except ApiException as error:
            self.check_api_exception(api_factory,
                                     "OriginalSampleApi->download_original_samples_by_location", error)


    """
    """
    def test_os_location_lookup(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        se_api_instance = api_factory.SamplingEventApi()
        location_api_instance = api_factory.LocationApi()

        try:

            sampling_event = swagger_client.SamplingEvent(None, '4024-MD-UP', date(2017, 10, 10),
                                                doc_accuracy='month')
            loc = swagger_client.Location(None, 27.463, 90.495, 'city',
                                          'Trongsa, Trongsa, Bhutan', 'test_create_with_locations', 'BTN')
            loc = location_api_instance.create_location(loc)

            sampling_event.location_id = loc.location_id
            created_se = se_api_instance.create_sampling_event(sampling_event)

            samp = swagger_client.OriginalSample(None, study_name='4024-MD-UP')
            samp.sampling_event_id = created_se.sampling_event_id

            samp.attrs = [
                swagger_client.Attr (attr_type='oxford', attr_value='12345678',
                                           attr_source='upd')
            ]
            created = api_instance.create_original_sample(samp)

            results = api_instance.download_original_samples_by_location(loc.location_id)
            looked_up = results.original_samples[0]

            fetched = api_instance.download_original_sample(looked_up.original_sample_id)

            assert created == fetched, "create response != download response"

            assert results.attr_types == ['oxford']

            ffetched = api_instance.download_original_samples(filter='location:'+loc.location_id)

            assert ffetched == results

            fetched.original_sample_id = None
            assert samp == fetched, "upload != download response"

            se_api_instance.delete_sampling_event(created_se.sampling_event_id)

            api_instance.delete_original_sample(created.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_location_lookup_paged(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        se_api_instance = api_factory.SamplingEventApi()
        location_api_instance = api_factory.LocationApi()

        try:

            sampling_event = swagger_client.SamplingEvent(None, '4025-MD-UP', date(2017, 10, 10),
                                                doc_accuracy='month')
            loc = swagger_client.Location(None, 27.463, 90.495, 'city',
                                          'Trongsa, Trongsa, Bhutan', 'test_create_with_locations', 'BTN')
            loc = location_api_instance.create_location(loc)

            sampling_event.location_id = loc.location_id
            created_se = se_api_instance.create_sampling_event(sampling_event)

            samp1 = swagger_client.OriginalSample(None, study_name='4025-MD-UP')
            samp1.sampling_event_id = created_se.sampling_event_id

            created1 = api_instance.create_original_sample(samp1)

            samp2 = swagger_client.OriginalSample(None, study_name='4025-MD-UP')
            samp2.sampling_event_id = created_se.sampling_event_id

            created2 = api_instance.create_original_sample(samp2)

            results = api_instance.download_original_samples_by_location(loc.location_id,
                                                                         start=0,
                                                                         count=1)

            assert results.count == 2
            assert len(results.original_samples) == 1

            looked_up = results.original_samples[0]

            fetched = api_instance.download_original_sample(looked_up.original_sample_id)

            assert created1 == fetched or created2 == fetched, "create response != download response"

            ffetched = api_instance.download_original_samples(filter='location:'+loc.location_id,
                                                              start=0,
                                                              count=1)

            assert ffetched == results

            fetched.original_sample_id = None
            assert samp1 == fetched, "upload != download response"

            se_api_instance.delete_sampling_event(created_se.sampling_event_id)
            api_instance.delete_original_sample(created1.original_sample_id)
            api_instance.delete_original_sample(created2.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_taxa_lookup_missing(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        try:

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    api_instance.download_original_samples_by_taxa(12345)
            else:
                with pytest.raises(ApiException, status=403):
                    api_instance.download_original_samples_by_taxa(12345)

        except ApiException as error:
            self.check_api_exception(api_factory,
                                     "OriginalSampleApi->download_original_samples_by_taxa", error)


    """
    """
    def test_os_taxa_lookup(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        se_api_instance = api_factory.SamplingEventApi()
        study_api = api_factory.StudyApi()

        try:

            sampling_event = swagger_client.SamplingEvent(None, '4025-MD-UP', date(2017, 10, 10),
                                                partner_species='PF')
            created_se = se_api_instance.create_sampling_event(sampling_event)
            study_detail = study_api.download_study('4025')
            study_detail.partner_species[0].taxa = [ swagger_client.Taxonomy(taxonomy_id=5833) ]
            study_api.update_study('4025', study_detail)


            samp = swagger_client.OriginalSample(None, study_name='4025-MD-UP')
            samp.sampling_event_id = created_se.sampling_event_id

            samp.attrs = [
                swagger_client.Attr (attr_type='oxford', attr_value='12345-T',
                                           attr_source='upd')
            ]
            created = api_instance.create_original_sample(samp)

            results = api_instance.download_original_samples_by_taxa(5833)
            looked_up = results.original_samples[0]

            fetched = api_instance.download_original_sample(looked_up.original_sample_id)

            assert created == fetched, "create response != download response"

            assert results.attr_types == ['oxford']

            ffetched = api_instance.download_original_samples(filter='taxa:5833')

            assert ffetched == results

            fetched.original_sample_id = None
            assert samp == fetched, "upload != download response"

            for original_sample in results.original_samples:
                se_api_instance.delete_sampling_event(original_sample.sampling_event_id)
                api_instance.delete_original_sample(original_sample.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_taxa_lookup_paged(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        se_api_instance = api_factory.SamplingEventApi()
        study_api = api_factory.StudyApi()

        try:

            study_codes = [ '4031-MD-UP', '4032-MD-UP', '4033-MD-UP', '4034-MD-UP', '4034-MD-UP']

            for study_code in study_codes:
                samp = swagger_client.SamplingEvent(None, study_code, date(2017, 10, 14),
                                                    partner_species='PF')
                created = se_api_instance.create_sampling_event(samp)
                study_detail = study_api.download_study(study_code)
                study_detail.partner_species[0].taxa = [ swagger_client.Taxonomy(taxonomy_id=5833) ]
                study_api.update_study(study_code, study_detail)
                samp1 = swagger_client.OriginalSample(None, study_name=study_code)
                samp1.sampling_event_id = created.sampling_event_id
                created1 = api_instance.create_original_sample(samp1)

            results = api_instance.download_original_samples_by_taxa(5833,
                                                                         start=0,
                                                                         count=2)

            assert results.count == 5
            assert len(results.original_samples) == 2

            looked_up = results.original_samples[0]

            fetched = api_instance.download_original_sample(looked_up.original_sample_id)

            ffetched = api_instance.download_original_samples(filter='taxa:5833',
                                                              start=0,
                                                              count=2)

            assert ffetched == results

            #Clean up
            fetch_all = api_instance.download_original_samples_by_taxa(5833)

            for original_sample in fetch_all.original_samples:
                se_api_instance.delete_sampling_event(original_sample.sampling_event_id)
                api_instance.delete_original_sample(original_sample.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)
