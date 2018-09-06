import six

from swagger_server.models.sampling_event import SamplingEvent  # noqa: E501
from swagger_server.models.sampling_events import SamplingEvents  # noqa: E501
from swagger_server import util

import logging

from backbone_server.controllers.sampling_event_controller  import SamplingEventController

from local.base_local_api import BaseLocalApi

class LocalSamplingEventApi(BaseLocalApi):

    def __init__(self, api_client, user, auths, method):

        super().__init__(api_client, user, auths, method)

        self.sampling_event_controller = SamplingEventController()

    def create_sampling_event(self, samplingEvent):
        """
        create_sampling_event
        Create a samplingEvent
        :param samplingEvent: 
        :type samplingEvent: dict | bytes

        :rtype: SamplingEvent
        """

        (ret, retcode) = self.sampling_event_controller.create_sampling_event(samplingEvent, self._user,
                                                               self.auth_tokens())

        return self.create_response(ret, retcode, 'SamplingEvent')

    def delete_sampling_event(self, samplingEventId):
        """
        deletes an samplingEvent
        
        :param samplingEventId: ID of samplingEvent to fetch
        :type samplingEventId: str

        :rtype: None
        """
        (ret, retcode) = self.sampling_event_controller.delete_sampling_event(samplingEventId, self._user,
                                                               self.auth_tokens())

        return self.create_response(ret, retcode)


    def download_sampling_event(self, samplingEventId):
        """
        fetches an samplingEvent
        
        :param samplingEventId: ID of samplingEvent to fetch
        :type samplingEventId: str

        :rtype: SamplingEvent
        """
        (ret, retcode) = self.sampling_event_controller.download_sampling_event(samplingEventId, self._user,
                                                                 self.auth_tokens())

        return self.create_response(ret, retcode, 'SamplingEvent')

    def download_sampling_events(self, search_filter=None, start=None, count=None):
        """
        fetches an samplingEvent
        
        :param samplingEventId: ID of samplingEvent to fetch
        :type samplingEventId: str

        :rtype: SamplingEvent
        """
        (ret, retcode) = self.sampling_event_controller.download_sampling_events(search_filter, start,
                                                                                 count, self._user,
                                                                                 self.auth_tokens())

        return self.create_response(ret, retcode, 'SamplingEvents')


    def download_sampling_events_by_event_set(self, eventSetId, start=None, count=None):
        """
        fetches samplingEvents in a given event set
        
        :param eventSetId: Event Set name
        :type eventSetId: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: SamplingEvents
        """
        (ret, retcode) = self.sampling_event_controller.download_sampling_events_by_event_set(eventSetId,start,
                                                                               count, self._user,
                                                                           self.auth_tokens())

        return self.create_response(ret, retcode, 'SamplingEvents')

    def download_sampling_events_by_attr(self, propName, propValue, study_name=None):
        """
        fetches a samplingEvent by property value
        
        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str

        :rtype: SamplingEvents
        """
        (ret, retcode) = self.sampling_event_controller.download_sampling_events_by_attr(propName, propValue,
                                                                               study_name,
                                                                               self._user,
                                                                               self.auth_tokens())

        return self.create_response(ret, retcode, 'SamplingEvents')

    def download_sampling_events_by_os_attr(self, propName, propValue, study_name=None):
        """
        fetches a samplingEvent by property value
        
        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str

        :rtype: SamplingEvents
        """
        (ret, retcode) = self.sampling_event_controller.download_sampling_events_by_os_attr(propName, propValue,
                                                                               study_name,
                                                                               self._user,
                                                                               self.auth_tokens())

        return self.create_response(ret, retcode, 'SamplingEvents')

    def download_sampling_events_by_location(self, locationId, start=None, count=None):
        """
        fetches samplingEvents for a location
        
        :param locationId: location
        :type locationId: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: SamplingEvents
        """
        (ret, retcode) = self.sampling_event_controller.download_sampling_events_by_location(locationId, start,
                                                                              count, self._user,
                                                                              self.auth_tokens())

        return self.create_response(ret, retcode, 'SamplingEvents')

    def download_sampling_events_by_study(self, studyName, start=None, count=None):
        """
        fetches samplingEvents for a study
        
        :param studyName: 4 digit study code
        :type studyName: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: SamplingEvents
        """
        (ret, retcode) = self.sampling_event_controller.download_sampling_events_by_study(studyName, start,
                                                                           count, self._user,
                                                                           self.auth_tokens())

        return self.create_response(ret, retcode, 'SamplingEvents')

    def download_sampling_events_by_taxa(self, taxaId, start=None, count=None):
        """
        fetches samplingEvents for a given taxonomy classification code
        
        :param taxaId: NCBI taxonomy code
        :type taxaId: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: SamplingEvents
        """
        (ret, retcode) = self.sampling_event_controller.download_sampling_events_by_taxa(taxaId, start,
                                                                          count, self._user,
                                                                           self.auth_tokens())

        return self.create_response(ret, retcode, 'SamplingEvents')


    def update_sampling_event(self, samplingEventId, samplingEvent):
        """
        updates an samplingEvent
        
        :param samplingEventId: ID of samplingEvent to update
        :type samplingEventId: str
        :param samplingEvent: 
        :type samplingEvent: dict | bytes

        :rtype: SamplingEvent
        """
        (ret, retcode) = self.sampling_event_controller.update_sampling_event(samplingEventId, samplingEvent, self._user,
                                                               self.auth_tokens())

        return self.create_response(ret, retcode, 'SamplingEvent')


    def merge_sampling_events(self, samplingEventId1, samplingEventId2):
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
                                                                              self._user,
                                                                              self.auth_tokens())

        return self.create_response(ret, retcode, 'SamplingEvent')

