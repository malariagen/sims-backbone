import openapi_client
from openapi_client.rest import ApiException
from test_base import TestBase
from datetime import date

import sys
import pytest
import uuid

class TestEventSets(TestBase):


    attr_value = 12345

    def create_sampling_event(self, api_factory):

        os_api_instance = api_factory.OriginalSampleApi()
        api_instance = api_factory.SamplingEventApi()
        study_api = api_factory.StudyApi()

        try:
            study_code = '1010-MD-UP'

            sampling_event = openapi_client.SamplingEvent(None, doc=date(2017, 10, 14))
            self.attr_value = self.attr_value + 1
            sampling_event.attrs = [
                openapi_client.Attr(attr_type='se_oxford',
                                    attr_value=str(self.attr_value),
                                    attr_source='se_taxa_lookup')
            ]
            created_se = api_instance.create_sampling_event(sampling_event)

            samp = openapi_client.OriginalSample(None, study_name=study_code,
                                                 partner_species='PF',
                                                 sampling_event_id=created_se.sampling_event_id)

            samp.attrs = [
                openapi_client.Attr(attr_type='oxford',
                                    attr_value=str(self.attr_value),
                                    attr_source='upd')
            ]
            created_os = os_api_instance.create_original_sample(samp)

            return created_os, created_se

        except ApiException as error:
            self.check_api_exception(api_factory, "TestEventSets->create_sampling_event", error)

    def delete_sampling_event(self, api_factory, original_sample):

        os_api_instance = api_factory.OriginalSampleApi()
        api_instance = api_factory.SamplingEventApi()

        try:
            os_api_instance.delete_original_sample(original_sample.original_sample_id)
            api_instance.delete_sampling_event(original_sample.sampling_event_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "TestEventSets->create_sampling_event", error)

    """
    """
    def test_create_event_set_simple(self, api_factory):

        api_instance = api_factory.EventSetApi()

        try:

            created = api_instance.create_event_set('EventSet1')
            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to create_event_set succeeded')

            assert created.event_set_name == 'EventSet1'

            created = api_instance.delete_event_set('EventSet1')
            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to delete_event_set succeeded')


        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetsApi->create_event_set", error)


    """
    """
    def test_create_member(self, api_factory):

        api_instance = api_factory.EventSetApi()
        event_api_instance = api_factory.SamplingEventApi()

        try:

            event_set = 'EventSet2'
            created = api_instance.create_event_set(event_set)

            os_created, created = self.create_sampling_event(api_factory)

            created_set = api_instance.create_event_set_item(event_set, created.sampling_event_id)
            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to create_event_set_item succeeded')
            fetched_set = api_instance.download_event_set(event_set)

            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to download_event_set succeeded')

            assert fetched_set.members.count == 1
            assert fetched_set.members.sampling_events[0].sampling_event_id == created.sampling_event_id

            api_instance.delete_event_set_item(event_set, created.sampling_event_id)

            fetched_set = api_instance.download_event_set(event_set)

            assert fetched_set.members.count == 0

            self.delete_sampling_event(api_factory, os_created)

            api_instance.delete_event_set(event_set)

        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetsApi->create_event_set", error)

    """
    """
    def test_create_missing_member(self, api_factory):

        api_instance = api_factory.EventSetApi()
        event_api_instance = api_factory.SamplingEventApi()

        try:

            event_set = 'EventSet2'
            created = api_instance.create_event_set(event_set)

            with pytest.raises(ApiException, status=404):
                created_set = api_instance.create_event_set_item('404', str(uuid.uuid4()))

            api_instance.delete_event_set(event_set)

        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetsApi->create_event_set", error)

    """
    """
    def test_create_member_permissions(self, api_factory):

        api_instance = api_factory.EventSetApi()
        event_api_instance = api_factory.SamplingEventApi()

        try:

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    created_set = api_instance.create_event_set_item('404', str(uuid.uuid4()))
            else:
                with pytest.raises(ApiException, status=403):
                    created_set = api_instance.create_event_set_item('404', str(uuid.uuid4()))


        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetsApi->create_event_set", error)
