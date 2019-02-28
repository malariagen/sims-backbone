import openapi_client
from openapi_client.rest import ApiException

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

            samp = openapi_client.OriginalSample(None, study_name='4000-MD-UP')
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
    def test_os_taxa_on_create(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        study_api = api_factory.StudyApi()

        try:

            study_code = '4000-MD-UP'
            samp = openapi_client.OriginalSample(None, study_name=study_code,
                                                 partner_species='PF')
            created = api_instance.create_original_sample(samp)
            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to create_original_sample succeeded')

            study_detail = study_api.download_study(study_code)
            study_detail.partner_species[0].taxa = [ openapi_client.Taxonomy(taxonomy_id=5833) ]
            study_api.update_study(study_code, study_detail)

            created2 = api_instance.create_original_sample(samp)

            assert not created2.partner_taxonomies is None, 'Taxonomies missing'
            assert int(created2.partner_taxonomies[0].taxonomy_id) == 5833, 'Wrong Taxonomy'
            api_instance.delete_original_sample(created.original_sample_id)
            api_instance.delete_original_sample(created2.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)


    """
    """
    def test_os_delete(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp = openapi_client.OriginalSample(None, study_name='4001-MD-UP')
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

            samp = openapi_client.OriginalSample(None, study_name='4002-MD-UP')
            samp.attrs = [
                openapi_client.Attr (attr_type='oxford', attr_value='1234',
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

            samp = openapi_client.OriginalSample(None, study_name='4003-MD-UP')
            samp.attrs = [
                openapi_client.Attr (attr_type='partner_id', attr_value='12345')
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

            samp = openapi_client.OriginalSample(None, study_name='4029-MD-UP')
            samp.attrs = [
                openapi_client.Attr (attr_type='individual_id', attr_value='12345')
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

            samp = openapi_client.OriginalSample(None, study_name='4004-MD-UP')
            samp.attrs = [
                openapi_client.Attr (attr_type='oxford', attr_value='123456')
            ]
            created = api_instance.create_original_sample(samp)
            results = api_instance.download_original_samples_by_attr('oxford', '123456')
            looked_up = results.original_samples[0]

            fetched = api_instance.download_original_sample(looked_up.original_sample_id)

            assert created == fetched, "create response != download response"

            ffetched = api_instance.download_original_samples(search_filter='attr:oxford:123456')

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
        se_api_instance = api_factory.SamplingEventApi()

        try:

            sampling_event = openapi_client.SamplingEvent(None, date(2017, 10, 10),
                                                          doc_accuracy='month')

            created_se = se_api_instance.create_sampling_event(sampling_event)
            samp = openapi_client.OriginalSample(None, study_name='4022-MD-UP')
            samp.attrs = [
                openapi_client.Attr (attr_type='partner_id', attr_value='123456')
            ]
            samp.sampling_event_id = created_se.sampling_event_id

            created = api_instance.create_original_sample(samp)
            looked_up = api_instance.download_original_samples_by_attr('partner_id', '123456',
                                                                       study_name='4022')
            assert looked_up.count == 1


            looked_up = api_instance.download_original_samples_by_attr('oxford', '123456',
                                                                       study_name='9999')

            assert not looked_up.original_samples
            assert looked_up.count == 0

            created1 = api_instance.create_original_sample(samp)

            looked_up = api_instance.download_original_samples_by_attr('partner_id', '123456',
                                                                       study_name='4022')
            assert looked_up.count == 2

            ffetched = api_instance.download_original_samples(search_filter='attr:partner_id:123456:4022')

            assert ffetched == looked_up

            api_instance.delete_original_sample(created.original_sample_id)
            api_instance.delete_original_sample(created1.original_sample_id)
            se_api_instance.delete_sampling_event(created_se.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_attr_merge(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            ident1 = openapi_client.Attr(attr_type='oxford_id', attr_value='1234')
            ident2 = openapi_client.Attr(attr_type='roma_id', attr_value='12345')
            ident3 = openapi_client.Attr(attr_type='lims_id', attr_value='123456')
            samp1 = openapi_client.OriginalSample(None, study_name='4022-MD-UP')
            samp1.attrs = [
                ident1
            ]
            created1 = api_instance.create_original_sample(samp1)

            samp2 = openapi_client.OriginalSample(None, study_name='4022-MD-UP')
            samp2.attrs = [
                ident2
            ]
            created2 = api_instance.create_original_sample(samp2)


            samp3 = openapi_client.OriginalSample(None, study_name='4022-MD-UP')
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

            samp = openapi_client.OriginalSample(None, study_name='4005-MD-UP',)
            samp.attrs = [
                openapi_client.Attr (attr_type='oxford', attr_value='1234567')
            ]
            created = api_instance.create_original_sample(samp)
            looked_up = api_instance.download_original_samples_by_attr('oxford', '1234567')
            looked_up = looked_up.original_samples[0]
            new_samp = openapi_client.OriginalSample(None, study_name='0001-MD-UP')
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

            samp = openapi_client.OriginalSample(None, study_name='4006-MD-UP')
            samp.attrs = [
                openapi_client.Attr (attr_type='oxford', attr_value='12345678',
                                     attr_source='upd')
            ]
            created = api_instance.create_original_sample(samp)
            looked_up = api_instance.download_original_samples_by_attr('oxford', '12345678')
            looked_up = looked_up.original_samples[0]
            new_samp = openapi_client.OriginalSample(None, study_name='0001-MD-UP')
            new_samp.attrs = [
                openapi_client.Attr (attr_type='oxford', attr_value='123456789',
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

            new_samp = openapi_client.OriginalSample(None, study_name='4007-MD-UP')
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
            samp = openapi_client.OriginalSample(None, study_name='4008-MD-UP')
            samp.attrs = [
                openapi_client.Attr (attr_type='partner_id', attr_value=test_id,
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

            ffetched = api_instance.download_original_samples(search_filter=urllib.parse.quote_plus('attr:partner_id:' + test_id))

            assert ffetched == results

            api_instance.delete_original_sample(created.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_study_lookup(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        se_api_instance = api_factory.SamplingEventApi()

        try:
            study_code = '4020-MD-UP'

            sampling_event = openapi_client.SamplingEvent(None, date(2017, 10, 10),
                                                          doc_accuracy='month')

            created_se = se_api_instance.create_sampling_event(sampling_event)

            samp = openapi_client.OriginalSample(None, study_name=study_code)
            samp.sampling_event_id = created_se.sampling_event_id

            samp.attrs = [
                openapi_client.Attr (attr_type='partner_id',
                                     attr_value='os_study_lookup',
                                     attr_source='encode')
            ]
            created = api_instance.create_original_sample(samp)

            fetched = api_instance.download_original_samples_by_study(study_code)

            assert fetched.count == 1, "Study not found"

            assert created == fetched.original_samples[0], "create response != download response"

            assert fetched.original_samples[0].sampling_event_id in fetched.sampling_events

            assert fetched.attr_types == [ samp.attrs[0].attr_type ]

            ffetched = api_instance.download_original_samples(search_filter='studyId:' + study_code)

            assert ffetched.count == 1, "Study not found"

            assert ffetched == fetched

            api_instance.delete_original_sample(created.original_sample_id)
            se_api_instance.delete_sampling_event(created_se.sampling_event_id)

            with pytest.raises(ApiException, status=404):
                fetched = api_instance.download_original_samples_by_study('asdfhjik')
        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_study_lookup_with_taxa(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        study_api = api_factory.StudyApi()

        try:
            study_code = '4036-MD-UP-A'

            samp = openapi_client.OriginalSample(None, study_name=study_code,
                                                partner_species='PF')
            created = api_instance.create_original_sample(samp)

            study_detail = study_api.download_study(study_code)
            study_detail.partner_species[0].taxa = [ openapi_client.Taxonomy(taxonomy_id=5833) ]
            study_api.update_study(study_code, study_detail)

            fetched = api_instance.download_original_samples_by_study(study_code)

            assert fetched.count == 1, "Study not found"

            ffetched = api_instance.download_original_samples(search_filter='studyId:' + study_code)

            assert ffetched.count == 1, "Study not found"

            assert ffetched == fetched

            fetched.original_samples[0].partner_taxonomies = None

            assert created == fetched.original_samples[0], "create response != download response"

            api_instance.delete_original_sample(created.original_sample_id)

            with pytest.raises(ApiException, status=404):
                fetched = api_instance.download_original_samples_by_study('asdfhjik')
        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)


    """
    """
    def test_os_study_lookup_paged(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:
            study_code = '4021-MD-UP'

            for i in range(5):
                samp = openapi_client.OriginalSample(None, study_name=study_code)
                created = api_instance.create_original_sample(samp)


            fetched1 = api_instance.download_original_samples_by_study(study_code, start=0, count=2)

            assert len(fetched1.original_samples) ==2, "Wrong number of original_samples returned"
            assert fetched1.count == 5, "Wrong total of original_samples returned"

            ffetched = api_instance.download_original_samples(search_filter='studyId:' + study_code,
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
            samp = openapi_client.OriginalSample(None, study_name='4023-MD-UP')
            samp.attrs = [
                openapi_client.Attr (attr_type='oxford', attr_value='12345678',
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

            sampling_event = openapi_client.SamplingEvent(None, date(2017, 10, 10),
                                                          doc_accuracy='month')
            loc = openapi_client.Location(None, 27.463, 90.495, 'city',
                                          'Trongsa, Trongsa, Bhutan', 'test_create_with_locations', 'BTN')
            loc = location_api_instance.create_location(loc)

            sampling_event.location_id = loc.location_id
            created_se = se_api_instance.create_sampling_event(sampling_event)

            samp = openapi_client.OriginalSample(None, study_name='4024-MD-UP')
            samp.sampling_event_id = created_se.sampling_event_id

            samp.attrs = [
                openapi_client.Attr (attr_type='oxford', attr_value='12345678',
                                     attr_source='upd')
            ]
            created = api_instance.create_original_sample(samp)

            results = api_instance.download_original_samples_by_location(loc.location_id)
            looked_up = results.original_samples[0]

            assert looked_up.sampling_event_id in results.sampling_events

            fetched = api_instance.download_original_sample(looked_up.original_sample_id)

            assert created == fetched, "create response != download response"

            assert results.attr_types == ['oxford']

            ffetched = api_instance.download_original_samples(search_filter='location:'+loc.location_id)

            assert ffetched == results

            fetched.original_sample_id = None
            assert samp == fetched, "upload != download response"

            se_api_instance.delete_sampling_event(created_se.sampling_event_id)

            location_api_instance.delete_location(loc.location_id)

            api_instance.delete_original_sample(created.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)


    """
    """
    def test_os_event_set_lookup(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        se_api_instance = api_factory.SamplingEventApi()
        es_api_instance = api_factory.EventSetApi()

        try:

            event_set_name = 'test_os_event_set_lookup'

            created_es = es_api_instance.create_event_set(event_set_name)

            sampling_event = openapi_client.SamplingEvent(None, date(2017, 10, 10),
                                                          doc_accuracy='month')

            created_se = se_api_instance.create_sampling_event(sampling_event)

            created_set = es_api_instance.create_event_set_item(event_set_name, created_se.sampling_event_id)

            samp = openapi_client.OriginalSample(None, study_name='4024-MD-UP')
            samp.sampling_event_id = created_se.sampling_event_id

            samp.attrs = [
                openapi_client.Attr (attr_type='oxford', attr_value='12345678',
                                     attr_source='upd')
            ]
            created = api_instance.create_original_sample(samp)

            results = api_instance.download_original_samples_by_event_set(event_set_name)
            looked_up = results.original_samples[0]

            assert looked_up.sampling_event_id in results.sampling_events
            fetched = api_instance.download_original_sample(looked_up.original_sample_id)

            assert created == fetched, "create response != download response"

            assert results.attr_types == ['oxford']

            se_api_instance.delete_sampling_event(created_se.sampling_event_id)

            es_api_instance.delete_event_set(event_set_name)

            api_instance.delete_original_sample(created.original_sample_id)

            with pytest.raises(ApiException, status=404):
                results = api_instance.download_original_samples_by_event_set(event_set_name)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_location_lookup_paged(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        se_api_instance = api_factory.SamplingEventApi()
        location_api_instance = api_factory.LocationApi()

        try:

            sampling_event = openapi_client.SamplingEvent(None, date(2017, 10, 10),
                                                          doc_accuracy='month')
            loc = openapi_client.Location(None, 27.463, 90.495, 'city',
                                          'Trongsa, Trongsa, Bhutan', 'test_create_with_locations', 'BTN')
            loc = location_api_instance.create_location(loc)

            sampling_event.location_id = loc.location_id
            created_se = se_api_instance.create_sampling_event(sampling_event)

            samp1 = openapi_client.OriginalSample(None, study_name='4025-MD-UP')
            samp1.sampling_event_id = created_se.sampling_event_id

            created1 = api_instance.create_original_sample(samp1)

            samp2 = openapi_client.OriginalSample(None, study_name='4025-MD-UP')
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

            ffetched = api_instance.download_original_samples(search_filter='location:'+loc.location_id,
                                                              start=0,
                                                              count=1)

            assert ffetched == results

            fetched.original_sample_id = None
            assert samp1 == fetched, "upload != download response"

            se_api_instance.delete_sampling_event(created_se.sampling_event_id)
            location_api_instance.delete_location(loc.location_id)
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

            sampling_event = openapi_client.SamplingEvent(None, date(2017, 10, 10),
                                                          doc_accuracy='month')

            created_se = se_api_instance.create_sampling_event(sampling_event)
            samp = openapi_client.OriginalSample(None, study_name='4025-MD-UP',
                                                 partner_species='PF')
            samp.sampling_event_id = created_se.sampling_event_id

            samp.attrs = [
                openapi_client.Attr (attr_type='oxford', attr_value='12345-T',
                                     attr_source='upd')
            ]
            created = api_instance.create_original_sample(samp)

            study_detail = study_api.download_study('4025')
            study_detail.partner_species[0].taxa = [ openapi_client.Taxonomy(taxonomy_id=5833) ]
            study_api.update_study('4025', study_detail)

            created.partner_taxonomies = study_detail.partner_species[0].taxa
            samp.partner_taxonomies = study_detail.partner_species[0].taxa
            results = api_instance.download_original_samples_by_taxa(5833)
            looked_up = results.original_samples[0]

            fetched = api_instance.download_original_sample(looked_up.original_sample_id)

            assert created == fetched, "create response != download response"

            assert results.attr_types == ['oxford']

            ffetched = api_instance.download_original_samples(search_filter='taxa:5833')

            assert ffetched == results

            fetched.original_sample_id = None

            assert samp == fetched, "upload != download response"

            for original_sample in results.original_samples:
                api_instance.delete_original_sample(original_sample.original_sample_id)
            se_api_instance.delete_sampling_event(created_se.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_taxa_lookup_paged(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        study_api = api_factory.StudyApi()

        try:

            study_codes = [ '4031-MD-UP', '4032-MD-UP', '4033-MD-UP', '4034-MD-UP', '4034-MD-UP']

            for study_code in study_codes:
                samp1 = openapi_client.OriginalSample(None,
                                                      study_name=study_code,
                                                      partner_species='PF')
                created1 = api_instance.create_original_sample(samp1)
                study_detail = study_api.download_study(study_code)
                study_detail.partner_species[0].taxa = [ openapi_client.Taxonomy(taxonomy_id=5833) ]
                study_api.update_study(study_code, study_detail)

            results = api_instance.download_original_samples_by_taxa(5833,
                                                                     start=0,
                                                                     count=2)

            assert results.count == 5
            assert len(results.original_samples) == 2

            looked_up = results.original_samples[0]

            fetched = api_instance.download_original_sample(looked_up.original_sample_id)

            ffetched = api_instance.download_original_samples(search_filter='taxa:5833',
                                                              start=0,
                                                              count=2)

            assert ffetched == results

            #Clean up
            fetch_all = api_instance.download_original_samples_by_taxa(5833)

            for original_sample in fetch_all.original_samples:
                api_instance.delete_original_sample(original_sample.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def get_merge_samples(self):

        samp1 = openapi_client.OriginalSample(None, study_name='4035-MD-UP',
                                              days_in_culture=3)
        samp1.attrs = [
            openapi_client.Attr (attr_type='partner_id', attr_value='os1-12345678',
                                 attr_source='mrg')
        ]
        samp2 = openapi_client.OriginalSample(None, study_name='4035-MD-UP',
                                              days_in_culture=3)
        samp2.attrs = [
            openapi_client.Attr (attr_type='partner_id', attr_value='os2-12345678',
                                 attr_source='mrg')
        ]

        return samp1, samp2

    """
    """
    def test_os_merge(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp1, samp2 = self.get_merge_samples()

            created1 = api_instance.create_original_sample(samp1)
            created2 = api_instance.create_original_sample(samp2)

            merged = api_instance.merge_original_samples(created1.original_sample_id,
                                                         created2.original_sample_id)

            fetched = api_instance.download_original_sample(created1.original_sample_id)
            assert merged == fetched, "create response != download response"

            for attr in samp1.attrs:
                assert attr in fetched.attrs
                for attr in samp2.attrs:
                    assert attr in fetched.attrs

            api_instance.delete_original_sample(created1.original_sample_id)

            with pytest.raises(ApiException, status=404):
                api_instance.delete_original_sample(created2.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_merge_missing(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp1, samp2 = self.get_merge_samples()

            created1 = api_instance.create_original_sample(samp1)


            with pytest.raises(ApiException, status=404):
                merged = api_instance.merge_original_samples(created1.original_sample_id,
                                                             str(uuid.uuid4()))

            with pytest.raises(ApiException, status=404):
                merged = api_instance.merge_original_samples(str(uuid.uuid4()),
                                                             created1.original_sample_id)

            merged = api_instance.merge_original_samples(created1.original_sample_id,
                                                         created1.original_sample_id)

            assert merged == created1

            api_instance.delete_original_sample(created1.original_sample_id)


        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_merge_study1(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp1, samp2 = self.get_merge_samples()

            samp1.study_name = '0000 default'
            created1 = api_instance.create_original_sample(samp1)
            created2 = api_instance.create_original_sample(samp2)

            api_instance.delete_original_sample(created1.original_sample_id)


        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_merge_study1(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp1, samp2 = self.get_merge_samples()

            samp1.study_name = '0000 default'
            created1 = api_instance.create_original_sample(samp1)
            created2 = api_instance.create_original_sample(samp2)

            merged = api_instance.merge_original_samples(created1.original_sample_id,
                                                         created2.original_sample_id)

            fetched = api_instance.download_original_sample(created1.original_sample_id)
            assert merged == fetched, "create response != download response"

            assert fetched.study_name == samp2.study_name

            for attr in samp1.attrs:
                assert attr in fetched.attrs
                for attr in samp2.attrs:
                    assert attr in fetched.attrs

            api_instance.delete_original_sample(created1.original_sample_id)

            with pytest.raises(ApiException, status=404):
                api_instance.delete_original_sample(created2.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_merge_study2(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp1, samp2 = self.get_merge_samples()

            samp2.study_name = '0000 default'
            created1 = api_instance.create_original_sample(samp1)
            created2 = api_instance.create_original_sample(samp2)

            merged = api_instance.merge_original_samples(created1.original_sample_id,
                                                         created2.original_sample_id)

            fetched = api_instance.download_original_sample(created1.original_sample_id)
            assert merged == fetched, "create response != download response"

            assert fetched.study_name == samp1.study_name

            for attr in samp1.attrs:
                assert attr in fetched.attrs
                for attr in samp2.attrs:
                    assert attr in fetched.attrs

            api_instance.delete_original_sample(created1.original_sample_id)

            with pytest.raises(ApiException, status=404):
                api_instance.delete_original_sample(created2.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_merge_study3(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp1, samp2 = self.get_merge_samples()

            samp1.study_name = None
            created1 = api_instance.create_original_sample(samp1)
            created2 = api_instance.create_original_sample(samp2)

            merged = api_instance.merge_original_samples(created1.original_sample_id,
                                                         created2.original_sample_id)

            fetched = api_instance.download_original_sample(created1.original_sample_id)
            assert merged == fetched, "create response != download response"

            assert fetched.study_name == samp2.study_name

            for attr in samp1.attrs:
                assert attr in fetched.attrs
                for attr in samp2.attrs:
                    assert attr in fetched.attrs

            api_instance.delete_original_sample(created1.original_sample_id)

            with pytest.raises(ApiException, status=404):
                api_instance.delete_original_sample(created2.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_merge_study4(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp1, samp2 = self.get_merge_samples()

            samp2.study_name = None
            created1 = api_instance.create_original_sample(samp1)
            created2 = api_instance.create_original_sample(samp2)

            merged = api_instance.merge_original_samples(created1.original_sample_id,
                                                         created2.original_sample_id)

            fetched = api_instance.download_original_sample(created1.original_sample_id)
            assert merged == fetched, "create response != download response"

            assert fetched.study_name == samp1.study_name

            for attr in samp1.attrs:
                assert attr in fetched.attrs
                for attr in samp2.attrs:
                    assert attr in fetched.attrs

            api_instance.delete_original_sample(created1.original_sample_id)

            with pytest.raises(ApiException, status=404):
                api_instance.delete_original_sample(created2.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_merge_study5(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp1, samp2 = self.get_merge_samples()

            samp2.study_name = '4036-MD-UP'
            created1 = api_instance.create_original_sample(samp1)
            created2 = api_instance.create_original_sample(samp2)

            with pytest.raises(ApiException, status=404):
                merged = api_instance.merge_original_samples(created1.original_sample_id,
                                                             created2.original_sample_id)

            api_instance.delete_original_sample(created1.original_sample_id)
            api_instance.delete_original_sample(created2.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_merge_days_in_culture1(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp1, samp2 = self.get_merge_samples()

            samp1.days_in_culture = None
            created1 = api_instance.create_original_sample(samp1)
            created2 = api_instance.create_original_sample(samp2)

            merged = api_instance.merge_original_samples(created1.original_sample_id,
                                                         created2.original_sample_id)

            fetched = api_instance.download_original_sample(created1.original_sample_id)
            assert merged == fetched, "create response != download response"

            assert fetched.days_in_culture == samp2.days_in_culture

            for attr in samp1.attrs:
                assert attr in fetched.attrs
                for attr in samp2.attrs:
                    assert attr in fetched.attrs

            api_instance.delete_original_sample(created1.original_sample_id)

            with pytest.raises(ApiException, status=404):
                api_instance.delete_original_sample(created2.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_merge_days_in_culture2(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp1, samp2 = self.get_merge_samples()

            samp2.days_in_culture = None
            created1 = api_instance.create_original_sample(samp1)
            created2 = api_instance.create_original_sample(samp2)

            merged = api_instance.merge_original_samples(created1.original_sample_id,
                                                         created2.original_sample_id)

            fetched = api_instance.download_original_sample(created1.original_sample_id)
            assert merged == fetched, "create response != download response"

            assert fetched.days_in_culture == samp1.days_in_culture

            for attr in samp1.attrs:
                assert attr in fetched.attrs
                for attr in samp2.attrs:
                    assert attr in fetched.attrs

            api_instance.delete_original_sample(created1.original_sample_id)

            with pytest.raises(ApiException, status=404):
                api_instance.delete_original_sample(created2.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)


    """
    """
    def test_os_merge_days_in_culture3(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp1, samp2 = self.get_merge_samples()

            samp2.days_in_culture = 2
            created1 = api_instance.create_original_sample(samp1)
            created2 = api_instance.create_original_sample(samp2)

            with pytest.raises(ApiException, status=404):
                merged = api_instance.merge_original_samples(created1.original_sample_id,
                                                             created2.original_sample_id)

            api_instance.delete_original_sample(created1.original_sample_id)
            api_instance.delete_original_sample(created2.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_merge_os_attr_dedup(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp1, samp2 = self.get_merge_samples()

            expected = len(samp1.attrs) + len(samp2.attrs)

            samp2.attrs.append(samp1.attrs[0])

            created1 = api_instance.create_original_sample(samp1)
            created2 = api_instance.create_original_sample(samp2)

            merged = api_instance.merge_original_samples(created1.original_sample_id,
                                                         created2.original_sample_id)

            fetched = api_instance.download_original_sample(created1.original_sample_id)

            for attr in samp1.attrs:
                assert attr in fetched.attrs
                for attr in samp2.attrs:
                    assert attr in fetched.attrs

            assert len(fetched.attrs) == expected

            api_instance.delete_original_sample(created1.original_sample_id)

            with pytest.raises(ApiException, status=404):
                fetched = api_instance.download_original_sample(created2.original_sample_id)
        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    def get_merge_events(self):

            #Uses partner_id because only partner_id and individual_id are allowed to
            #have the same value assigned to different sampling events
            samp1 = openapi_client.SamplingEvent(None, date(2017, 10, 16))
            samp1.attrs = [
                openapi_client.Attr (attr_type='partner_id', attr_value='mrg1-12345678',
                                     attr_source='mrg')
            ]
            samp1.doc_accuracy = 'day'
            samp2 = openapi_client.SamplingEvent(None, date(2017, 10, 16))
            samp2.attrs = [
                openapi_client.Attr (attr_type='partner_id', attr_value='mrg2-12345678',
                                     attr_source='mrg')
            ]
            samp2.doc_accuracy = 'day'

            return samp1, samp2

    """
    """
    def test_os_merge_sampling_events(self, api_factory):

        se_api_instance = api_factory.SamplingEventApi()
        api_instance = api_factory.OriginalSampleApi()
        ds_api_instance = api_factory.DerivativeSampleApi()

        try:

            evnt1, evnt2 = self.get_merge_events()

            se_created1 = se_api_instance.create_sampling_event(evnt1)
            se_created2 = se_api_instance.create_sampling_event(evnt2)

            samp1, samp2 = self.get_merge_samples()

            samp1.sampling_event_id = se_created1.sampling_event_id
            samp2.sampling_event_id = se_created2.sampling_event_id


            created1 = api_instance.create_original_sample(samp1)
            created2 = api_instance.create_original_sample(samp2)

            ds_samp1 = openapi_client.DerivativeSample(None)
            ds_samp2 = openapi_client.DerivativeSample(None)

            ds_samp1.attrs = [
                openapi_client.Attr (attr_type='test1', attr_value='test1',
                                     attr_source='ds_os_attr')
            ]
            ds_samp2.attrs = [
                openapi_client.Attr (attr_type='test2', attr_value='test2',
                                     attr_source='ds_os_attr')
            ]
            ds_samp1.original_sample_id = created1.original_sample_id
            ds_samp2.original_sample_id = created2.original_sample_id
            ds_created1 = ds_api_instance.create_derivative_sample(ds_samp1)
            ds_created2 = ds_api_instance.create_derivative_sample(ds_samp2)

            merged = api_instance.merge_original_samples(created1.original_sample_id,
                                                         created2.original_sample_id)

            fetched = api_instance.download_original_sample(created1.original_sample_id)
            assert merged == fetched, "create response != download response"

            for attr in samp1.attrs:
                assert attr in fetched.attrs
                for attr in samp2.attrs:
                    assert attr in fetched.attrs

            assert fetched.sampling_event_id == se_created1.sampling_event_id

            fetched = se_api_instance.download_sampling_event(se_created1.sampling_event_id)

            for attr in evnt1.attrs:
                assert attr in fetched.attrs
                for attr in evnt2.attrs:
                    assert attr in fetched.attrs

            ds1 = ds_api_instance.download_derivative_sample(ds_created1.derivative_sample_id)
            ds2 = ds_api_instance.download_derivative_sample(ds_created2.derivative_sample_id)

            assert ds1.original_sample_id == ds2.original_sample_id

            assert ds1.original_sample_id == created1.original_sample_id

            ds_api_instance.delete_derivative_sample(ds_created1.derivative_sample_id)
            ds_api_instance.delete_derivative_sample(ds_created2.derivative_sample_id)
            api_instance.delete_original_sample(created1.original_sample_id)
            se_api_instance.delete_sampling_event(se_created1.sampling_event_id)

            with pytest.raises(ApiException, status=404):
                api_instance.delete_original_sample(created2.original_sample_id)

            with pytest.raises(ApiException, status=404):
                se_api_instance.delete_sampling_event(se_created2.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->se_create_sampling_event", error)


    """
    """
    def test_os_merge_sampling_events_fail(self, api_factory):

        se_api_instance = api_factory.SamplingEventApi()
        api_instance = api_factory.OriginalSampleApi()

        try:

            evnt1, evnt2 = self.get_merge_events()

            evnt1.doc_accuracy = 'day'
            evnt2.doc_accuracy = 'month'
            se_created1 = se_api_instance.create_sampling_event(evnt1)
            se_created2 = se_api_instance.create_sampling_event(evnt2)

            samp1, samp2 = self.get_merge_samples()

            samp1.sampling_event_id = se_created1.sampling_event_id
            samp2.sampling_event_id = se_created2.sampling_event_id


            created1 = api_instance.create_original_sample(samp1)
            created2 = api_instance.create_original_sample(samp2)

            with pytest.raises(ApiException, status=422):
                merged = api_instance.merge_original_samples(created1.original_sample_id,
                                                             created2.original_sample_id)

            fetched = api_instance.download_original_sample(created1.original_sample_id)

            for attr in samp1.attrs:
                assert attr in fetched.attrs
                for attr in samp2.attrs:
                    assert attr not in fetched.attrs

            assert fetched.sampling_event_id == se_created1.sampling_event_id

            fetched = se_api_instance.download_sampling_event(se_created1.sampling_event_id)

            for attr in evnt1.attrs:
                assert attr in fetched.attrs
                for attr in evnt2.attrs:
                    assert attr not in fetched.attrs

            api_instance.delete_original_sample(created1.original_sample_id)
            se_api_instance.delete_sampling_event(se_created1.sampling_event_id)

            api_instance.delete_original_sample(created2.original_sample_id)
            se_api_instance.delete_sampling_event(se_created2.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->se_create_sampling_event", error)

    """
    """
    def test_os_filter_fail(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            with pytest.raises(ApiException, status=422):
                ffetched = api_instance.download_original_samples(search_filter='xxxxx')

            with pytest.raises(ApiException, status=422):
                ffetched = api_instance.download_original_samples(search_filter='xxxxx:xxxxx')

            with pytest.raises(ApiException, status=422):
                ffetched = api_instance.download_original_samples(search_filter='attr:oxford_id')

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->download_original_samples", error)

    """
    """
    def test_merge_os_partner_species1(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp1, samp2 = self.get_merge_samples()

            samp1.partner_species = 'PF'

            created1 = api_instance.create_original_sample(samp1)
            created2 = api_instance.create_original_sample(samp2)

            api_instance.merge_original_samples(created1.original_sample_id,
                                               created2.original_sample_id)

            fetched = api_instance.download_original_sample(created1.original_sample_id)

            for attr in samp1.attrs:
                assert attr in fetched.attrs
                for attr in samp2.attrs:
                    assert attr in fetched.attrs

            assert fetched.partner_species == samp1.partner_species

            api_instance.delete_original_sample(created1.original_sample_id)

            with pytest.raises(ApiException, status=404):
                fetched = api_instance.download_original_sample(created2.original_sample_id)
        except ApiException as error:
            self.check_api_exception(api_factory,
                                     "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_merge_os_partner_species2(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp1, samp2 = self.get_merge_samples()

            samp2.partner_species = 'PV'

            created1 = api_instance.create_original_sample(samp1)
            created2 = api_instance.create_original_sample(samp2)

            api_instance.merge_original_samples(created1.original_sample_id,
                                               created2.original_sample_id)

            fetched = api_instance.download_original_sample(created1.original_sample_id)

            for attr in samp1.attrs:
                assert attr in fetched.attrs
                for attr in samp2.attrs:
                    assert attr in fetched.attrs

            assert fetched.partner_species == samp2.partner_species

            api_instance.delete_original_sample(created1.original_sample_id)

            with pytest.raises(ApiException, status=404):
                fetched = api_instance.download_original_sample(created2.original_sample_id)
        except ApiException as error:
            self.check_api_exception(api_factory,
                                     "OriginalSampleApi->create_original_sample", error)



    """
    """
    def test_merge_os_partner_species_fail(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp1, samp2 = self.get_merge_samples()

            samp1.partner_species = 'PF'
            samp2.partner_species = 'PV'

            created1 = api_instance.create_original_sample(samp1)
            created2 = api_instance.create_original_sample(samp2)

            with pytest.raises(ApiException, status=422):
                api_instance.merge_original_samples(created1.original_sample_id,
                                                   created2.original_sample_id)

            fetched = api_instance.download_original_sample(created1.original_sample_id)

            assert fetched == created1

            api_instance.delete_original_sample(created1.original_sample_id)
            api_instance.delete_original_sample(created2.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory,
                                     "OriginalSampleApi->create_original_sample", error)


    """
    """
    def test_merge_os_partner_species_missing_fail(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()

        try:

            samp1, samp2 = self.get_merge_samples()

            created1 = api_instance.create_original_sample(samp1)

            merged = api_instance.merge_original_samples(created1.original_sample_id,
                                                        created1.original_sample_id)

            assert merged == created1

            with pytest.raises(ApiException, status=404):
                api_instance.merge_original_samples(str(uuid.uuid4()), str(uuid.uuid4()))

            api_instance.delete_original_sample(created1.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory,
                                     "OriginalSampleApi->create_original_sample", error)

    """
    """
    def test_os_update_study(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        se_api_instance = api_factory.SamplingEventApi()
        location_api_instance = api_factory.LocationApi()
        indiv_api_instance = api_factory.IndividualApi()

        try:

            old_study = '4037-MD-UP'
            new_study = '4038-MD-UP'

            sampling_event = openapi_client.SamplingEvent(None, date(2017, 10, 10),
                                                          doc_accuracy='month')
            loc = openapi_client.Location(None, 27.463, 90.495, 'city',
                                          'Trongsa, Trongsa, Bhutan',
                                          'test_os_update_study', 'BTN')
            loc.attrs = [
                openapi_client.Attr(attr_type='partner_name',
                                    attr_value='Trongsa',
                                    attr_source='upd_s',
                                    study_name=old_study)
            ]
            loc = location_api_instance.create_location(loc)
            sampling_event.location_id = loc.location_id
            indiv = openapi_client.Individual(None)
            indiv.attrs = [
                openapi_client.Attr(attr_type='individual_id',
                                    attr_value='patient0',
                                    attr_source='upd_s',
                                    study_name=old_study),
                openapi_client.Attr(attr_type='individual_id',
                                    attr_value='patient1',
                                    attr_source='upd_s',
                                    study_name=new_study)
            ]
            individual = indiv_api_instance.create_individual(indiv)
            sampling_event.individual_id = individual.individual_id

            created_se = se_api_instance.create_sampling_event(sampling_event)

            samp = openapi_client.OriginalSample(None, study_name=old_study)
            samp.sampling_event_id = created_se.sampling_event_id

            created = api_instance.create_original_sample(samp)
            looked_up = api_instance.download_original_sample(created.original_sample_id)
            looked_up.study_name = new_study
            updated = api_instance.update_original_sample(looked_up.original_sample_id, looked_up)
            fetched = api_instance.download_original_sample(looked_up.original_sample_id)

            fetched_se = se_api_instance.download_sampling_event(fetched.sampling_event_id)
            assert fetched_se.location.attrs[0].study_name == looked_up.study_name
            assert updated == fetched, "update response != download response"

            fetched_i = indiv_api_instance.download_individual(individual.individual_id)
            assert fetched_i.attrs[0].study_name == looked_up.study_name
            assert fetched_i.attrs[1].study_name == looked_up.study_name

            se_api_instance.delete_sampling_event(created_se.sampling_event_id)
            with pytest.raises(ApiException, status=404):
                indiv_api_instance.delete_individual(individual.individual_id)
            location_api_instance.delete_location(loc.location_id)
            api_instance.delete_original_sample(looked_up.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)
