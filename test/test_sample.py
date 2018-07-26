import swagger_client
from swagger_client.rest import ApiException

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

            samp = swagger_client.SamplingEvent(None, '1000-MD-UP', date(2017, 10, 10),
                                                doc_accuracy='month')
            created = api_instance.create_sampling_event(samp)
            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to create_sampling_event succeeded')

            fetched = api_instance.download_sampling_event(created.sampling_event_id)
            assert created == fetched, "create response != download response"
            fetched.sampling_event_id = None
            assert samp == fetched, "upload != download response"
            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_delete(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            samp = swagger_client.SamplingEvent(None, '1001-MD-UP', date(2017, 10, 11))
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

            samp = swagger_client.SamplingEvent(None, '1002-MD-UP', date(2017, 10, 12))
            samp.attrs = [
                swagger_client.Attr (attr_type='oxford', attr_value='1234',
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

            samp = swagger_client.SamplingEvent(None, '1003-MD-UP', date(2017, 10, 13))
            samp.attrs = [
                swagger_client.Attr (attr_type='partner_id', attr_value='12345')
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

            samp = swagger_client.SamplingEvent(None, '1025-MD-UP', date(2017, 10, 13))
            samp.attrs = [
                swagger_client.Attr (attr_type='individual_id', attr_value='12345')
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

        try:

            samp = swagger_client.SamplingEvent(None, '1004-MD-UP', date(2017, 10, 14))
            samp.attrs = [
                swagger_client.Attr (attr_type='oxford', attr_value='123456')
            ]
            created = api_instance.create_sampling_event(samp)
            results = api_instance.download_sampling_events_by_attr('oxford', '123456')
            looked_up = results.sampling_events[0]

            fetched = api_instance.download_sampling_event(looked_up.sampling_event_id)

            assert created == fetched, "create response != download response"

            ffetched = api_instance.download_sampling_events(filter='attr:oxford:123456')

            assert ffetched == results

            fetched.sampling_event_id = None
            assert samp == fetched, "upload != download response"

            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_attr_lookup_by_study(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            samp = swagger_client.SamplingEvent(None, '1022-MD-UP', date(2017, 10, 14))
            samp.attrs = [
                swagger_client.Attr (attr_type='partner_id', attr_value='123456')
            ]
            created = api_instance.create_sampling_event(samp)
            looked_up = api_instance.download_sampling_events_by_attr('partner_id', '123456',
                                                                            study_name='1022')
            assert looked_up.count == 1


            with pytest.raises(ApiException, status=404):
                looked_up = api_instance.download_sampling_events_by_attr('oxford', '123456',
                                                                            study_name='9999')

            created1 = api_instance.create_sampling_event(samp)

            looked_up = api_instance.download_sampling_events_by_attr('partner_id', '123456',
                                                                            study_name='1022')
            assert looked_up.count == 2

            ffetched = api_instance.download_sampling_events(filter='attr:partner_id:123456:1022')

            assert ffetched == looked_up

            api_instance.delete_sampling_event(created.sampling_event_id)
            api_instance.delete_sampling_event(created1.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_attr_merge(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            ident1 = swagger_client.Attr(attr_type='oxford_id', attr_value='1234')
            ident2 = swagger_client.Attr(attr_type='roma_id', attr_value='12345')
            ident3 = swagger_client.Attr(attr_type='lims_id', attr_value='123456')
            samp1 = swagger_client.SamplingEvent(None, '1022-MD-UP', date(2017, 10, 14))
            samp1.attrs = [
                ident1
            ]
            created1 = api_instance.create_sampling_event(samp1)

            samp2 = swagger_client.SamplingEvent(None, '1022-MD-UP', date(2017, 10, 14))
            samp2.attrs = [
                ident2
            ]
            created2 = api_instance.create_sampling_event(samp2)


            samp3 = swagger_client.SamplingEvent(None, '1022-MD-UP', date(2017, 10, 14))
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

            samp = swagger_client.SamplingEvent(None, '1005-MD-UP', date(2017, 10, 15))
            samp.attrs = [
                swagger_client.Attr (attr_type='oxford', attr_value='1234567')
            ]
            created = api_instance.create_sampling_event(samp)
            looked_up = api_instance.download_sampling_events_by_attr('oxford', '1234567')
            looked_up = looked_up.sampling_events[0]
            new_samp = swagger_client.SamplingEvent(None, '0001-MD-UP', date(2018, 11, 11))
            updated = api_instance.update_sampling_event(looked_up.sampling_event_id, new_samp)
            fetched = api_instance.download_sampling_event(looked_up.sampling_event_id)
            assert updated == fetched, "update response != download response"
            fetched.sampling_event_id = None
            assert new_samp == fetched, "update != download response"
            api_instance.delete_sampling_event(looked_up.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_update_duplicate(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:

            samp = swagger_client.SamplingEvent(None, '1006-MD-UP', date(2017, 10, 16))
            samp.attrs = [
                swagger_client.Attr (attr_type='oxford', attr_value='12345678',
                                           attr_source='upd')
            ]
            created = api_instance.create_sampling_event(samp)
            looked_up = api_instance.download_sampling_events_by_attr('oxford', '12345678')
            looked_up = looked_up.sampling_events[0]
            new_samp = swagger_client.SamplingEvent(None, '0001-MD-UP', date(2018, 10, 10))
            new_samp.attrs = [
                swagger_client.Attr (attr_type='oxford', attr_value='123456789',
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

            new_samp = swagger_client.SamplingEvent(None, '1007-MD-UP', date(2018, 11, 17))
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

        try:

            test_id = 'MDG/DK_0005'
            samp = swagger_client.SamplingEvent(None, '1008-MD-UP', date(2017, 10, 14))
            samp.attrs = [
                swagger_client.Attr (attr_type='partner_id', attr_value=test_id,
                                          attr_source='encode')
            ]
            created = api_instance.create_sampling_event(samp)

            fetched = api_instance.download_sampling_event(created.sampling_event_id)

            assert created == fetched, "create response != download response"
            fetched.sampling_event_id = None
            assert samp == fetched, "upload != download response"

            results = api_instance.download_sampling_events_by_attr('partner_id',
                                                                      urllib.parse.quote_plus(test_id))
            looked_up = results.sampling_events[0]
            fetched = api_instance.download_sampling_event(looked_up.sampling_event_id)

            assert created == fetched, "create response != download response"
            fetched.sampling_event_id = None
            assert samp == fetched, "upload != download response"

            ffetched = api_instance.download_sampling_events(filter=urllib.parse.quote_plus('attr:partner_id:' + test_id))

            assert ffetched == results

            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)

    """
    """
    def test_create_with_locations(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        location_api_instance = api_factory.LocationApi()

        try:

            samp = swagger_client.SamplingEvent(None, '1009-MD-UP', date(2017, 10, 10),
                                                doc_accuracy='month')
            loc = swagger_client.Location(None, 27.463, 90.495, 'city',
                                          'Trongsa, Trongsa, Bhutan', 'test_create_with_locations', 'BTN')
            loc = location_api_instance.create_location(loc)

            samp.location_id = loc.location_id
            created = api_instance.create_sampling_event(samp)
            fetched = api_instance.download_sampling_event(created.sampling_event_id)
            assert samp.location_id == fetched.location_id, "upload location != download response"
            assert samp.location_id == fetched.public_location_id, "upload public_location != proxy download response"

            proxy_loc = swagger_client.Location(None, 27.4, 90.4, 'region',
                                          'Trongsa, Bhutan', 'test_create_with_locations', 'BTN')
            proxy_loc = location_api_instance.create_location(proxy_loc)
            samp.proxy_location_id = proxy_loc.location_id
            fetched = api_instance.update_sampling_event(fetched.sampling_event_id, samp)
            assert samp.location_id == fetched.location_id, "upload location != download response"
            assert samp.proxy_location_id == fetched.proxy_location_id, "upload proxy_location != download response"
            assert samp.proxy_location_id == fetched.public_location_id, "upload public_location != proxy download response"

            looked_up = api_instance.download_sampling_events_by_location(loc.location_id)

            assert looked_up.count == 1

            looked_up = api_instance.download_sampling_events_by_location(proxy_loc.location_id)

            assert looked_up.count == 1

            api_instance.delete_sampling_event(created.sampling_event_id)

            location_api_instance.delete_location(loc.location_id)
            location_api_instance.delete_location(proxy_loc.location_id)


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

        api_instance = api_factory.SamplingEventApi()
        study_api = api_factory.StudyApi()

        try:
            study_code = '1010-MD-UP'

            samp = swagger_client.SamplingEvent(None, study_code, date(2017, 10, 14),
                                                partner_species='PF')
            created = api_instance.create_sampling_event(samp)
            study_detail = study_api.download_study(study_code)
            study_detail.partner_species[0].taxa = [ swagger_client.Taxonomy(taxonomy_id=5833) ]
            study_api.update_study(study_code, study_detail)

            fetched = api_instance.download_sampling_events_by_taxa(5833)

            assert fetched.count == 1, "Taxa not found"

            assert fetched.sampling_events[0].partner_taxonomies is not None, 'Taxonomies missing'
            assert int(fetched.sampling_events[0].partner_taxonomies[0].taxonomy_id) == 5833, 'Wrong Taxonomy'

            ffetched = api_instance.download_sampling_events(filter='taxa:5833')

            assert ffetched == fetched

            #As the taxonomy wasn't set when created was created it won't be in the response
            #separate test for this
            fetched.sampling_events[0].partner_taxonomies = None
            assert created == fetched.sampling_events[0], "create response != download response"

            api_instance.delete_sampling_event(created.sampling_event_id)

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

        api_instance = api_factory.SamplingEventApi()
        study_api = api_factory.StudyApi()

        try:
            study_codes = [ '1011-MD-UP', '1012-MD-UP', '1013-MD-UP', '1014-MD-UP', '1014-MD-UP']

            for study_code in study_codes:
                samp = swagger_client.SamplingEvent(None, study_code, date(2017, 10, 14),
                                                    partner_species='PF')
                created = api_instance.create_sampling_event(samp)
                study_detail = study_api.download_study(study_code)
                study_detail.partner_species[0].taxa = [ swagger_client.Taxonomy(taxonomy_id=5833) ]
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

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)


    """
    """
    def test_taxa_on_create(self, api_factory):

        api_instance = api_factory.SamplingEventApi()
        study_api = api_factory.StudyApi()

        try:
            study_code = '1015-MD-UP'

            samp = swagger_client.SamplingEvent(None, study_code, date(2017, 10, 14),
                                                partner_species='PF')
            created = api_instance.create_sampling_event(samp)
            study_detail = study_api.download_study(study_code)
            study_detail.partner_species[0].taxa = [ swagger_client.Taxonomy(taxonomy_id=5833) ]
            study_api.update_study(study_code, study_detail)


            created2 = api_instance.create_sampling_event(samp)

            assert not created2.partner_taxonomies is None, 'Taxonomies missing'
            assert int(created2.partner_taxonomies[0].taxonomy_id) == 5833, 'Wrong Taxonomy'
            api_instance.delete_sampling_event(created.sampling_event_id)
            api_instance.delete_sampling_event(created2.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)


    """
    """
    def test_study_lookup(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:
            study_code = '1020-MD-UP'

            samp = swagger_client.SamplingEvent(None, study_code, date(2017, 10, 14),
                                                partner_species='PF')
            created = api_instance.create_sampling_event(samp)

            fetched = api_instance.download_sampling_events_by_study(study_code)

            assert fetched.count == 1, "Study not found"

            assert created == fetched.sampling_events[0], "create response != download response"

            ffetched = api_instance.download_sampling_events(filter='studyId:' + study_code)

            assert ffetched.count == 1, "Study not found"

            assert ffetched == fetched

            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)


    """
    """
    def test_study_lookup_paged(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        try:
            study_code = '1021-MD-UP'

            for i in range(5):
                samp = swagger_client.SamplingEvent(None, study_code, date(2017, 10, 14),
                                                    partner_species='PF')
                created = api_instance.create_sampling_event(samp)


            fetched1 = api_instance.download_sampling_events_by_study(study_code, start=0, count=2)

            assert len(fetched1.sampling_events) ==2, "Wrong number of sampling_events returned"
            assert fetched1.count == 5, "Wrong total of sampling_events returned"

            ffetched = api_instance.download_sampling_events(filter='studyId:' + study_code,
                                                             start=0, count=2)

            assert ffetched == fetched1

            fetched2 = api_instance.download_sampling_events_by_study(study_code, start=2, count=5)

            #Gets second tranche and also attempts to retrieve more than exist
            assert len(fetched2.sampling_events) ==3, "Wrong number of sampling_events returned"
            assert fetched2.count == 5, "Wrong total of sampling_events returned"

            ids = []
            for sampling_event in fetched1.sampling_events + fetched2.sampling_events:
                assert not sampling_event.sampling_event_id in ids, "SamplingEvent returned twice"
                ids.append(sampling_event.sampling_event_id)

            #Check that it's the correct number of *unique* events

            #Clean up
            fetch_all = api_instance.download_sampling_events_by_study(study_code)

            for sampling_event in fetch_all.sampling_events:
                api_instance.delete_sampling_event(sampling_event.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "SamplingEventApi->create_sampling_event", error)


    """
    """
    def test_event_set_lookup(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        es_api_instance = api_factory.EventSetApi()

        es_name = 'test_event_set_lookup'

        try:
            es_api_instance.create_event_set(es_name)

            study_code = '1022-MD-UP'

            samp = swagger_client.SamplingEvent(None, study_code, date(2017, 10, 14),
                                                partner_species='PF')
            created = api_instance.create_sampling_event(samp)

            es_api_instance.create_event_set_item(es_name, created.sampling_event_id)

            fetched = api_instance.download_sampling_events_by_event_set(es_name)

            assert fetched.count ==1, "event_set not found"

            assert created == fetched.sampling_events[0], "create response != download response"

            ffetched = api_instance.download_sampling_events(filter='eventSet:' + es_name)

            assert ffetched == fetched

            api_instance.delete_sampling_event(created.sampling_event_id)

            es_api_instance.delete_event_set(es_name)
        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetApi->create_event_set", error)


    """
    """
    def test_event_set_lookup_complex_name(self, api_factory):

        api_instance = api_factory.SamplingEventApi()

        es_api_instance = api_factory.EventSetApi()

        es_name = 'test event set lookup'

        try:
            es_api_instance.create_event_set(es_name)

            study_code = '1023-MD-UP'

            samp = swagger_client.SamplingEvent(None, study_code, date(2017, 10, 14),
                                                partner_species='PF')
            created = api_instance.create_sampling_event(samp)

            es_api_instance.create_event_set_item(es_name, created.sampling_event_id)

            fetched = api_instance.download_sampling_events_by_event_set(es_name)

            assert fetched.count ==1, "event_set not found"

            assert created == fetched.sampling_events[0], "create response != download response"
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

        es_name = 'test_event_set_lookup_paged'

        try:
            es_api_instance.create_event_set(es_name)

            for i in range(5):
                samp = swagger_client.SamplingEvent(None, study_code, date(2017, 10, 14),
                                                    partner_species='PF')
                created = api_instance.create_sampling_event(samp)
                es_api_instance.create_event_set_item(es_name, created.sampling_event_id)


            fetched1 = api_instance.download_sampling_events_by_event_set(es_name, start=0, count=2)

            assert len(fetched1.sampling_events) ==2, "Wrong number of sampling_events returned"
            assert fetched1.count == 5, "Wrong total of sampling_events returned"

            ffetched = api_instance.download_sampling_events(filter='eventSet:' + es_name, start=0,
                                                            count=2)

            assert ffetched == fetched1

            fetched2 = api_instance.download_sampling_events_by_event_set(es_name, start=2, count=5)

            #Gets second tranche and also attempts to retrieve more than exist
            assert len(fetched2.sampling_events) ==3, "Wrong number of sampling_events returned"
            assert fetched2.count == 5, "Wrong total of sampling_events returned"

            ids = []
            for sampling_event in fetched1.sampling_events + fetched2.sampling_events:
                assert not sampling_event.sampling_event_id in ids, "SamplingEvent returned twice"
                ids.append(sampling_event.sampling_event_id)

            #Check that it's the correct number of *unique* events

            #Clean up
            fetch_all = api_instance.download_sampling_events_by_event_set(es_name)

            for sampling_event in fetch_all.sampling_events:
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
            samp = swagger_client.SamplingEvent(None, '1023-MD-UP', date(2017, 10, 16))
            samp.attrs = [
                swagger_client.Attr (attr_type='oxford', attr_value='12345678',
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

            samp = swagger_client.SamplingEvent(None, '1009-MD-UP', date(2017, 10, 10),
                                                doc_accuracy='month')
            loc = swagger_client.Location(None, 27.463, 90.495, 'city',
                                          'Trongsa, Trongsa, Bhutan', 'test_create_with_locations', 'BTN')
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

            samp = swagger_client.SamplingEvent(None, '1009-MD-UP', date(2017, 10, 10),
                                                doc_accuracy='month')
            loc = swagger_client.Location(None, 27.463, 90.495, 'city',
                                          'Trongsa, Trongsa, Bhutan', 'test_create_with_locations', 'BTN')
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

            samp = swagger_client.SamplingEvent(None, '1009-MD-UP', date(2017, 10, 10),
                                                doc_accuracy='month')
            loc = swagger_client.Location(None, 27.463, 90.495, 'city',
                                          'Trongsa, Trongsa, Bhutan', 'test_create_with_locations', 'BTN')
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

            samp = swagger_client.SamplingEvent(None, '1009-MD-UP', date(2017, 10, 10),
                                                doc_accuracy='month')
            loc = swagger_client.Location(None, 27.463, 90.495, 'city',
                                          'Trongsa, Trongsa, Bhutan', 'test_create_with_locations', 'BTN')
            loc = location_api_instance.create_location(loc)

            samp.proxy_location_id = loc.location_id

            created = api_instance.create_sampling_event(samp)

            created.proxy_location.accuracy = 'region'

            with pytest.raises(ApiException, status=422):
                created1 = api_instance.update_sampling_event(created.sampling_event_id, created)

            api_instance.delete_sampling_event(created.sampling_event_id)
            location_api_instance.delete_location(loc.location_id)


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

            sampling_event = swagger_client.SamplingEvent(None, '1026-MD-UP', date(2017, 10, 10),
                                                doc_accuracy='month')
            created_se = se_api_instance.create_sampling_event(sampling_event)

            samp = swagger_client.OriginalSample(None, study_name='4024-MD-UP')
            samp.sampling_event_id = created_se.sampling_event_id

            samp.attrs = [
                swagger_client.Attr (attr_type='oxford', attr_value='12345678',
                                           attr_source='upd')
            ]
            created = api_instance.create_original_sample(samp)

            results = se_api_instance.download_sampling_events_by_os_attr('oxford', '12345678')

            assert results.count == 1

            looked_up = results.sampling_events[0]

            fetched = se_api_instance.download_sampling_event(looked_up.sampling_event_id)

            assert created_se == fetched, "create response != download response"

            results1 = se_api_instance.download_sampling_events_by_os_attr('oxford', '12345678',
                                                                           study_name='1026-MD-UP')

            assert results == results1

            with pytest.raises(ApiException, status=404):
                results2 = se_api_instance.download_sampling_events_by_os_attr('oxford', '12345678',
                                                                           study_name='1027-MD-UP')


            se_api_instance.delete_sampling_event(created_se.sampling_event_id)

            api_instance.delete_original_sample(created.original_sample_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)
