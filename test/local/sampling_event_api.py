import logging

from openapi_server.models.sampling_event import SamplingEvent  # noqa: E501
from openapi_server.models.sampling_events import SamplingEvents  # noqa: E501
from openapi_server import util


from backbone_server.controllers.sampling_event_controller import SamplingEventController

from local.base_local_api import BaseLocalApi


class LocalSamplingEventApi(BaseLocalApi):

    def __init__(self, api_client, user, auths, method):

        super().__init__(api_client, user, auths, method)

        self.sampling_event_controller = SamplingEventController()

    def create_sampling_event(self, sampling_event, studies=None):
        """
        create_sampling_event
        Create a samplingEvent
        :param sampling_event:
        :type sampling_event: dict | bytes

        :rtype: SamplingEvent
        """

        (ret, retcode) = self.sampling_event_controller.create_sampling_event(sampling_event, studies=studies, user=self._user,
                                                                              auths=self.sampling_event_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'SamplingEvent')

    def delete_sampling_event(self, sampling_event_id, studies=None):
        """
        deletes an samplingEvent

        :param sampling_event_id: ID of samplingEvent to fetch
        :type sampling_event_id: str

        :rtype: None
        """
        (ret, retcode) = self.sampling_event_controller.delete_sampling_event(sampling_event_id, studies=studies, user=self._user,
                                                                              auths=self.sampling_event_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode)

    def download_sampling_event(self, sampling_event_id, studies=None):
        """
        fetches an samplingEvent

        :param samplingEventId: ID of samplingEvent to fetch
        :type samplingEventId: str

        :rtype: SamplingEvent
        """
        (ret, retcode) = self.sampling_event_controller.download_sampling_event(sampling_event_id, studies=studies, user=self._user,
                                                                                auths=self.sampling_event_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'SamplingEvent')

    def download_sampling_events(self, search_filter=None, value_type=None, start=None, count=None, studies=None):
        """
        fetches an samplingEvent

        :param samplingEventId: ID of samplingEvent to fetch
        :type samplingEventId: str

        :rtype: SamplingEvent
        """
        (ret, retcode) = self.sampling_event_controller.download_sampling_events(search_filter,
                                                                                 value_type=value_type,
                                                                                 start=start,
                                                                                 count=count, studies=studies, user=self._user,
                                                                                 auths=self.sampling_event_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'SamplingEvents')

    def download_sampling_events_by_event_set(self, event_set_id, studies=None, start=None, count=None):
        """
        fetches samplingEvents in a given event set

        :param event_set_id: Event Set name
        :type event_set_id: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: SamplingEvents
        """
        (ret, retcode) = self.sampling_event_controller.download_sampling_events_by_event_set(event_set_id, start=start,
                                                                                              count=count, studies=studies, user=self._user,
                                                                                              auths=self.sampling_event_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'SamplingEvents')

    def download_sampling_events_by_attr(self, prop_name, prop_value,
                                         study_name=None, value_type=None,
                                         start=None, count=None, studies=None):
        """
        fetches a samplingEvent by property value

        :param prop_name: name of property to search
        :type prop_name: str
        :param prop_value: matching value of property to search
        :type prop_value: str

        :rtype: SamplingEvents
        """
        (ret, retcode) = self.sampling_event_controller.download_sampling_events_by_attr(prop_name, prop_value,
                                                                                         study_name,
                                                                                         value_type=value_type,
                                                                                         start=start,
                                                                                         count=count,
                                                                                         studies=studies, user=self._user,
                                                                                         auths=self.sampling_event_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'SamplingEvents')

    def download_sampling_events_by_os_attr(self, prop_name, prop_value,
                                            study_name=None,
                                            value_type=None, start=None,
                                            count=None, studies=None):
        """
        fetches a samplingEvent by property value

        :param prop_name: name of property to search
        :type prop_name: str
        :param prop_value: matching value of property to search
        :type prop_value: str

        :rtype: SamplingEvents
        """
        (ret, retcode) = self.sampling_event_controller.download_sampling_events_by_os_attr(prop_name, prop_value,
                                                                                            study_name,
                                                                                            value_type=value_type,
                                                                                            start=start,
                                                                                            count=count,
                                                                                            studies=studies, user=self._user,
                                                                                            auths=self.sampling_event_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'SamplingEvents')

    def download_sampling_events_by_location(self, location_id, studies=None, start=None, count=None):
        """
        fetches samplingEvents for a location

        :param location_id: location
        :type location_id: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: SamplingEvents
        """
        (ret, retcode) = self.sampling_event_controller.download_sampling_events_by_location(location_id, start=start,
                                                                                             count=count, studies=studies, user=self._user,
                                                                                             auths=self.sampling_event_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'SamplingEvents')

    def download_sampling_events_by_study(self, study_name, studies=None, start=None, count=None):
        """
        fetches samplingEvents for a study

        :param study_name: 4 digit study code
        :type study_name: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: SamplingEvents
        """
        (ret, retcode) = self.sampling_event_controller.download_sampling_events_by_study(study_name, start=start,
                                                                                          count=count, studies=studies, user=self._user,
                                                                                          auths=self.sampling_event_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'SamplingEvents')

    def download_sampling_events_by_taxa(self, taxa_id, studies=None, start=None, count=None):
        """
        fetches samplingEvents for a given taxonomy classification code

        :param taxa_id: NCBI taxonomy code
        :type taxa_id: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: SamplingEvents
        """
        (ret, retcode) = self.sampling_event_controller.download_sampling_events_by_taxa(taxa_id, start=start,
                                                                                         count=count, studies=studies, user=self._user,
                                                                                         auths=self.sampling_event_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'SamplingEvents')

    def update_sampling_event(self, sampling_event_id, sampling_event,
                              studies=None):
        """
        updates an samplingEvent

        :param sampling_event_id: ID of samplingEvent to update
        :type sampling_event_id: str
        :param sampling_event:
        :type sampling_event: dict | bytes

        :rtype: SamplingEvent
        """
        (ret, retcode) = self.sampling_event_controller.update_sampling_event(sampling_event_id, sampling_event, studies=studies, user=self._user,
                                                                              auths=self.sampling_event_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'SamplingEvent')

    def merge_sampling_events(self, samplingEventId1, samplingEventId2,
                              studies=None):
        """
        merges samplingEvents

        :param samplingEventId1: ID of samplingEvent to update
        :type samplingEventId1: str
        :param samplingEventId2: ID of samplingEvent to update
        :type samplingEventId2: str

        :rtype: SamplingEvent
        """
        (ret, retcode) = self.sampling_event_controller.merge_sampling_events(samplingEventId1,
                                                                              samplingEventId2,
                                                                              studies=studies, user=self._user,
                                                                              auths=self.sampling_event_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'SamplingEvent')
