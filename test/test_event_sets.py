import swagger_client
from swagger_client.rest import ApiException
from test_base import TestBase
from datetime import date
from api_factory import ApiFactory

class TestEventSets(TestBase):


    """
    """
    def test_create_event_set_simple(self):

        api_instance = ApiFactory.EventSetApi(self._api_client)

        try:

            created = api_instance.create_event_set('EventSet1')

            self.assertEqual(created.event_set_name, 'EventSet1')

            created = api_instance.delete_event_set('EventSet1')

        except ApiException as error:
            self.fail("test_create: Exception when calling EventSetsApi->create_event_set: %s\n" % error)

    """
    """
    def test_create_member(self):

        api_instance = ApiFactory.EventSetApi(self._api_client)
        event_api_instance = ApiFactory.SamplingEventApi(self._api_client)

        try:

            event_set = 'EventSet2'
            created = api_instance.create_event_set(event_set)

            samp = swagger_client.SamplingEvent(None, '4000-MD-UP', date(2017, 10, 10))
            created = event_api_instance.create_sampling_event(samp)

            created_set = api_instance.create_event_set_item(event_set, created.sampling_event_id)
            fetched_set = api_instance.download_event_set(event_set)

            self.assertEqual(fetched_set.members.sampling_events[0].sampling_event_id, created.sampling_event_id)

            api_instance.delete_event_set(event_set)
            event_api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.fail("test_create: Exception when calling EventSetsApi->create_event_set: %s\n" % error)
#
#    """
#    """
#    def test_create_member_implicit(self):
#
#        api_instance = swagger_client.EventSetApi(self._api_client)
#        event_api_instance = swagger_client.SamplingEventApi(self._api_client)
#
#        try:
#
#            event_set = 'EventSet6'
#            created = api_instance.create_event_set(event_set)
#
#            samp = swagger_client.SamplingEvent(None, '4000-MD-UP', date(2017, 10, 10))
#            samp.event_sets = [ event_set ]
#            created = event_api_instance.create_sampling_event(samp)
#
#            fetched_set = api_instance.download_event_set(event_set)
#
#            self.assertEqual(fetched_set.members.sampling_events[0].sampling_event_id, created.sampling_event_id)
#
#            api_instance.delete_event_set(event_set)
#            event_api_instance.delete_sampling_event(created.sampling_event_id)
#
#        except ApiException as error:
#            self.fail("test_create_member: Exception when calling EventSetsApi->create_event_set: %s\n" % error)
#
#    """
#    """
#    def test_update_member_implicit(self):
#
#        api_instance = swagger_client.EventSetApi(self._api_client)
#        event_api_instance = swagger_client.SamplingEventApi(self._api_client)
#
#        try:
#
#            event_set = 'EventSet7'
#            created = api_instance.create_event_set(event_set)
#
#            samp = swagger_client.SamplingEvent(None, '4000-MD-UP', date(2017, 10, 10))
#            created = event_api_instance.create_sampling_event(samp)
#
#            created.event_sets = [ event_set ]
#
#            updated = event_api_instance.update_sampling_event(created.sampling_event_id, created)
#
#            fetched_set = api_instance.download_event_set(event_set)
#
#            self.assertEqual(fetched_set.members.sampling_events[0].sampling_event_id, created.sampling_event_id)
#
#            create.event_sets = None
#
#            updated = event_api_instance.update_sampling_event(created)
#
#            fetched_set = api_instance.download_event_set(event_set)
#
#            self.assertIsNone(fetched_set.members)
#
#            api_instance.delete_event_set(event_set)
#
#            event_api_instance.delete_sampling_event(created.sampling_event_id)
#
#        except ApiException as error:
#            self.fail("test_update_member: Exception when calling EventSetsApi->create_event_set: %s\n" % error)

    """
    """
    def test_create_note(self):

        api_instance = ApiFactory.EventSetApi(self._api_client)
        event_api_instance = ApiFactory.SamplingEventApi(self._api_client)

        try:

            event_set = 'EventSet3'
            evsn = swagger_client.EventSetNote('note3', 'note3text')
            evs = swagger_client.EventSet()
            created = api_instance.create_event_set(event_set)

            created_set = api_instance.create_event_set_note(event_set, evsn.note_name, evsn)

            fetched_set = api_instance.download_event_set(event_set)

            self.assertEqual(fetched_set.notes[0].note_name, evsn.note_name)
            
            api_instance.delete_event_set(event_set)

        except ApiException as error:
            self.fail("test_create: Exception when calling EventSetsApi->create_event_set: %s\n" % error)

    """
    """
    def test_event_sets(self):

        api_instance = ApiFactory.EventSetApi(self._api_client)

        try:

            sets = [ 'EventSet4', 'EventSet5' ]

            for evset in sets:
                created = api_instance.create_event_set(evset)
            downloaded = api_instance.download_event_sets()

            self.assertEqual(len(downloaded.event_sets), 2)

            for evset in sets:
                api_instance.delete_event_set(evset)

        except ApiException as error:
            self.fail("test_create: Exception when calling EventSetsApi->create_event_set: %s\n" % error)