#
#    """
#    """
#    def test_create_member_implicit(self, api_factory):
#
#        api_instance = openapi_client.EventSetApi(api_client)
#        event_api_instance = openapi_client.SamplingEventApi(api_client)
#
#        try:
#
#            event_set = 'EventSet6'
#            created = api_instance.create_event_set(event_set)
#
#            samp = openapi_client.SamplingEvent(None, '4000-MD-UP', doc=date(2017, 10, 10))
#            samp.event_sets = [ event_set ]
#            created = event_api_instance.create_sampling_event(samp)
#
#            fetched_set = api_instance.download_event_set(event_set)
#
#            assert fetched_set.members.sampling_events[0].sampling_event_id == created.sampling_event_id
#
#            api_instance.delete_event_set(event_set)
#            event_api_instance.delete_sampling_event(created.sampling_event_id)
#
#        except ApiException as error:
#            self.check_api_exception(api_factory, "EventSetsApi->create_event_set", error)
#
#    """
#    """
#    def test_update_member_implicit(self, api_factory):
#
#        api_instance = openapi_client.EventSetApi(api_client)
#        event_api_instance = openapi_client.SamplingEventApi(api_client)
#
#        try:
#
#            event_set = 'EventSet7'
#            created = api_instance.create_event_set(event_set)
#
#            samp = openapi_client.SamplingEvent(None, '4000-MD-UP', doc=date(2017, 10, 10))
#            created = event_api_instance.create_sampling_event(samp)
#
#            created.event_sets = [ event_set ]
#
#            updated = event_api_instance.update_sampling_event(created.sampling_event_id, created)
#
#            fetched_set = api_instance.download_event_set(event_set)
#
#            assert fetched_set.members.sampling_events[0].sampling_event_id == created.sampling_event_id
#
#            create.event_sets = None
#
#            updated = event_api_instance.update_sampling_event(created)
#
#            fetched_set = api_instance.download_event_set(event_set)
#
#            assert fetched_set.members is None
#
#            api_instance.delete_event_set(event_set)
#
#            event_api_instance.delete_sampling_event(created.sampling_event_id)
#
#        except ApiException as error:
#            self.check_api_exception(api_factory, "EventSetsApi->create_event_set", error)

    """
    """
    def test_create_note(self, api_factory):

        api_instance = api_factory.EventSetApi()
        event_api_instance = api_factory.SamplingEventApi()

        try:

            event_set = 'EventSet3'
            evsn = openapi_client.EventSetNote('note3', 'note3text')
            evs = openapi_client.EventSet()
            created = api_instance.create_event_set(event_set)

            created_set = api_instance.create_event_set_note(event_set, evsn.note_name, evsn)

            fetched_set = api_instance.download_event_set(event_set)

            assert fetched_set.notes[0].note_name == evsn.note_name

            with pytest.raises(ApiException, status=422):
                created_set = api_instance.create_event_set_note(event_set, evsn.note_name, evsn)


            api_instance.delete_event_set(event_set)

        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetsApi->create_event_set", error)

    """
    """
    def test_update_note(self, api_factory):

        api_instance = api_factory.EventSetApi()
        event_api_instance = api_factory.SamplingEventApi()

        try:

            event_set = 'EventSet4'
            evsn = openapi_client.EventSetNote('note4', 'note4text')
            evs = openapi_client.EventSet()
            created = api_instance.create_event_set(event_set)

            created_set = api_instance.create_event_set_note(event_set, evsn.note_name, evsn)

            fetched_set = api_instance.download_event_set(event_set)

            note = fetched_set.notes[0]

            assert note.note_name == evsn.note_name
            assert note.note_text == evsn.note_text

            assert len(fetched_set.notes) == 1

            new_text = 'updated_note'

            note.note_text = new_text

            api_instance.update_event_set_note(event_set, note.note_name, note)

            fetched_set = api_instance.download_event_set(event_set)

            assert len(fetched_set.notes) == 1

            note = fetched_set.notes[0]

            assert note.note_name == evsn.note_name
            assert note.note_text == new_text

            with pytest.raises(ApiException, status=404):
                api_instance.update_event_set_note(event_set, '404', note)

            #Can't change the name of a note to be the same as another note
            evsna = openapi_client.EventSetNote('note4a', 'note4atext')
            created_set = api_instance.create_event_set_note(event_set, evsna.note_name, evsna)

            with pytest.raises(ApiException, status=422):
                api_instance.update_event_set_note(event_set, evsn.note_name, evsna)


            api_instance.delete_event_set(event_set)

        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetsApi->create_event_set", error)

    """
    """
    def test_delete_note(self, api_factory):

        api_instance = api_factory.EventSetApi()
        event_api_instance = api_factory.SamplingEventApi()

        try:

            event_set = 'EventSet5'
            evsn = openapi_client.EventSetNote('note5', 'note5text')
            evs = openapi_client.EventSet()
            created = api_instance.create_event_set(event_set)

            created_set = api_instance.create_event_set_note(event_set, evsn.note_name, evsn)

            fetched_set = api_instance.download_event_set(event_set)

            note = fetched_set.notes[0]

            assert note.note_name == evsn.note_name
            assert note.note_text == evsn.note_text

            api_instance.delete_event_set_note(event_set, note.note_name)

            fetched_set = api_instance.download_event_set(event_set)

            assert fetched_set.notes is None

            with pytest.raises(ApiException, status=404):
                api_instance.delete_event_set_note(event_set, note.note_name)


            with pytest.raises(ApiException, status=404):
                api_instance.delete_event_set_note('xxxx', note.note_name)


            api_instance.delete_event_set(event_set)

        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetsApi->create_event_set", error)

    """
    """
    def test_event_sets(self, api_factory):

        api_instance = api_factory.EventSetApi()

        try:

            sets = [ 'EventSet6', 'EventSet7' ]

            for evset in sets:
                created = api_instance.create_event_set(evset)
            downloaded = api_instance.download_event_sets()

            assert len(downloaded.event_sets) == 2

            for evset in sets:
                api_instance.delete_event_set(evset)

        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetsApi->create_event_set", error)

    """
    """
    def test_update_event_set(self, api_factory):

        api_instance = api_factory.EventSetApi()
        event_api_instance = api_factory.SamplingEventApi()

        try:

            event_set = 'EventSet8'
            created = api_instance.create_event_set(event_set)

            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 10))
            os_created, created = self.create_sampling_event(api_factory)

            samp2 = openapi_client.SamplingEvent(None, doc=date(2017, 10, 11))
            os_created2, created2 = self.create_sampling_event(api_factory)

            created_set = api_instance.create_event_set_item(event_set, created.sampling_event_id)
            fetched_set1 = api_instance.download_event_set(event_set)

            assert fetched_set1.members.count == 1
            assert fetched_set1.members.sampling_events[0].sampling_event_id == created.sampling_event_id
            assert fetched_set1.notes is None

            evsn = openapi_client.EventSetNote('note8', 'note8text')

            fetched_set1.notes = [evsn]
            fetched_set1.members.sampling_events.append(created2)
            fetched_set1.members.count = 2

            api_instance.update_event_set(event_set, fetched_set1)

            fetched_set2 = api_instance.download_event_set(event_set)

            assert fetched_set2.members.count == 2
            assert len(fetched_set2.notes) == 1

            fetched_set2.members = None

            api_instance.update_event_set(event_set, fetched_set2)

            fetched_set3 = api_instance.download_event_set(event_set)

            assert fetched_set3.members.count == 2
            assert len(fetched_set3.notes) == 1

            api_instance.delete_event_set_item(event_set, created.sampling_event_id)
            api_instance.delete_event_set_item(event_set, created2.sampling_event_id)

            fetched_set = api_instance.download_event_set(event_set)

            assert fetched_set.members.count == 0


            self.delete_sampling_event(api_factory, os_created)
            self.delete_sampling_event(api_factory, os_created2)
            api_instance.delete_event_set(event_set)

        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetsApi->create_event_set", error)

    """
    """
    def test_create_duplicate(self, api_factory):

        api_instance = api_factory.EventSetApi()
        event_api_instance = api_factory.SamplingEventApi()

        try:

            event_set = 'EventSet9'
            evs = openapi_client.EventSet()

            created = api_instance.create_event_set(event_set)

            with pytest.raises(ApiException, status=422):
                created = api_instance.create_event_set(event_set)

            api_instance.delete_event_set(event_set)

        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetsApi->create_event_set", error)

    """
    """
    def test_create_note_duplicate(self, api_factory):

        api_instance = api_factory.EventSetApi()
        event_api_instance = api_factory.SamplingEventApi()

        try:

            event_set = 'EventSet10'
            evsn = openapi_client.EventSetNote('note10', 'note10text')
            evs = openapi_client.EventSet()
            created = api_instance.create_event_set(event_set)

            created_set = api_instance.create_event_set_note(event_set, evsn.note_name, evsn)
            with pytest.raises(ApiException, status=422):
                created_set = api_instance.create_event_set_note(event_set, evsn.note_name, evsn)

            api_instance.delete_event_set(event_set)

        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetsApi->create_event_set", error)

    """
    """
    def test_create_member_duplicate(self, api_factory):

        api_instance = api_factory.EventSetApi()
        event_api_instance = api_factory.SamplingEventApi()

        try:

            event_set = 'EventSet11'
            created = api_instance.create_event_set(event_set)

            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 10))
            os_created, created = self.create_sampling_event(api_factory)

            created_set = api_instance.create_event_set_item(event_set, created.sampling_event_id)

            with pytest.raises(ApiException, status=422):
                created_set = api_instance.create_event_set_item(event_set, created.sampling_event_id)

            api_instance.delete_event_set_item(event_set, created.sampling_event_id)

            self.delete_sampling_event(api_factory, os_created)
            api_instance.delete_event_set(event_set)

        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetsApi->create_event_set", error)

    """
    """
    def test_delete_missing_member(self, api_factory):

        api_instance = api_factory.EventSetApi()
        event_api_instance = api_factory.SamplingEventApi()

        try:

            event_set = 'EventSet12'
            created = api_instance.create_event_set(event_set)

            samp = openapi_client.SamplingEvent(None, doc=date(2017, 10, 10))
            os_created, created = self.create_sampling_event(api_factory)

            created_set = api_instance.create_event_set_item(event_set, created.sampling_event_id)

            api_instance.delete_event_set_item(event_set, created.sampling_event_id)

            with pytest.raises(ApiException, status=404):
                api_instance.delete_event_set_item(event_set, created.sampling_event_id)

            self.delete_sampling_event(api_factory, os_created)
            api_instance.delete_event_set(event_set)

        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetsApi->create_event_set", error)

    """
    """
    def test_create_note_missing_event_set(self, api_factory):

        api_instance = api_factory.EventSetApi()
        event_api_instance = api_factory.SamplingEventApi()

        try:

            evsn = openapi_client.EventSetNote('note404', 'note404text')

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    created_set = api_instance.create_event_set_note('404', evsn.note_name, evsn)
            else:
                with pytest.raises(ApiException, status=403):
                    created_set = api_instance.create_event_set_note('404', evsn.note_name, evsn)

        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetsApi->create_event_set_note", error)


    """
    """
    def test_download_missing(self, api_factory):

        api_instance = api_factory.EventSetApi()

        try:

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    api_instance.download_event_set('404')
            else:
                with pytest.raises(ApiException, status=403):
                    api_instance.download_event_set('404')

        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetsApi->download_event_set", error)

    """
    """
    def test_update_missing(self, api_factory):

        api_instance = api_factory.EventSetApi()

        try:

            event_set = openapi_client.EventSet('404')

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    api_instance.update_event_set('404',event_set)
            else:
                with pytest.raises(ApiException, status=403):
                    api_instance.update_event_set('404',event_set)

        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetsApi->update_event_set", error)


    """
    """
    def test_delete_missing(self, api_factory):

        api_instance = api_factory.EventSetApi()

        try:


            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    api_instance.delete_event_set('404')
            else:
                with pytest.raises(ApiException, status=403):
                    api_instance.delete_event_set('404')

        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetsApi->delete_event_set", error)

    """
    """
    def test_delete_item_permission(self, api_factory):

        api_instance = api_factory.EventSetApi()

        try:


            if not api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=403):
                    api_instance.delete_event_set_item('404', str(uuid.uuid4()))

        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetsApi->delete_event_set_item", error)

    """
    """
    def test_delete_note_permission(self, api_factory):

        api_instance = api_factory.EventSetApi()

        try:


            if not api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=403):
                    api_instance.delete_event_set_note('404', '404 note')

        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetsApi->delete_event_set_note", error)


    """
    """
    def test_update_note_permission(self, api_factory):

        api_instance = api_factory.EventSetApi()

        try:


            if not api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=403):
                    api_instance.update_event_set_note('404', '404 note', {})

        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetsApi->update_event_set_note", error)

    """
    """
    def test_download_permission(self, api_factory):

        api_instance = api_factory.EventSetApi()

        try:


            if not api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=403):
                    api_instance.download_event_sets()

        except ApiException as error:
            self.check_api_exception(api_factory, "EventSetsApi->download_event_sets", error)

