import logging

from openapi_server.models.event_set import EventSet
from openapi_server.models.event_set_note import EventSetNote

from backbone_server.controllers.event_set_controller import EventSetController

from local.base_local_api import BaseLocalApi


class LocalEventSetApi(BaseLocalApi):

    def __init__(self, api_client, user, auths, method):

        super().__init__(api_client, user, auths, method)

        self.event_set_controller = EventSetController()

    def create_event_set(self, event_set_id, studies=None):
        """
        creates an eventSet

        :param event_set:
        :type event_set: dict | bytes

        :rtype: EventSet
        """
        (ret, retcode) = self.event_set_controller.create_event_set(event_set_id, studies=studies,
                                                                    user=self._user,
                                                                    auths=self.event_set_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'EventSet')

    def create_event_set_item(self, event_set_id, sampling_event_id,
                              studies=None):
        """
        Adds a samplingEvent to an eventSet

        :param event_set_id: ID of eventSet to modify
        :type event_set_id: str
        :param sampling_event_id: ID of samplingEvent to add to the set
        :type sampling_event_id: str

        :rtype: EventSet
        """
        (ret, retcode) = self.event_set_controller.create_event_set_item(event_set_id,
                                                                         sampling_event_id,
                                                                         studies=studies,
                                                                         user=self._user,
                                                                         auths=self.event_set_controller.token_info(self.auth_tokens()))
        return self.create_response(ret, retcode, 'EventSet')

    def create_event_set_note(self, event_set_id, note_id, note, studies=None):
        """
        Adds a note to an eventSet

        :param event_set_id: ID of eventSet to modify
        :type event_set_id: str
        :param note_id: ID of note to modify in the set
        :type note_id: str
        :param note:
        :type note: dict | bytes

        :rtype: None
        """
        (ret, retcode) = self.event_set_controller.create_event_set_note(event_set_id, note_id,
                                                                         note, studies=studies,
                                                                         user=self._user,
                                                                         auths=self.event_set_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode)

    def delete_event_set(self, event_set_id, studies=None):
        """
        deletes an eventSet

        :param eventSetId: ID of eventSet to delete
        :type eventSetId: str

        :rtype: None
        """
        (ret, retcode) = self.event_set_controller.delete_event_set(
            event_set_id, studies=studies,
            user=self._user, auths=self.event_set_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode)

    def delete_event_set_item(self, event_set_id, sampling_event_id,
                              studies=None):
        """
        deletes a samplingEvent from an eventSet

        :param eventSetId: ID of eventSet to modify
        :type eventSetId: str
        :param samplingEventId: ID of samplingEvent to remove from the set
        :type samplingEventId: str

        :rtype: None
        """
        (ret, retcode) = self.event_set_controller.delete_event_set_item(event_set_id,
                                                                         sampling_event_id,
                                                                         studies=studies,
                                                                         user=self._user,
                                                                         auths=self.event_set_controller.token_info(self.auth_tokens()))
        return self.create_response(ret, retcode)

    def delete_event_set_note(self, event_set_id, note_id, studies=None):
        """
        deletes an eventSet note

        :param event_set_id: ID of eventSet to modify
        :type event_set_id: str
        :param note_id: ID of note to remove from the set
        :type note_id: str

        :rtype: None
        """
        (ret, retcode) = self.event_set_controller.delete_event_set_note(event_set_id, note_id,
                                                                         studies=studies,
                                                                         user=self._user,
                                                                         auths=self.event_set_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode)

    def download_event_set(self, event_set_id, studies=None, start=None, count=None):
        """
        fetches an eventSet

        :param eventSetId: ID of eventSet to fetch
        :type eventSetId: str

        :rtype: EventSet
        """
        (ret, retcode) = self.event_set_controller.download_event_set(event_set_id, start=start,
                                                                      count=count, studies=studies,
                                                                      user=self._user,
                                                                      auths=self.event_set_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'EventSet')

    def download_event_sets(self, studies=None):
        """
        fetches eventSets


        :rtype: EventSets
        """
        (ret, retcode) = self.event_set_controller.download_event_sets(studies=studies,
                                                                       user=self._user,
                                                                       auths=self.event_set_controller.token_info(self.auth_tokens()))
        return self.create_response(ret, retcode, 'EventSets')

    def update_event_set(self, event_set_id, event_set, studies=None):
        """
        updates an eventSet

        :param event_set_id: ID of eventSet to update
        :type event_set_id: str
        :param event_set:
        :type event_set: dict | bytes

        :rtype: EventSet
        """
        (ret, retcode) = self.event_set_controller.update_event_set(event_set_id, event_set,
                                                                    studies=studies,
                                                                    user=self._user,
                                                                    auths=self.event_set_controller.token_info(self.auth_tokens()))
        return self.create_response(ret, retcode, 'EventSet')

    def update_event_set_note(self, event_set_id, note_id, note, studies=None):
        """
        Adds a note to an eventSet

        :param event_set_id: ID of eventSet to modify
        :type event_set_id: str
        :param note_id: ID of note to modify in the set
        :type note_id: str
        :param note:
        :type note: dict | bytes

        :rtype: None
        """

        (ret, retcode) = self.event_set_controller.update_event_set_note(event_set_id, note_id,
                                                                         note, studies=studies,
                                                                         user=self._user,
                                                                         auths=self.event_set_controller.token_info(self.auth_tokens()))
        return self.create_response(ret, retcode)
