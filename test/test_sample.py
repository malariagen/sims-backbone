import openapi_client
from openapi_client.rest import ApiException

from test_base import TestBase
from datetime import date
import urllib

import uuid
import pytest

class TestSample(TestBase):


    """
    """
    def test_create(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 10),
                                                doc_accuracy='month')
            created = api_instance.create_sampling_event(samp)
            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to create_sampling_event succeeded')

            fetched = api_instance.download_sampling_event(created.sampling_event_id)
            assert created == fetched, "create response != download response"
            fetched.sampling_event_id = None
            fetched.version = None
            assert samp == fetched, "upload != download response"
            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_create_acc_date(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 10),
                                                acc_date=date(2017, 10, 10),
                                                doc_accuracy='month')
            created = api_instance.create_sampling_event(samp)
            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to create_sampling_event succeeded')

            fetched = api_instance.download_sampling_event(created.sampling_event_id)
            assert created == fetched, "create response != download response"
            fetched.sampling_event_id = None
            fetched.version = None
            assert samp == fetched, "upload != download response"
            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_delete(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 11))
            created = api_instance.create_sampling_event(samp)
            api_instance.delete_sampling_event(created.sampling_event_id)
            with pytest.raises(ApiException, status=404):
                fetched = api_instance.download_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)


    """
    """
    def test_delete_missing(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    api_instance.delete_sampling_event(str(uuid.uuid4()))
            else:
                with pytest.raises(ApiException, status=403):
                    api_instance.delete_sampling_event(str(uuid.uuid4()))

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->delete_sampling_event", error)

    """
    """
    def test_duplicate_key(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 12))
            samp.attrs = [
                openapi_client.Attr (attr_type='oxford', attr_value='1234',
                                     attr_source='same')
            ]
            created = api_instance.create_sampling_event(samp)

            with pytest.raises(ApiException, status=422):
                created = api_instance.create_sampling_event(samp)

            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_duplicate_partner_key(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 13))
            samp.attrs = [
                openapi_client.Attr (attr_type='partner_id', attr_value='12345')
            ]
            created = api_instance.create_sampling_event(samp)

            created1 = api_instance.create_sampling_event(samp)


            api_instance.delete_sampling_event(created.sampling_event_id)
            api_instance.delete_sampling_event(created1.sampling_event_id)

            assert created.sampling_event_id != created1.sampling_event_id

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_duplicate_individual_id(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 13))
            samp.attrs = [
                openapi_client.Attr (attr_type='individual_id', attr_value='12345')
            ]
            created = api_instance.create_sampling_event(samp)

            created1 = api_instance.create_sampling_event(samp)


            api_instance.delete_sampling_event(created.sampling_event_id)
            api_instance.delete_sampling_event(created1.sampling_event_id)

            assert created.sampling_event_id != created1.sampling_event_id

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)


    """
    """
    def test_attr_lookup(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        os_api_instance = api_factory.OriginalSampleApi()

        try:

            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 14))
            samp.attrs = [
                openapi_client.Attr (attr_type='oxford', attr_value='123456')
            ]
            created = api_instance.create_sampling_event(samp)
            study_code = '1015-MD-UP'
            os_samp = openapi_client.OriginalSample(None, study_name=study_code,
                                                    partner_species='PF',
                                                    sampling_event_id=created.sampling_event_id)

            os_created = os_api_instance.create_original_sample(os_samp)
            results = api_instance.download_sampling_events_by_attr('oxford', '123456')
            looked_up = results.sampling_events[0]

            fetched = api_instance.download_sampling_event(looked_up.sampling_event_id)

            assert created == fetched, "create response != download response"

            ffetched = api_instance.download_sampling_events(search_filter='attr:oxford:123456')

            assert ffetched == results

            fetched.sampling_event_id = None
            fetched.version = None
            assert samp == fetched, "upload != download response"

            os_api_instance.delete_original_sample(os_created.original_sample_id)
            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_attr_lookup_by_study(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        os_api_instance = api_factory.OriginalSampleApi()

        try:

            study_code = '1022-MD-UP'
            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 14))
            samp.attrs = [
                openapi_client.Attr(attr_type='partner_id',
                                    attr_value='123456', study_name=study_code)
            ]
            created = api_instance.create_sampling_event(samp)
            os_samp = openapi_client.OriginalSample(None, study_name=study_code,
                                                    partner_species='PF',
                                                    sampling_event_id=created.sampling_event_id)

            os_created = os_api_instance.create_original_sample(os_samp)
            looked_up = api_instance.download_sampling_events_by_attr('partner_id', '123456',
                                                                      study_name=study_code)
            assert looked_up.count == 1


            looked_up = api_instance.download_sampling_events_by_attr('oxford', '123456',
                                                                      study_name='9999')

            assert not looked_up.sampling_events
            assert looked_up.count == 0

            created1 = api_instance.create_sampling_event(samp)
            os_samp1 = openapi_client.OriginalSample(None, study_name=study_code,
                                                     partner_species='PF',
                                                     sampling_event_id=created1.sampling_event_id)

            os_created1 = os_api_instance.create_original_sample(os_samp1)

            looked_up = api_instance.download_sampling_events_by_attr('partner_id', '123456',
                                                                      study_name=study_code)
            assert looked_up.count == 2

            ffetched = api_instance.download_sampling_events(search_filter='attr:partner_id:123456:' + study_code)

            assert ffetched == looked_up

            os_api_instance.delete_original_sample(os_created.original_sample_id)
            os_api_instance.delete_original_sample(os_created1.original_sample_id)
            api_instance.delete_sampling_event(created.sampling_event_id)
            api_instance.delete_sampling_event(created1.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_attr_merge(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            ident1 = openapi_client.Attr(attr_type='oxford_id', attr_value='1234')
            ident2 = openapi_client.Attr(attr_type='roma_id', attr_value='12345')
            ident3 = openapi_client.Attr(attr_type='lims_id', attr_value='123456')
            samp1 = openapi_client.SamplingEvent(None, doc=date(2017, 10, 14))
            samp1.attrs = [
                ident1
            ]
            created1 = api_instance.create_sampling_event(samp1)

            samp2 = openapi_client.SamplingEvent(None, doc=date(2017, 10, 14))
            samp2.attrs = [
                ident2
            ]
            created2 = api_instance.create_sampling_event(samp2)


            samp3 = openapi_client.SamplingEvent(None, doc=date(2017, 10, 14))
            samp3.attrs = [
                ident1,
                ident2,
                ident3
            ]
            with pytest.raises(ApiException, status=422):
                created3 = api_instance.create_sampling_event(samp3)

            api_instance.delete_sampling_event(created1.sampling_event_id)
            api_instance.delete_sampling_event(created2.sampling_event_id)


        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_update(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 15))
            samp.attrs = [
                openapi_client.Attr(attr_type='oxford', attr_value='1234567')
            ]
            created = api_instance.create_sampling_event(samp)
            looked_up = api_instance.download_sampling_events_by_attr('oxford', '1234567')
            looked_up = looked_up.sampling_events[0]
            new_samp = openapi_client.SamplingEvent(None, doc=date(2018, 11, 11))
            new_samp.sampling_event_id = looked_up.sampling_event_id
            new_samp.attrs = samp.attrs
            new_samp.version = looked_up.version
            updated = api_instance.update_sampling_event(looked_up.sampling_event_id, new_samp)
            fetched = api_instance.download_sampling_event(looked_up.sampling_event_id)
            assert updated == fetched, "update response != download response"
            new_samp.version = fetched.version
            assert new_samp == fetched, "update != download response"
            api_instance.delete_sampling_event(looked_up.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_update_acc_date(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 15))
            samp.attrs = [
                openapi_client.Attr(attr_type='oxford', attr_value='1234567')
            ]
            created = api_instance.create_sampling_event(samp)
            looked_up = api_instance.download_sampling_events_by_attr('oxford', '1234567')
            looked_up = looked_up.sampling_events[0]
            new_samp = openapi_client.SamplingEvent(None, doc=date(2018, 11, 11),
                                                    acc_date=date(2019, 11, 6))
            new_samp.sampling_event_id = looked_up.sampling_event_id
            new_samp.version = looked_up.version
            new_samp.attrs = samp.attrs
            updated = api_instance.update_sampling_event(looked_up.sampling_event_id, new_samp)
            fetched = api_instance.download_sampling_event(looked_up.sampling_event_id)
            assert updated == fetched, "update response != download response"
            new_samp.version = fetched.version
            assert new_samp == fetched, "update != download response"
            api_instance.delete_sampling_event(looked_up.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_update_duplicate(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 16))
            samp.attrs = [
                openapi_client.Attr (attr_type='oxford', attr_value='12345678',
                                     attr_source='upd')
            ]
            created = api_instance.create_sampling_event(samp)
            looked_up = api_instance.download_sampling_events_by_attr('oxford', '12345678')
            looked_up = looked_up.sampling_events[0]
            new_samp = openapi_client.SamplingEvent(None, doc=date(2018, 10, 10))
            new_samp.attrs = [
                openapi_client.Attr (attr_type='oxford', attr_value='123456789',
                                     attr_source='upd')
            ]
            new_created = api_instance.create_sampling_event(new_samp)
            with pytest.raises(ApiException, status=422):
                updated = api_instance.update_sampling_event(looked_up.sampling_event_id, new_samp)

            api_instance.delete_sampling_event(looked_up.sampling_event_id)
            api_instance.delete_sampling_event(new_created.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_update_missing(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            new_samp = openapi_client.SamplingEvent(None, doc=date(2018, 11, 17))
            fake_id = uuid.uuid4()
            new_samp.sampling_event_id = str(fake_id)


            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    updated = api_instance.update_sampling_event(new_samp.sampling_event_id, new_samp)
            else:
                with pytest.raises(ApiException, status=403):
                    updated = api_instance.update_sampling_event(new_samp.sampling_event_id, new_samp)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->update_sampling_event", error)

    """
    """
    def test_attr_lookup_encode(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        os_api_instance = api_factory.OriginalSampleApi()

        try:

            test_id = 'MDG/DK_0005'
            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 14))
            samp.attrs = [
                openapi_client.Attr (attr_type='partner_id', attr_value=test_id,
                                     attr_source='encode')
            ]
            created = api_instance.create_sampling_event(samp)

            fetched = api_instance.download_sampling_event(created.sampling_event_id)

            assert created == fetched, "create response != download response"
            fetched.sampling_event_id = None
            fetched.version = None
            assert samp == fetched, "upload != download response"

            results = api_instance.download_sampling_events_by_attr('partner_id',
                                                                    urllib.parse.quote_plus(test_id))
            looked_up = results.sampling_events[0]
            fetched = api_instance.download_sampling_event(looked_up.sampling_event_id)

            assert created == fetched, "create response != download response"
            fetched.sampling_event_id = None
            fetched.version = None
            assert samp == fetched, "upload != download response"

            ffetched = api_instance.download_sampling_events(search_filter=urllib.parse.quote_plus('attr:partner_id:' + test_id))

            assert ffetched == results

            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)


    """
    """
    def test_create_with_locations(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        location_api_instance = api_factory.LocationApi()
        os_api_instance = api_factory.OriginalSampleApi()

        try:
            study_code = '1010-MD-UP'



            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 10),
                                                doc_accuracy='month')
            loc = openapi_client.Location(None, latitude=27.463,
                                          longitude=90.495,
                                          accuracy='city',
                                          curated_name='Trongsa, Trongsa, Bhutan',
                                          notes='test_create_with_locations',
                                          country='BTN')
            ident = openapi_client.Attr(attr_type='partner_name', attr_value='Trongsa',
                                        study_name='1009-MD-UP')
            loc.attrs = [
                ident
            ]
            loc = location_api_instance.create_location(loc)

            samp.location_id = loc.location_id
            created = api_instance.create_sampling_event(samp)

            os_samp = openapi_client.OriginalSample(None, study_name=study_code,
                                                    partner_species='PF',
                                                    sampling_event_id=created.sampling_event_id)

            os_created = os_api_instance.create_original_sample(os_samp)

            fetched = api_instance.download_sampling_event(created.sampling_event_id)
            assert samp.location_id == fetched.location_id, "upload location != download response"
            assert samp.location_id == fetched.public_location_id, "upload public_location != proxy download response"

            proxy_loc = openapi_client.Location(None, latitude=27.4,
                                                longitude=90.4,
                                                accuracy='region',
                                                curated_name='Trongsa, Bhutan',
                                                notes='test_create_with_locations',
                                                country='BTN')
            proxy_loc = location_api_instance.create_location(proxy_loc)
            loc.proxy_location_id = proxy_loc.location_id
            location_api_instance.update_location(loc.location_id, loc)
            samp.proxy_location_id = proxy_loc.location_id
            samp.sampling_event_id = fetched.sampling_event_id
            samp.version = fetched.version
            fetched = api_instance.update_sampling_event(fetched.sampling_event_id, samp)
            assert samp.location_id == fetched.location_id, "upload location != download response"
            assert samp.proxy_location_id == fetched.proxy_location_id, "upload proxy_location != download response"
            assert samp.proxy_location_id == fetched.public_location_id, "upload public_location != proxy download response"

            looked_up = api_instance.download_sampling_events_by_location(loc.location_id)

            assert looked_up.count == 1

            looked_up = api_instance.download_sampling_events_by_location(proxy_loc.location_id)

            assert looked_up.count == 1

            os_api_instance.delete_original_sample(os_created.original_sample_id)
            api_instance.delete_sampling_event(created.sampling_event_id)

            location_api_instance.delete_location(loc.location_id)
            location_api_instance.delete_location(proxy_loc.location_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)

    """
    """
    def test_update_with_locations(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        location_api_instance = api_factory.LocationApi()
        os_api_instance = api_factory.OriginalSampleApi()

        try:
            study_code = '1010-MD-UP'



            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 10),
                                                doc_accuracy='month')
            loc = openapi_client.Location(None, latitude=27.463,
                                          longitude=90.495,
                                          accuracy='city',
                                          curated_name='Trongsa, Trongsa, Bhutan',
                                          notes='test_create_with_locations',
                                          country='BTN')
            ident = openapi_client.Attr(attr_type='partner_name', attr_value='Trongsa',
                                        study_name='1009-MD-UP')
            loc.attrs = [
                ident
            ]
            loc = location_api_instance.create_location(loc)

            samp.location_id = loc.location_id
            created = api_instance.create_sampling_event(samp)

            os_samp = openapi_client.OriginalSample(None, study_name=study_code,
                                                    partner_species='PF',
                                                    sampling_event_id=created.sampling_event_id)

            os_created = os_api_instance.create_original_sample(os_samp)

            fetched = api_instance.download_sampling_event(created.sampling_event_id)
            assert samp.location_id == fetched.location_id, "upload location != download response"
            assert samp.location_id == fetched.public_location_id, "upload public_location != proxy download response"

            proxy_loc = openapi_client.Location(None, latitude=27.4,
                                                longitude=90.4,
                                                accuracy='region',
                                                curated_name='Trongsa, Bhutan',
                                                notes='test_create_with_locations',
                                                country='BTN')
            proxy_loc = location_api_instance.create_location(proxy_loc)
            loc.proxy_location_id = proxy_loc.location_id
            location_api_instance.update_location(loc.location_id, loc)
            samp.proxy_location_id = proxy_loc.location_id
            samp.sampling_event_id = fetched.sampling_event_id
            samp.version = fetched.version
            fetched = api_instance.update_sampling_event(fetched.sampling_event_id, samp)
            assert samp.location_id == fetched.location_id, "upload location != download response"
            assert samp.proxy_location_id == fetched.proxy_location_id, "upload proxy_location != download response"
            assert samp.proxy_location_id == fetched.public_location_id, "upload public_location != proxy download response"

            looked_up = api_instance.download_sampling_events_by_location(loc.location_id)

            assert looked_up.count == 1

            looked_up = api_instance.download_sampling_events_by_location(proxy_loc.location_id)

            assert looked_up.count == 1

            new_loc = openapi_client.Location(None, latitude=28.463,
                                              longitude=91.495,
                                              accuracy='region',
                                              curated_name='Trongsa, Bhutan',
                                              notes='test_update_with_locations',
                                              country='BTN')
            new_loc = location_api_instance.create_location(new_loc)

            created.location_id = new_loc.location_id
            created.public_location_id = new_loc.location_id
            created.location = None
            created.version = fetched.version
            new_se = api_instance.update_sampling_event(created.sampling_event_id, created)

            new_se.location = None
            assert new_se.version == created.version + 1
            created.version = new_se.version
            assert new_se == created

            os_api_instance.delete_original_sample(os_created.original_sample_id)
            api_instance.delete_sampling_event(created.sampling_event_id)

            location_api_instance.delete_location(loc.location_id)
            location_api_instance.delete_location(proxy_loc.location_id)
            location_api_instance.delete_location(new_loc.location_id)


        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)

    """
    """
    def test_se_get_by_location_paged(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        location_api_instance = api_factory.LocationApi()
        os_api_instance = api_factory.OriginalSampleApi()

        study_code = '1009-MD_UP'
        try:

            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 10),
                                                doc_accuracy='month')
            samp.attrs = [
                openapi_client.Attr(attr_type='attr1',
                                    attr_value='attr1val'),
                openapi_client.Attr(attr_type='attr2',
                                    attr_value='attr2val'),
            ]
            samp1 = openapi_client.SamplingEvent(None, doc=date(2017, 11, 11),
                                                 doc_accuracy='month')
            samp2 = openapi_client.SamplingEvent(None, doc=date(2017, 12, 12),
                                                 doc_accuracy='month')
            loc = openapi_client.Location(None, latitude=27.463,
                                          longitude=90.495,
                                          accuracy='city',
                                          curated_name='Trongsa, Trongsa, Bhutan',
                                          notes='test_create_with_locations',
                                          country='BTN')
            loc1 = openapi_client.Location(None, latitude=27.4632,
                                           longitude=90.4952,
                                           accuracy='city',
                                           curated_name='Trongsa, Trongsa, Bhutan',
                                           notes='test_create_with_locations',
                                           country='BTN')
            ident = openapi_client.Attr(attr_type='partner_name', attr_value='Trongsa',
                                        study_name=study_code)
            loc.attrs = [
                ident
            ]
            loc = location_api_instance.create_location(loc)
            loc1.proxy_location_id = loc.location_id
            loc1 = location_api_instance.create_location(loc1)

            samp.location_id = loc.location_id
            created = api_instance.create_sampling_event(samp)
            samp1.location_id = loc.location_id
            created1 = api_instance.create_sampling_event(samp1)
            samp2.location_id = loc1.location_id
            samp2.proxy_location_id = loc.location_id
            created2 = api_instance.create_sampling_event(samp2)


            os_samp = openapi_client.OriginalSample(None, study_name=study_code,
                                                    partner_species='PF',
                                                    sampling_event_id=created.sampling_event_id)

            os_created = os_api_instance.create_original_sample(os_samp)

            os_samp1 = openapi_client.OriginalSample(None, study_name=study_code,
                                                     partner_species='PF',
                                                     sampling_event_id=created1.sampling_event_id)

            os_created1 = os_api_instance.create_original_sample(os_samp1)

            os_samp2 = openapi_client.OriginalSample(None, study_name=study_code,
                                                     partner_species='PF',
                                                     sampling_event_id=created2.sampling_event_id)

            os_created2 = os_api_instance.create_original_sample(os_samp2)

            looked_up = api_instance.download_sampling_events_by_location(loc.location_id)

            assert looked_up.count == 3

            event_ids = []
            for sampling_event in looked_up.sampling_events:
                event_ids.append(sampling_event.sampling_event_id)
            assert created.sampling_event_id in event_ids
            assert created1.sampling_event_id in event_ids
            assert created2.sampling_event_id in event_ids


            looked_up = api_instance.download_sampling_events_by_location(loc.location_id,
                                                                          start=0,
                                                                          count=1)
            looked_up1 = api_instance.download_sampling_events_by_location(loc.location_id,
                                                                           start=1,
                                                                           count=1)
            looked_up2 = api_instance.download_sampling_events_by_location(loc.location_id,
                                                                           start=2,
                                                                           count=1)
            assert looked_up.count == 3
            assert len(looked_up.sampling_events) == 1
            assert looked_up1.count == 3
            assert len(looked_up1.sampling_events) == 1
            assert looked_up2.count == 3
            assert len(looked_up2.sampling_events) == 1

            assert looked_up.sampling_events[0].sampling_event_id != looked_up1.sampling_events[0].sampling_event_id
            assert looked_up.sampling_events[0].sampling_event_id != looked_up2.sampling_events[0].sampling_event_id
            assert looked_up1.sampling_events[0].sampling_event_id != looked_up2.sampling_events[0].sampling_event_id

            assert samp.attrs[0].attr_type in looked_up.attr_types
            assert samp.attrs[1].attr_type in looked_up.attr_types

            os_api_instance.delete_original_sample(os_created.original_sample_id)
            os_api_instance.delete_original_sample(os_created1.original_sample_id)
            os_api_instance.delete_original_sample(os_created2.original_sample_id)
            api_instance.delete_sampling_event(created.sampling_event_id)
            api_instance.delete_sampling_event(created1.sampling_event_id)
            api_instance.delete_sampling_event(created2.sampling_event_id)

            location_api_instance.delete_location(loc1.location_id)
            location_api_instance.delete_location(loc.location_id)


        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)


    """
    """
    def test_missing_location(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        try:

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    fetched = api_instance.download_sampling_events_by_location(str(uuid.uuid4()))
            else:
                with pytest.raises(ApiException, status=403):
                    fetched = api_instance.download_sampling_events_by_location(str(uuid.uuid4()))

        except ApiException as error:
            self.check_api_exception(api_factory,
                                     "SamplingEventApi->download_sampling_events_by_location", error)

    """
    """
    def test_taxa_lookup(self, api_factory):

        os_api_instance = api_factory.OriginalSampleApi()
        api_instance = api_factory.SamplingEventApi()
        study_api = api_factory.StudyApi()

        try:
            study_code = '1010-MD-UP'

            sampling_event = openapi_client.SamplingEvent(None, doc=date(2017, 10, 14))
            sampling_event.attrs = [
                openapi_client.Attr(attr_type='se_oxford', attr_value='12345678',
                                    attr_source='se_taxa_lookup')
            ]
            created_se = api_instance.create_sampling_event(sampling_event)

            samp = openapi_client.OriginalSample(None, study_name=study_code,
                                                 partner_species='PF',
                                                 sampling_event_id=created_se.sampling_event_id)

            samp.attrs = [
                openapi_client.Attr(attr_type='oxford', attr_value='12345678',
                                    attr_source='upd')
            ]
            created_os = os_api_instance.create_original_sample(samp)

            study_detail = study_api.download_study(study_code)

            study_detail.partner_species[0].taxa = [openapi_client.Taxonomy(taxonomy_id=5833)]
            study_api.update_study(study_code, study_detail)

            fetched = api_instance.download_sampling_events_by_taxa(5833)

            assert fetched.count == 1, "Taxa not found"
            assert fetched.attr_types[0] == sampling_event.attrs[0].attr_type

            ffetched = api_instance.download_sampling_events(search_filter='taxa:5833')

            assert ffetched == fetched

            assert created_se == fetched.sampling_events[0], "create response != download response"
            os_api_instance.delete_original_sample(created_os.original_sample_id)

            api_instance.delete_sampling_event(created_se.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)


    """
    """
    def test_missing_taxa(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        try:

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    fetched = api_instance.download_sampling_events_by_taxa(404)
            else:
                with pytest.raises(ApiException, status=403):
                    fetched = api_instance.download_sampling_events_by_taxa(404)

        except ApiException as error:
            self.check_api_exception(api_factory,
                                     "SamplingEventApi->download_sampling_events_by_taxa", error)

    """
    """
    def test_taxa_lookup_paged(self, api_factory):

        os_api_instance = api_factory.OriginalSampleApi()
        api_instance = api_factory.SamplingEventApi()
        study_api = api_factory.StudyApi()

        original_samples = []
        try:
            study_codes = [ '1011-MD-UP', '1012-MD-UP', '1013-MD-UP', '1014-MD-UP', '1014-MD-UP']

            for study_code in study_codes:
                samp_event = openapi_client.SamplingEvent(None, doc=date(2017, 10, 14))
                created_se = api_instance.create_sampling_event(samp_event)
                samp = openapi_client.OriginalSample(None, study_name=study_code,
                                                     partner_species='PF')
                samp.sampling_event_id = created_se.sampling_event_id
                created_os = os_api_instance.create_original_sample(samp)
                original_samples.append(created_os.original_sample_id)
                study_detail = study_api.download_study(study_code)
                study_detail.partner_species[0].taxa = [ openapi_client.Taxonomy(taxonomy_id=5833) ]
                study_api.update_study(study_code, study_detail)



            fetched1 = api_instance.download_sampling_events_by_taxa(5833, start=0, count=2)

            assert len(fetched1.sampling_events) ==2, "Wrong number of sampling_events returned"
            assert fetched1.count == len(study_codes), "Wrong total of sampling_events returned"

            fetched2 = api_instance.download_sampling_events_by_taxa(5833, start=2, count=5)

            #Gets second tranche and also attempts to retrieve more than exist
            assert len(fetched2.sampling_events) ==3, "Wrong number of sampling_events returned"
            assert fetched2.count == len(study_codes), "Wrong total of sampling_events returned"

            ids = []
            for sampling_event in fetched1.sampling_events + fetched2.sampling_events:
                assert not sampling_event.sampling_event_id in ids, "SamplingEvent returned twice"
                ids.append(sampling_event.sampling_event_id)

            #Check that it's the correct number of *unique* events

            #Clean up
            fetch_all = api_instance.download_sampling_events_by_taxa(5833)

            for sampling_event in fetch_all.sampling_events:
                api_instance.delete_sampling_event(sampling_event.sampling_event_id)

            for original_sample in original_samples:
                os_api_instance.delete_original_sample(original_sample)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)


    """
    """
    def test_study_lookup(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        os_api_instance = api_factory.OriginalSampleApi()

        try:
            study_code = '1020-MD-UP'

            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 14))
            created_se = api_instance.create_sampling_event(samp)
            samp = openapi_client.OriginalSample(None, study_name=study_code,
                                                 partner_species='PF',
                                                 sampling_event_id=created_se.sampling_event_id)
            created_os = os_api_instance.create_original_sample(samp)

            fetched = api_instance.download_sampling_events_by_study(study_code)

            assert fetched.count == 1, "Study not found"

            assert created_se == fetched.sampling_events[0], "create response != download response"

            ffetched = api_instance.download_sampling_events(search_filter='studyId:' + study_code)

            assert ffetched.count == 1, "Study not found"

            assert ffetched == fetched

            os_api_instance.delete_original_sample(created_os.original_sample_id)

            api_instance.delete_sampling_event(created_se.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)


    """
    """
    def test_study_lookup_paged(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        os_api_instance = api_factory.OriginalSampleApi()

        try:
            study_code = '1021-MD-UP'

            original_samples = []
            for i in range(5):
                samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 14))
                created = api_instance.create_sampling_event(samp)
                samp = openapi_client.OriginalSample(None, study_name=study_code,
                                                     partner_species='PF')
                samp.sampling_event_id = created.sampling_event_id
                created_os = os_api_instance.create_original_sample(samp)
                original_samples.append(created_os.original_sample_id)



            fetched1 = api_instance.download_sampling_events_by_study(study_code, start=0, count=2)

            assert len(fetched1.sampling_events) == 2, "Wrong number of sampling_events returned"
            assert fetched1.count == 5, "Wrong total of sampling_events returned"

            ffetched = api_instance.download_sampling_events(search_filter='studyId:' + study_code,
                                                             start=0, count=2)

            assert ffetched == fetched1

            fetched2 = api_instance.download_sampling_events_by_study(study_code, start=2, count=5)

            #Gets second tranche and also attempts to retrieve more than exist
            assert len(fetched2.sampling_events) == 3, "Wrong number of sampling_events returned"
            assert fetched2.count == 5, "Wrong total of sampling_events returned"

            ids = []
            for sampling_event in fetched1.sampling_events + fetched2.sampling_events:
                assert not sampling_event.sampling_event_id in ids, "SamplingEvent returned twice"
                ids.append(sampling_event.sampling_event_id)

            #Check that it's the correct number of *unique* events

            #Clean up
            fetch_all = api_instance.download_sampling_events_by_study(study_code)

            for original_sample_id in original_samples:
                os_api_instance.delete_original_sample(original_sample_id)

            for sampling_event in fetch_all.sampling_events:
                api_instance.delete_sampling_event(sampling_event.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)


    """
    """
    def test_event_set_lookup(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        es_api_instance = api_factory.EventSetApi()
        os_api_instance = api_factory.OriginalSampleApi()

        es_name = 'test_event_set_lookup'

        try:
            es_api_instance.create_event_set(es_name)

            study_code = '1022-MD-UP'

            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 14))
            created = api_instance.create_sampling_event(samp)
            os_samp = openapi_client.OriginalSample(None, study_name=study_code,
                                                    partner_species='PF',
                                                    sampling_event_id=created.sampling_event_id)
            os_created = os_api_instance.create_original_sample(os_samp)

            es_api_instance.create_event_set_item(es_name, created.sampling_event_id)

            fetched = api_instance.download_sampling_events_by_event_set(es_name)

            assert fetched.count == 1, "event_set not found"

            created.event_sets = [es_name]

            assert created == fetched.sampling_events[0], "create response != download response"

            ffetched = api_instance.download_sampling_events(search_filter='eventSet:' + es_name)

            assert ffetched == fetched

            os_api_instance.delete_original_sample(os_created.original_sample_id)
            es_api_instance.delete_event_set_item(es_name, created.sampling_event_id)
            api_instance.delete_sampling_event(created.sampling_event_id)

            es_api_instance.delete_event_set(es_name)
        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetApi->create_event_set", error)


    """
    """
    def test_event_set_lookup_complex_name(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        es_api_instance = api_factory.EventSetApi()
        os_api_instance = api_factory.OriginalSampleApi()

        es_name = 'test event set lookup'

        try:
            es_api_instance.create_event_set(es_name)

            study_code = '1023-MD-UP'

            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 14))
            created = api_instance.create_sampling_event(samp)
            os_samp = openapi_client.OriginalSample(None, study_name=study_code,
                                                    partner_species='PF',
                                                    sampling_event_id=created.sampling_event_id)
            os_created = os_api_instance.create_original_sample(os_samp)

            es_api_instance.create_event_set_item(es_name, created.sampling_event_id)

            fetched = api_instance.download_sampling_events_by_event_set(es_name)

            assert fetched.count == 1, "event_set not found"

            created.event_sets = [es_name]

            assert created == fetched.sampling_events[0], "create response != download response"
            es_api_instance.delete_event_set_item(es_name, created.sampling_event_id)
            os_api_instance.delete_original_sample(os_created.original_sample_id)
            api_instance.delete_sampling_event(created.sampling_event_id)

            es_api_instance.delete_event_set(es_name)
        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetApi->create_event_set", error)

    """
    """
    def test_event_set_lookup_missing(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        es_api_instance = api_factory.EventSetApi()

        es_name = '404 test_event_set_lookup'

        try:

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    fetched = api_instance.download_sampling_events_by_event_set(es_name)
            else:
                with pytest.raises(ApiException, status=403):
                    fetched = api_instance.download_sampling_events_by_event_set(es_name)

        except ApiException as error:
            self.check_api_exception(api_factory,
                                     "SamplingEventApi->download_sampling_events_by_event_set", error)


    """
    """
    def test_event_set_lookup_paged(self, api_factory):

        study_code = '1024-MD-UP'

        api_instance = api_factory.SamplingEventApi()
        study_api = api_factory.StudyApi()

        es_api_instance = api_factory.EventSetApi()
        os_api_instance = api_factory.OriginalSampleApi()

        es_name = 'test_event_set_lookup_paged'

        try:
            es_api_instance.create_event_set(es_name)

            original_samples = []
            for i in range(5):
                samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 14))
                created = api_instance.create_sampling_event(samp)
                es_api_instance.create_event_set_item(es_name, created.sampling_event_id)
                os_samp = openapi_client.OriginalSample(None, study_name=study_code,
                                                        partner_species='PF',
                                                        sampling_event_id=created.sampling_event_id)
                os_created = os_api_instance.create_original_sample(os_samp)
                original_samples.append(os_created)


            fetched1 = api_instance.download_sampling_events_by_event_set(es_name, start=0, count=2)

            assert len(fetched1.sampling_events) == 2, "Wrong number of sampling_events returned"
            assert fetched1.count == 5, "Wrong total of sampling_events returned"

            ffetched = api_instance.download_sampling_events(search_filter='eventSet:' + es_name, start=0,
                                                             count=2)

            assert ffetched == fetched1

            fetched2 = api_instance.download_sampling_events_by_event_set(es_name, start=2, count=5)

            #Gets second tranche and also attempts to retrieve more than exist
            assert len(fetched2.sampling_events) == 3, "Wrong number of sampling_events returned"
            assert fetched2.count == 5, "Wrong total of sampling_events returned"

            ids = []
            for sampling_event in fetched1.sampling_events + fetched2.sampling_events:
                assert not sampling_event.sampling_event_id in ids, "SamplingEvent returned twice"
                ids.append(sampling_event.sampling_event_id)

            #Check that it's the correct number of *unique* events

            #Clean up
            fetch_all = api_instance.download_sampling_events_by_event_set(es_name)

            for os_created in original_samples:
                os_api_instance.delete_original_sample(os_created.original_sample_id)
            for sampling_event in fetch_all.sampling_events:
                es_api_instance.delete_event_set_item(es_name, sampling_event.sampling_event_id)
                api_instance.delete_sampling_event(sampling_event.sampling_event_id)

            es_api_instance.delete_event_set(es_name)

        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetApi->create_event_set", error)

    """
    """
    def test_get_attrs(self, api_factory):

        metadata_api_instance = api_factory.MetadataApi()
        api_instance = api_factory.SamplingEventApi()

        try:
            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 16))
            samp.attrs = [
                openapi_client.Attr (attr_type='oxford', attr_value='12345678',
                                     attr_source='upd')
            ]
            created = api_instance.create_sampling_event(samp)
            idents = metadata_api_instance.get_attr_types()

            assert 'oxford' in idents

            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    Used to test permissions on get_attr_types
    """
    def test_get_attr_types(self, api_factory):

        metadata_api_instance = api_factory.MetadataApi()

        try:
            idents = metadata_api_instance.get_attr_types()

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)



    """
    """
    def test_create_with_location_integrity_failure(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        location_api_instance = api_factory.LocationApi()

        try:

            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 10),
                                                doc_accuracy='month')
            loc = openapi_client.Location(None, latitude=27.463,
                                          longitude=90.495,
                                          accuracy='city',
                                          curated_name='Trongsa, Trongsa, Bhutan',
                                          notes='test_create_with_locations',
                                          country='BTN')
            loc = location_api_instance.create_location(loc)

            samp.location_id = loc.location_id
            samp.location = loc
            samp.location.accuracy = 'region'

            with pytest.raises(ApiException, status=422):
                created = api_instance.create_sampling_event(samp)

            location_api_instance.delete_location(loc.location_id)


        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_create_with_proxy_location_integrity_failure(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        location_api_instance = api_factory.LocationApi()

        try:

            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 10),
                                                doc_accuracy='month')
            loc = openapi_client.Location(None, latitude=27.463,
                                          longitude=90.495,
                                          accuracy='city',
                                          curated_name='Trongsa, Trongsa, Bhutan',
                                          notes='test_create_with_locations',
                                          country='BTN')
            loc = location_api_instance.create_location(loc)

            samp.proxy_location_id = loc.location_id
            samp.proxy_location = loc
            samp.proxy_location.accuracy = 'region'

            with pytest.raises(ApiException, status=422):
                created = api_instance.create_sampling_event(samp)

            location_api_instance.delete_location(loc.location_id)


        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)


    """
    """
    def test_update_with_location_integrity_failure(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        location_api_instance = api_factory.LocationApi()

        try:

            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 10),
                                                doc_accuracy='month')
            loc = openapi_client.Location(None, latitude=27.463,
                                          longitude=90.495,
                                          accuracy='city',
                                          curated_name='Trongsa, Trongsa, Bhutan',
                                          notes='test_create_with_locations',
                                          country='BTN')
            loc = location_api_instance.create_location(loc)

            samp.location_id = loc.location_id

            created = api_instance.create_sampling_event(samp)

            created.location.accuracy = 'region'

            with pytest.raises(ApiException, status=422):
                created1 = api_instance.update_sampling_event(created.sampling_event_id, created)

            api_instance.delete_sampling_event(created.sampling_event_id)
            location_api_instance.delete_location(loc.location_id)


        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)

    """
    """
    def test_update_with_proxy_location_integrity_failure(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        location_api_instance = api_factory.LocationApi()

        try:

            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 10),
                                                doc_accuracy='month')
            loc = openapi_client.Location(None, latitude=27.463,
                                          longitude=90.495,
                                          accuracy='city',
                                          curated_name='Trongsa, Trongsa, Bhutan',
                                          notes='test_create_with_locations',
                                          country='BTN')
            loc1 = openapi_client.Location(None, latitude=27.46,
                                           longitude=90.49,
                                           accuracy='city',
                                           curated_name='Trongsa, Trongsa, Bhutan',
                                           notes='test_create_with_locations',
                                           country='BTN')
            loc1 = location_api_instance.create_location(loc1)
            loc.proxy_location_id = loc1.location_id
            loc = location_api_instance.create_location(loc)

            samp.location_id = loc.location_id
            samp.proxy_location_id = loc1.location_id

            created = api_instance.create_sampling_event(samp)

            created.proxy_location.accuracy = 'region'

            with pytest.raises(ApiException, status=422):
                created1 = api_instance.update_sampling_event(created.sampling_event_id, created)

            api_instance.delete_sampling_event(created.sampling_event_id)
            location_api_instance.delete_location(loc.location_id)
            location_api_instance.delete_location(loc1.location_id)


        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)

    """
    """
    def test_download_sampling_event_permission(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:
            if not api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=403):
                    api_instance.download_sampling_event(str(uuid.uuid4()))
        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->download_sampling_event", error)

    """
    """
    def test_download_sampling_event_by_attr_permission(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:
            if not api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=403):
                    api_instance.download_sampling_events_by_attr('partner_id','404')
        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->download_sampling_events_by_attr", error)


    """
    """
    def test_lookup_sampling_event_by_os_attr(self, api_factory):

        api_instance = api_factory.OriginalSampleApi()
        se_api_instance = api_factory.SamplingEventApi()
        location_api_instance = api_factory.LocationApi()

        try:

            sampling_event = openapi_client.SamplingEvent(None, doc=date(2017, 10, 10),
                                                          doc_accuracy='month')
            created_se = se_api_instance.create_sampling_event(sampling_event)

            samp = openapi_client.OriginalSample(None, study_name='4024-MD-UP')
            samp.sampling_event_id = created_se.sampling_event_id

            samp.attrs = [
                openapi_client.Attr (attr_type='oxford', attr_value='12345678',
                                     attr_source='upd')
            ]
            created = api_instance.create_original_sample(samp)

            results = se_api_instance.download_sampling_events_by_os_attr('oxford', '12345678')

            assert results.count == 1

            looked_up = results.sampling_events[0]

            fetched = se_api_instance.download_sampling_event(looked_up.sampling_event_id)

            assert created_se == fetched, "create response != download response"

            results1 = se_api_instance.download_sampling_events_by_os_attr('oxford', '12345678',
                                                                           study_name='4024-MD-UP')

            assert results == results1

            ffetched = se_api_instance.download_sampling_events(search_filter='os_attr:oxford:12345678:4024')

            assert ffetched == results1

            results2 = se_api_instance.download_sampling_events_by_os_attr('oxford', '12345678',
                                                                           study_name='1027-MD-UP')

            assert not results2.sampling_events
            assert results2.count == 0

            se_api_instance.delete_sampling_event(created_se.sampling_event_id)

            api_instance.delete_original_sample(created.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

    def get_merge_events(self):

            #Uses partner_id because only partner_id and individual_id are allowed to
            #have the same value assigned to different sampling events
        samp1 = openapi_client.SamplingEvent(None, doc=date(2017, 10, 16))
        samp1.attrs = [
            openapi_client.Attr(attr_type='partner_id', attr_value='mrg1-12345678',
                                attr_source='mrg')
        ]
        samp1.doc_accuracy = 'day'
        samp2 = openapi_client.SamplingEvent(None, doc=date(2017, 10, 16))
        samp2.attrs = [
            openapi_client.Attr(attr_type='partner_id', attr_value='mrg2-12345678',
                                attr_source='mrg')
        ]
        samp2.doc_accuracy = 'day'

        return samp1, samp2

    """
    """
    def test_merge_sampling_events(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            samp1, samp2 = self.get_merge_events()

            created1 = api_instance.create_sampling_event(samp1)
            created2 = api_instance.create_sampling_event(samp2)

            api_instance.merge_sampling_events(created1.sampling_event_id,
                                               created2.sampling_event_id)

            fetched = api_instance.download_sampling_event(created1.sampling_event_id)

            for attr in samp1.attrs:
                assert attr in fetched.attrs
                for attr in samp2.attrs:
                    assert attr in fetched.attrs

            api_instance.delete_sampling_event(created1.sampling_event_id)

            with pytest.raises(ApiException, status=404):
                fetched = api_instance.download_sampling_event(created2.sampling_event_id)
        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_merge_sampling_events_missing(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            samp1, samp2 = self.get_merge_events()

            created1 = api_instance.create_sampling_event(samp1)

            with pytest.raises(ApiException, status=404):
                api_instance.merge_sampling_events(created1.sampling_event_id,
                                                   str(uuid.uuid4()))

            with pytest.raises(ApiException, status=404):
                api_instance.merge_sampling_events(str(uuid.uuid4()),
                                                   created1.sampling_event_id)

            with pytest.raises(ApiException, status=404):
                api_instance.merge_sampling_events(str(uuid.uuid4()),
                                                   str(uuid.uuid4()))
            api_instance.delete_sampling_event(created1.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_merge_sampling_events_doc1_none(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            samp1, samp2 = self.get_merge_events()

            samp1.doc = None

            created1 = api_instance.create_sampling_event(samp1)
            created2 = api_instance.create_sampling_event(samp2)

            api_instance.merge_sampling_events(created1.sampling_event_id,
                                               created2.sampling_event_id)

            fetched = api_instance.download_sampling_event(created1.sampling_event_id)

            for attr in samp1.attrs:
                assert attr in fetched.attrs
                for attr in samp2.attrs:
                    assert attr in fetched.attrs

            assert fetched.doc == samp2.doc

            api_instance.delete_sampling_event(created1.sampling_event_id)

            with pytest.raises(ApiException, status=404):
                fetched = api_instance.download_sampling_event(created2.sampling_event_id)
        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_merge_sampling_events_doc2_none(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            samp1, samp2 = self.get_merge_events()

            samp2.doc = None

            created1 = api_instance.create_sampling_event(samp1)
            created2 = api_instance.create_sampling_event(samp2)

            api_instance.merge_sampling_events(created1.sampling_event_id,
                                               created2.sampling_event_id)

            fetched = api_instance.download_sampling_event(created1.sampling_event_id)

            for attr in samp1.attrs:
                assert attr in fetched.attrs
                for attr in samp2.attrs:
                    assert attr in fetched.attrs

            assert fetched.doc == samp1.doc

            api_instance.delete_sampling_event(created1.sampling_event_id)

            with pytest.raises(ApiException, status=404):
                fetched = api_instance.download_sampling_event(created2.sampling_event_id)
        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)



    """
    """
    def test_merge_sampling_events_doc_fail(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            samp1, samp2 = self.get_merge_events()

            samp2.doc= date(2018, 10, 16)

            created1 = api_instance.create_sampling_event(samp1)
            created2 = api_instance.create_sampling_event(samp2)

            with pytest.raises(ApiException, status=422):
                api_instance.merge_sampling_events(created1.sampling_event_id,
                                                   created2.sampling_event_id)

            fetched = api_instance.download_sampling_event(created1.sampling_event_id)

            assert fetched == created1

            api_instance.delete_sampling_event(created1.sampling_event_id)
            api_instance.delete_sampling_event(created2.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)


    """
    """
    def test_merge_sampling_events_doc_accuracy1_none(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            samp1, samp2 = self.get_merge_events()

            samp1._doc_accuracy = None

            created1 = api_instance.create_sampling_event(samp1)
            created2 = api_instance.create_sampling_event(samp2)

            api_instance.merge_sampling_events(created1.sampling_event_id,
                                               created2.sampling_event_id)

            fetched = api_instance.download_sampling_event(created1.sampling_event_id)

            for attr in samp1.attrs:
                assert attr in fetched.attrs
                for attr in samp2.attrs:
                    assert attr in fetched.attrs

            assert fetched.doc_accuracy == samp2.doc_accuracy

            api_instance.delete_sampling_event(created1.sampling_event_id)

            with pytest.raises(ApiException, status=404):
                fetched = api_instance.download_sampling_event(created2.sampling_event_id)
        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_merge_sampling_events_doc_accuracy2_none(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            samp1, samp2 = self.get_merge_events()

            samp2._doc_accuracy = None

            created1 = api_instance.create_sampling_event(samp1)
            created2 = api_instance.create_sampling_event(samp2)

            api_instance.merge_sampling_events(created1.sampling_event_id,
                                               created2.sampling_event_id)

            fetched = api_instance.download_sampling_event(created1.sampling_event_id)

            for attr in samp1.attrs:
                assert attr in fetched.attrs
                for attr in samp2.attrs:
                    assert attr in fetched.attrs

            assert fetched.doc_accuracy == samp1.doc_accuracy

            api_instance.delete_sampling_event(created1.sampling_event_id)

            with pytest.raises(ApiException, status=404):
                fetched = api_instance.download_sampling_event(created2.sampling_event_id)
        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)



    """
    """
    def test_merge_sampling_events_doc_accuracy_fail(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            samp1, samp2 = self.get_merge_events()

            samp2.doc_accuracy = 'month'

            created1 = api_instance.create_sampling_event(samp1)
            created2 = api_instance.create_sampling_event(samp2)

            with pytest.raises(ApiException, status=422):
                api_instance.merge_sampling_events(created1.sampling_event_id,
                                                   created2.sampling_event_id)

            fetched = api_instance.download_sampling_event(created1.sampling_event_id)

            assert fetched == created1

            api_instance.delete_sampling_event(created1.sampling_event_id)
            api_instance.delete_sampling_event(created2.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)




    """
    """
    def test_merge_sampling_events_location1_none(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        location_api_instance = api_factory.LocationApi()

        try:

            loc = openapi_client.Location(None, latitude=27.463,
                                          longitude=90.495,
                                          accuracy='city',
                                          curated_name='Trongsa, Trongsa, Bhutan',
                                          notes='test_create_with_locations',
                                          country='BTN')
            loc = location_api_instance.create_location(loc)


            samp1, samp2 = self.get_merge_events()

            samp2.location_id = loc.location_id

            created1 = api_instance.create_sampling_event(samp1)
            created2 = api_instance.create_sampling_event(samp2)

            api_instance.merge_sampling_events(created1.sampling_event_id,
                                               created2.sampling_event_id)

            fetched = api_instance.download_sampling_event(created1.sampling_event_id)

            for attr in samp1.attrs:
                assert attr in fetched.attrs
                for attr in samp2.attrs:
                    assert attr in fetched.attrs

            assert fetched.location_id == samp2.location_id

            api_instance.delete_sampling_event(created1.sampling_event_id)
            location_api_instance.delete_location(loc.location_id)

            with pytest.raises(ApiException, status=404):
                fetched = api_instance.download_sampling_event(created2.sampling_event_id)
        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_merge_sampling_events_location2_none(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        location_api_instance = api_factory.LocationApi()

        try:

            loc = openapi_client.Location(None, latitude=27.463,
                                          longitude=90.495,
                                          accuracy='city',
                                          curated_name='Trongsa, Trongsa, Bhutan',
                                          notes='test_create_with_locations',
                                          country='BTN')
            loc = location_api_instance.create_location(loc)

            samp1, samp2 = self.get_merge_events()

            samp1.location_id = loc.location_id

            created1 = api_instance.create_sampling_event(samp1)
            created2 = api_instance.create_sampling_event(samp2)

            api_instance.merge_sampling_events(created1.sampling_event_id,
                                               created2.sampling_event_id)

            fetched = api_instance.download_sampling_event(created1.sampling_event_id)

            for attr in samp1.attrs:
                assert attr in fetched.attrs
                for attr in samp2.attrs:
                    assert attr in fetched.attrs

            assert fetched.location_id == samp1.location_id

            api_instance.delete_sampling_event(created1.sampling_event_id)
            location_api_instance.delete_location(loc.location_id)

            with pytest.raises(ApiException, status=404):
                fetched = api_instance.download_sampling_event(created2.sampling_event_id)
        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)



    """
    """
    def test_merge_sampling_events_location_fail(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        location_api_instance = api_factory.LocationApi()

        try:

            loc1 = openapi_client.Location(None, latitude=27.463,
                                           longitude=90.495,
                                           accuracy='city',
                                           curated_name='Trongsa, Trongsa, Bhutan',
                                           notes='test_create_with_locations',
                                           country='BTN')
            loc1 = location_api_instance.create_location(loc1)

            loc2 = openapi_client.Location(None, latitude=27.46, longitude=90.49,
                                           accuracy='city',
                                           curated_name='Trongsa, Bhutan',
                                           notes='test_create_with_locations',
                                           country='BTN')
            loc2 = location_api_instance.create_location(loc2)

            samp1, samp2 = self.get_merge_events()

            samp1.location_id = loc1.location_id
            samp2.location_id = loc2.location_id

            created1 = api_instance.create_sampling_event(samp1)
            created2 = api_instance.create_sampling_event(samp2)

            with pytest.raises(ApiException, status=422):
                api_instance.merge_sampling_events(created1.sampling_event_id,
                                                   created2.sampling_event_id)

            fetched = api_instance.download_sampling_event(created1.sampling_event_id)

            assert fetched == created1

            api_instance.delete_sampling_event(created1.sampling_event_id)
            api_instance.delete_sampling_event(created2.sampling_event_id)
            location_api_instance.delete_location(loc1.location_id)
            location_api_instance.delete_location(loc2.location_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_merge_sampling_events_proxy_location1_none(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        proxy_location_api_instance = api_factory.LocationApi()

        try:

            loc = openapi_client.Location(None, longitude=27.46, latitude=90.49,
                                          accuracy='city',
                                          curated_name='Trongsa, Trongsa, Bhutan',
                                          notes='test_create_with_proxy_locations',
                                          country='BTN')
            loc = proxy_location_api_instance.create_location(loc)


            loc1 = openapi_client.Location(None, longitude=27.463, latitude=90.495,
                                           accuracy='city',
                                           curated_name='Trongsa, Trongsa, Bhutan',
                                           notes='test_create_with_proxy_locations',
                                           proxy_location_id=loc.location_id,
                                           country='BTN')
            loc1 = proxy_location_api_instance.create_location(loc1)


            samp1, samp2 = self.get_merge_events()

            samp2.location_id = loc1.location_id
            samp2.proxy_location_id = loc.location_id

            created1 = api_instance.create_sampling_event(samp1)
            created2 = api_instance.create_sampling_event(samp2)

            api_instance.merge_sampling_events(created1.sampling_event_id,
                                               created2.sampling_event_id)

            fetched = api_instance.download_sampling_event(created1.sampling_event_id)

            for attr in samp1.attrs:
                assert attr in fetched.attrs
                for attr in samp2.attrs:
                    assert attr in fetched.attrs

            assert fetched.proxy_location_id == samp2.proxy_location_id

            api_instance.delete_sampling_event(created1.sampling_event_id)
            proxy_location_api_instance.delete_location(loc1.location_id)
            proxy_location_api_instance.delete_location(loc.location_id)

            with pytest.raises(ApiException, status=404):
                fetched = api_instance.download_sampling_event(created2.sampling_event_id)
        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_merge_sampling_events_proxy_location2_none(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        proxy_location_api_instance = api_factory.LocationApi()

        try:

            loc1 = openapi_client.Location(None, latitude=27.46, longitude=90.49,
                                          accuracy='city',
                                          curated_name='Trongsa, Trongsa, Bhutan',
                                          notes='test_create_with_proxy_locations',
                                          country='BTN')
            loc1 = proxy_location_api_instance.create_location(loc1)

            loc = openapi_client.Location(None, latitude=27.463, longitude=90.495,
                                          accuracy='city',
                                          curated_name='Trongsa, Trongsa, Bhutan',
                                          notes='test_create_with_proxy_locations',
                                          proxy_location_id=loc1.location_id,
                                          country='BTN')
            loc = proxy_location_api_instance.create_location(loc)

            samp1, samp2 = self.get_merge_events()

            samp1.proxy_location_id = loc1.location_id
            samp1.location_id = loc.location_id

            created1 = api_instance.create_sampling_event(samp1)
            created2 = api_instance.create_sampling_event(samp2)

            api_instance.merge_sampling_events(created1.sampling_event_id,
                                               created2.sampling_event_id)

            fetched = api_instance.download_sampling_event(created1.sampling_event_id)

            for attr in samp1.attrs:
                assert attr in fetched.attrs
                for attr in samp2.attrs:
                    assert attr in fetched.attrs

            assert fetched.proxy_location_id == samp1.proxy_location_id

            api_instance.delete_sampling_event(created1.sampling_event_id)
            proxy_location_api_instance.delete_location(loc.location_id)
            proxy_location_api_instance.delete_location(loc1.location_id)

            with pytest.raises(ApiException, status=404):
                fetched = api_instance.download_sampling_event(created2.sampling_event_id)
        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)



    """
    """
    def test_merge_sampling_events_proxy_location_fail(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        location_api_instance = api_factory.LocationApi()

        try:

            loc1 = openapi_client.Location(None, latitude=27.463, longitude=90.495,
                                           accuracy='city',
                                           curated_name='Trongsa, Trongsa, Bhutan',
                                           notes='test_create_with_proxy_locations',
                                           country='BTN')
            loc1 = location_api_instance.create_location(loc1)

            loc2 = openapi_client.Location(None, latitude=27.46, longitude=90.49,
                                           accuracy='city',
                                           curated_name='Trongsa, Bhutan',
                                           notes='test_create_with_proxy_locations',
                                           country='BTN')
            loc2 = location_api_instance.create_location(loc2)

            loc3 = openapi_client.Location(None, latitude=27.46, longitude=90.49,
                                           accuracy='city',
                                           curated_name='Trongsa, Bhutan',
                                           notes='test_create_with_proxy_locations',
                                           proxy_location_id=loc1.location_id,
                                           country='BTN')
            loc3 = location_api_instance.create_location(loc3)

            loc4 = openapi_client.Location(None, latitude=27.46, longitude=90.49,
                                           accuracy='city',
                                           curated_name='Trongsa, Bhutan',
                                           notes='test_create_with_proxy_locations',
                                           proxy_location_id=loc2.location_id,
                                           country='BTN')
            loc4 = location_api_instance.create_location(loc4)

            samp1, samp2 = self.get_merge_events()

            samp1.proxy_location_id = loc1.location_id
            samp1.location_id = loc3.location_id
            samp2.proxy_location_id = loc2.location_id
            samp2.location_id = loc4.location_id

            created1 = api_instance.create_sampling_event(samp1)
            created2 = api_instance.create_sampling_event(samp2)

            with pytest.raises(ApiException, status=422):
                api_instance.merge_sampling_events(created1.sampling_event_id,
                                                   created2.sampling_event_id)

            fetched = api_instance.download_sampling_event(created1.sampling_event_id)

            assert fetched == created1

            api_instance.delete_sampling_event(created1.sampling_event_id)
            api_instance.delete_sampling_event(created2.sampling_event_id)
            location_api_instance.delete_location(loc4.location_id)
            location_api_instance.delete_location(loc2.location_id)
            location_api_instance.delete_location(loc3.location_id)
            location_api_instance.delete_location(loc1.location_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_merge_sampling_events_attr_dedup(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            samp1, samp2 = self.get_merge_events()

            expected = len(samp1.attrs) + len(samp2.attrs)

            samp2.attrs.append(samp1.attrs[0])

            created1 = api_instance.create_sampling_event(samp1)
            created2 = api_instance.create_sampling_event(samp2)

            api_instance.merge_sampling_events(created1.sampling_event_id,
                                               created2.sampling_event_id)

            fetched = api_instance.download_sampling_event(created1.sampling_event_id)

            for attr in samp1.attrs:
                assert attr in fetched.attrs
                for attr in samp2.attrs:
                    assert attr in fetched.attrs

            assert len(fetched.attrs) == expected

            api_instance.delete_sampling_event(created1.sampling_event_id)

            with pytest.raises(ApiException, status=404):
                fetched = api_instance.download_sampling_event(created2.sampling_event_id)
        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_os_filter_fail(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            with pytest.raises(ApiException, status=422):
                ffetched = api_instance.download_sampling_events(search_filter='xxxxx')

            with pytest.raises(ApiException, status=422):
                ffetched = api_instance.download_sampling_events(search_filter='xxxxx:xxxxx')

            with pytest.raises(ApiException, status=422):
                ffetched = api_instance.download_sampling_events(search_filter='attr:oxford_id')

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->download_sampling_events", error)

    """
    """
    def test_create_future_date(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            samp = openapi_client.SamplingEvent(None, doc=date(2037, 10, 10),
                                                doc_accuracy='month')
            with pytest.raises(ApiException, status=422):
                created = api_instance.create_sampling_event(samp)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_update_future_date(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 15))
            samp.attrs = [
                openapi_client.Attr (attr_type='oxford', attr_value='1234567')
            ]
            created = api_instance.create_sampling_event(samp)
            looked_up = api_instance.download_sampling_events_by_attr('oxford', '1234567')
            looked_up = looked_up.sampling_events[0]
            new_samp = openapi_client.SamplingEvent(None, doc=date(2038, 11, 11))
            with pytest.raises(ApiException, status=422):
                updated = api_instance.update_sampling_event(looked_up.sampling_event_id, new_samp)
            fetched = api_instance.download_sampling_event(looked_up.sampling_event_id)
            assert created == fetched, "update response != download response"

            api_instance.delete_sampling_event(looked_up.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_create_with_individual(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        individual_api_instance = api_factory.IndividualApi()

        try:

            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 10),
                                                doc_accuracy='month')
            indiv = openapi_client.Individual(None)
            ident = openapi_client.Attr(attr_type='patient_id', attr_value='Tron',
                                        study_name='9090-MD-UP')
            indiv.attrs = [
                ident
            ]
            indiv = individual_api_instance.create_individual(indiv)

            samp.individual_id = indiv.individual_id
            created = api_instance.create_sampling_event(samp)
            fetched = api_instance.download_sampling_event(created.sampling_event_id)

            assert samp.individual_id == created.individual_id, "upload individual != response"
            assert samp.individual_id == fetched.individual_id, "upload individual != download response"

            individual_api_instance.delete_individual(indiv.individual_id)
            api_instance.delete_sampling_event(created.sampling_event_id)


        except ApiException as error:
            self.check_api_exception(api_factory, "IndividualApi->create_individual", error)

    """
    """
    def test_update_with_individual(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        individual_api_instance = api_factory.IndividualApi()

        try:

            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 10),
                                                doc_accuracy='month')
            indiv = openapi_client.Individual(None)
            ident = openapi_client.Attr(attr_type='patient_id', attr_value='Tron',
                                        study_name='9090-MD-UP')
            indiv.attrs = [
                ident
            ]
            indiv = individual_api_instance.create_individual(indiv)

            created = api_instance.create_sampling_event(samp)
            created.individual_id = indiv.individual_id
            updated = api_instance.update_sampling_event(created.sampling_event_id,
                                                         created)
            fetched = api_instance.download_sampling_event(created.sampling_event_id)
            assert indiv.individual_id == fetched.individual_id, "upload individual != download response"

            individual_api_instance.delete_individual(indiv.individual_id)
            api_instance.delete_sampling_event(created.sampling_event_id)


        except ApiException as error:
            self.check_api_exception(api_factory, "IndividualApi->create_individual", error)
