import swagger_client
from swagger_client.rest import ApiException
from test_base import TestBase
from datetime import date
import urllib

import uuid

class TestSample(TestBase):


    """
    """
    def test_create(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:

            samp = swagger_client.SamplingEvent(None, '1000-MD-UP', date(2017, 10, 10),
                                                doc_accuracy = 'month')
            created = api_instance.create_sampling_event(samp)
            fetched = api_instance.download_sampling_event(created.sampling_event_id)
            self.assertEqual(created, fetched, "create response != download response")
            fetched.sampling_event_id = None
            self.assertEqual(samp, fetched, "upload != download response")
            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.fail("test_create: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)

    """
    """
    def test_delete(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:

            samp = swagger_client.SamplingEvent(None, '1001-MD-UP', date(2017, 10, 11))
            created = api_instance.create_sampling_event(samp)
            api_instance.delete_sampling_event(created.sampling_event_id)
            with self.assertRaises(Exception) as context:
                fetched = api_instance.download_sampling_event(created.sampling_event_id)
            self.assertEqual(context.exception.status, 404)

        except ApiException as error:
            self.fail("test_delete: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)


    """
    """
    def test_delete_missing(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:

            with self.assertRaises(Exception) as context:
                api_instance.delete_sampling_event(str(uuid.uuid4()))
            self.assertEqual(context.exception.status, 404)

        except ApiException as error:
            self.fail("test_delete_missing: Exception when calling SamplingEventApi->delete_sampling_event: %s\n" % error)

    """
    """
    def test_duplicate_key(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:

            samp = swagger_client.SamplingEvent(None, '1002-MD-UP', date(2017, 10, 12))
            samp.identifiers = [
                swagger_client.Identifier (identifier_type='oxford', identifier_value='1234',
                                           identifier_source='same')
            ]
            created = api_instance.create_sampling_event(samp)

            with self.assertRaises(Exception) as context:
                created = api_instance.create_sampling_event(samp)

            self.assertEqual(context.exception.status, 422)

            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.fail("test_duplicate_key: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)

    """
    """
    def test_duplicate_partner_key(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:

            samp = swagger_client.SamplingEvent(None, '1003-MD-UP', date(2017, 10, 13))
            samp.identifiers = [
                swagger_client.Identifier (identifier_type='partner_id', identifier_value='12345')
            ]
            created = api_instance.create_sampling_event(samp)

            created1 = api_instance.create_sampling_event(samp)


            api_instance.delete_sampling_event(created.sampling_event_id)
            api_instance.delete_sampling_event(created1.sampling_event_id)

            self.assertNotEqual(created.sampling_event_id, created1.sampling_event_id)

        except ApiException as error:
            self.fail("test_duplicate_key: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)


    """
    """
    def test_identifier_lookup(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:

            samp = swagger_client.SamplingEvent(None, '1004-MD-UP', date(2017, 10, 14))
            samp.identifiers = [
                swagger_client.Identifier (identifier_type='oxford', identifier_value='123456')
            ]
            created = api_instance.create_sampling_event(samp)
            looked_up = api_instance.download_sampling_event_by_identifier('oxford', '123456')

            fetched = api_instance.download_sampling_event(looked_up.sampling_event_id)

            self.assertEqual(created, fetched, "create response != download response")
            fetched.sampling_event_id = None
            self.assertEqual(samp, fetched, "upload != download response")
            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.fail("test_identifier_lookup: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)

    """
    """
    def test_identifier_merge(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:

            ident1 = swagger_client.Identifier (identifier_type='oxford_id', identifier_value='1234')
            ident2 = swagger_client.Identifier (identifier_type='roma_id', identifier_value='12345')
            ident3 = swagger_client.Identifier (identifier_type='lims_id', identifier_value='123456')
            samp1 = swagger_client.SamplingEvent(None, '1022-MD-UP', date(2017, 10, 14))
            samp1.identifiers = [
                ident1
            ]
            created1 = api_instance.create_sampling_event(samp1)

            samp2 = swagger_client.SamplingEvent(None, '1022-MD-UP', date(2017, 10, 14))
            samp2.identifiers = [
                ident2
            ]
            created2 = api_instance.create_sampling_event(samp2)


            samp3 = swagger_client.SamplingEvent(None, '1022-MD-UP', date(2017, 10, 14))
            samp3.identifiers = [
                ident1,
                ident2,
                ident3
            ]
            with self.assertRaises(Exception) as context:
                created3 = api_instance.create_sampling_event(samp3)

            self.assertEqual(context.exception.status, 422)

            api_instance.delete_sampling_event(created1.sampling_event_id)
            api_instance.delete_sampling_event(created2.sampling_event_id)


        except ApiException as error:
            self.fail("test_identifier_merge: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)

    """
    """
    def test_update(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:

            samp = swagger_client.SamplingEvent(None, '1005-MD-UP', date(2017, 10, 15))
            samp.identifiers = [
                swagger_client.Identifier (identifier_type='oxford', identifier_value='1234567')
            ]
            created = api_instance.create_sampling_event(samp)
            looked_up = api_instance.download_sampling_event_by_identifier('oxford', '1234567')
            new_samp = swagger_client.SamplingEvent(None, '0001-MD-UP', date(2018, 11, 11))
            updated = api_instance.update_sampling_event(looked_up.sampling_event_id, new_samp)
            fetched = api_instance.download_sampling_event(looked_up.sampling_event_id)
            self.assertEqual(updated, fetched, "update response != download response")
            fetched.sampling_event_id = None
            self.assertEqual(new_samp, fetched, "update != download response")
            api_instance.delete_sampling_event(looked_up.sampling_event_id)

        except ApiException as error:
            self.fail("test_update: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)

    """
    """
    def test_update_duplicate(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:

            samp = swagger_client.SamplingEvent(None, '1006-MD-UP', date(2017, 10, 16))
            samp.identifiers = [
                swagger_client.Identifier (identifier_type='oxford', identifier_value='12345678',
                                           identifier_source='upd')
            ]
            created = api_instance.create_sampling_event(samp)
            looked_up = api_instance.download_sampling_event_by_identifier('oxford', '12345678')
            new_samp = swagger_client.SamplingEvent(None, '0001-MD-UP', date(2018, 10, 10))
            new_samp.identifiers = [
                swagger_client.Identifier (identifier_type='oxford', identifier_value='123456789',
                                          identifier_source='upd')
            ]
            new_created = api_instance.create_sampling_event(new_samp)
            with self.assertRaises(Exception) as context:
                updated = api_instance.update_sampling_event(looked_up.sampling_event_id, new_samp)

            self.assertEqual(context.exception.status, 422)

            api_instance.delete_sampling_event(looked_up.sampling_event_id)
            api_instance.delete_sampling_event(new_created.sampling_event_id)

        except ApiException as error:
            self.fail("test_update_duplicate: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)

    """
    """
    def test_update_missing(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:

            new_samp = swagger_client.SamplingEvent(None, '1007-MD-UP', date(2018, 11, 17))
            fake_id = uuid.uuid4()
            new_samp.sampling_event_id = str(fake_id)
            with self.assertRaises(Exception) as context:
                updated = api_instance.update_sampling_event(new_samp.sampling_event_id, new_samp)

            self.assertEqual(context.exception.status, 404)


        except ApiException as error:
            self.fail("test_update_missing: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)

    """
    """
    def test_identifier_lookup_encode(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:

            test_id = 'MDG/DK_0005'
            samp = swagger_client.SamplingEvent(None, '1008-MD-UP', date(2017, 10, 14))
            samp.identifiers = [
                swagger_client.Identifier (identifier_type='partner_id', identifier_value=test_id,
                                          identifier_source='encode')
            ]
            created = api_instance.create_sampling_event(samp)

            fetched = api_instance.download_sampling_event(created.sampling_event_id)

            self.assertEqual(created, fetched, "create response != download response")
            fetched.sampling_event_id = None
            self.assertEqual(samp, fetched, "upload != download response")

            looked_up = api_instance.download_sampling_event_by_identifier('partner_id',
                                                                           urllib.parse.quote_plus(test_id))
            fetched = api_instance.download_sampling_event(looked_up.sampling_event_id)

            self.assertEqual(created, fetched, "create response != download response")
            fetched.sampling_event_id = None
            self.assertEqual(samp, fetched, "upload != download response")


            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.fail("test_partner_lookup_encode: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)

    """
    """
    def test_create_with_locations(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)
        location_api_instance = swagger_client.LocationApi(self._api_client)

        try:

            samp = swagger_client.SamplingEvent(None, '1009-MD-UP', date(2017, 10, 10),
                                                doc_accuracy='month')
            loc = swagger_client.Location(None, 27.463, 90.495, 'city',
                                          'Trongsa, Trongsa, Bhutan', 'test_create_with_locations', 'BTN')
            loc = location_api_instance.create_location(loc)

            samp.location_id = loc.location_id
            created = api_instance.create_sampling_event(samp)
            fetched = api_instance.download_sampling_event(created.sampling_event_id)
            self.assertEqual(samp.location_id, fetched.location_id, "upload location != download response")
            self.assertEqual(samp.location_id, fetched.public_location_id, "upload public_location != proxy download response")

            proxy_loc = swagger_client.Location(None, 27.4, 90.4, 'region',
                                          'Trongsa, Bhutan', 'test_create_with_locations', 'BTN')
            proxy_loc = location_api_instance.create_location(proxy_loc)
            samp.proxy_location_id = proxy_loc.location_id
            fetched = api_instance.update_sampling_event(fetched.sampling_event_id, samp)
            self.assertEqual(samp.location_id, fetched.location_id, "upload location != download response")
            self.assertEqual(samp.proxy_location_id, fetched.proxy_location_id, "upload proxy_location != download response")
            self.assertEqual(samp.proxy_location_id, fetched.public_location_id, "upload public_location != proxy download response")
            api_instance.delete_sampling_event(created.sampling_event_id)
            location_api_instance.delete_location(loc.location_id)
            location_api_instance.delete_location(proxy_loc.location_id)


        except ApiException as error:
            self.fail("test_create: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)

    """
    """
    def test_taxa_lookup(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)
        study_api = swagger_client.StudyApi(self._api_client)

        try:
            study_code = '1010-MD-UP'

            samp = swagger_client.SamplingEvent(None, study_code, date(2017, 10, 14),
                                                partner_species='PF')
            created = api_instance.create_sampling_event(samp)
            study_detail = study_api.download_study(study_code)
            study_detail.partner_species[0].taxa = [ swagger_client.Taxonomy(taxonomy_id=5833) ]
            study_api.update_study(study_code, study_detail)

            fetched = api_instance.download_sampling_events_by_taxa(5833)

            self.assertEqual(fetched.count,1, "Taxa not found")

            self.assertIsNotNone(fetched.sampling_events[0].partner_taxonomies,
                                 'Taxonomies missing')
            self.assertEqual(int(fetched.sampling_events[0].partner_taxonomies[0].taxonomy_id), 5833,
                              'Wrong Taxonomy')
            #As the taxonomy wasn't set when created was created it won't be in the response
            #separate test for this
            fetched.sampling_events[0].partner_taxonomies = None
            self.assertEqual(created, fetched.sampling_events[0], "create response != download response")
            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.fail("test_partner_lookup: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)


    """
    """
    def test_taxa_lookup_paged(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)
        study_api = swagger_client.StudyApi(self._api_client)

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

            self.assertEqual(len(fetched1.sampling_events),2, "Wrong number of sampling_events returned")
            self.assertEqual(fetched1.count, len(study_codes), "Wrong total of sampling_events returned")

            fetched2 = api_instance.download_sampling_events_by_taxa(5833, start=2, count=5)

            #Gets second tranche and also attempts to retrieve more than exist
            self.assertEqual(len(fetched2.sampling_events),3, "Wrong number of sampling_events returned")
            self.assertEqual(fetched2.count, len(study_codes), "Wrong total of sampling_events returned")

            ids = []
            for sampling_event in fetched1.sampling_events + fetched2.sampling_events:
                self.assertNotIn(sampling_event.sampling_event_id, ids, "SamplingEvent returned twice")
                ids.append(sampling_event.sampling_event_id)

            #Check that it's the correct number of *unique* events

            #Clean up
            fetch_all = api_instance.download_sampling_events_by_taxa(5833)

            for sampling_event in fetch_all.sampling_events:
                api_instance.delete_sampling_event(sampling_event.sampling_event_id)

        except ApiException as error:
            self.fail("test_partner_lookup: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)


    """
    """
    def test_taxa_on_create(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)
        study_api = swagger_client.StudyApi(self._api_client)

        try:
            study_code = '1015-MD-UP'

            samp = swagger_client.SamplingEvent(None, study_code, date(2017, 10, 14),
                                                partner_species='PF')
            created = api_instance.create_sampling_event(samp)
            study_detail = study_api.download_study(study_code)
            study_detail.partner_species[0].taxa = [ swagger_client.Taxonomy(taxonomy_id=5833) ]
            study_api.update_study(study_code, study_detail)


            created2 = api_instance.create_sampling_event(samp)

            self.assertIsNotNone(created2.partner_taxonomies,
                                 'Taxonomies missing')
            self.assertEqual(int(created2.partner_taxonomies[0].taxonomy_id), 5833,
                              'Wrong Taxonomy')
            api_instance.delete_sampling_event(created.sampling_event_id)
            api_instance.delete_sampling_event(created2.sampling_event_id)

        except ApiException as error:
            self.fail("test_partner_lookup: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)


    """
    """
    def test_study_lookup(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:
            study_code = '1020-MD-UP'

            samp = swagger_client.SamplingEvent(None, study_code, date(2017, 10, 14),
                                                partner_species='PF')
            created = api_instance.create_sampling_event(samp)

            fetched = api_instance.download_sampling_events_by_study(study_code)

            self.assertEqual(fetched.count,1, "Study not found")

            self.assertEqual(created, fetched.sampling_events[0], "create response != download response")
            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.fail("test_partner_lookup: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)


    """
    """
    def test_study_lookup_paged(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:
            study_code = '1021-MD-UP'

            for i in range(5):
                samp = swagger_client.SamplingEvent(None, study_code, date(2017, 10, 14),
                                                    partner_species='PF')
                created = api_instance.create_sampling_event(samp)


            fetched1 = api_instance.download_sampling_events_by_study(study_code, start=0, count=2)

            self.assertEqual(len(fetched1.sampling_events),2, "Wrong number of sampling_events returned")
            self.assertEqual(fetched1.count, 5, "Wrong total of sampling_events returned")

            fetched2 = api_instance.download_sampling_events_by_study(study_code, start=2, count=5)

            #Gets second tranche and also attempts to retrieve more than exist
            self.assertEqual(len(fetched2.sampling_events),3, "Wrong number of sampling_events returned")
            self.assertEqual(fetched2.count, 5, "Wrong total of sampling_events returned")

            ids = []
            for sampling_event in fetched1.sampling_events + fetched2.sampling_events:
                self.assertNotIn(sampling_event.sampling_event_id, ids, "SamplingEvent returned twice")
                ids.append(sampling_event.sampling_event_id)

            #Check that it's the correct number of *unique* events

            #Clean up
            fetch_all = api_instance.download_sampling_events_by_study(study_code)

            for sampling_event in fetch_all.sampling_events:
                api_instance.delete_sampling_event(sampling_event.sampling_event_id)

        except ApiException as error:
            self.fail("test_partner_lookup: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)


    """
    """
    def test_event_set_lookup(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        es_api_instance = swagger_client.EventSetApi(self._api_client)

        es_name = 'test_event_set_lookup'

        try:
            es_api_instance.create_event_set(es_name)

            study_code = '1020-MD-UP'

            samp = swagger_client.SamplingEvent(None, study_code, date(2017, 10, 14),
                                                partner_species='PF')
            created = api_instance.create_sampling_event(samp)

            es_api_instance.create_event_set_item(es_name, created.sampling_event_id)

            fetched = api_instance.download_sampling_events_by_event_set(es_name)

            self.assertEqual(fetched.count,1, "event_set not found")

            self.assertEqual(created, fetched.sampling_events[0], "create response != download response")
            api_instance.delete_sampling_event(created.sampling_event_id)

            es_api_instance.delete_event_set(es_name)
        except ApiException as error:
            self.fail("test_partner_lookup: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)


    """
    """
    def test_event_set_lookup_paged(self):

        study_code = '1021-MD-UP'

        api_instance = swagger_client.SamplingEventApi(self._api_client)
        study_api = swagger_client.StudyApi(self._api_client)

        es_api_instance = swagger_client.EventSetApi(self._api_client)

        es_name = 'test_event_set_lookup_paged'

        try:
            es_api_instance.create_event_set(es_name)

            for i in range(5):
                samp = swagger_client.SamplingEvent(None, study_code, date(2017, 10, 14),
                                                    partner_species='PF')
                created = api_instance.create_sampling_event(samp)
                es_api_instance.create_event_set_item(es_name, created.sampling_event_id)


            fetched1 = api_instance.download_sampling_events_by_event_set(es_name, start=0, count=2)

            self.assertEqual(len(fetched1.sampling_events),2, "Wrong number of sampling_events returned")
            self.assertEqual(fetched1.count, 5, "Wrong total of sampling_events returned")

            fetched2 = api_instance.download_sampling_events_by_event_set(es_name, start=2, count=5)

            #Gets second tranche and also attempts to retrieve more than exist
            self.assertEqual(len(fetched2.sampling_events),3, "Wrong number of sampling_events returned")
            self.assertEqual(fetched2.count, 5, "Wrong total of sampling_events returned")

            ids = []
            for sampling_event in fetched1.sampling_events + fetched2.sampling_events:
                self.assertNotIn(sampling_event.sampling_event_id, ids, "SamplingEvent returned twice")
                ids.append(sampling_event.sampling_event_id)

            #Check that it's the correct number of *unique* events

            #Clean up
            fetch_all = api_instance.download_sampling_events_by_event_set(es_name)

            for sampling_event in fetch_all.sampling_events:
                api_instance.delete_sampling_event(sampling_event.sampling_event_id)

            es_api_instance.delete_event_set(es_name)

        except ApiException as error:
            self.fail("test_partner_lookup: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)

