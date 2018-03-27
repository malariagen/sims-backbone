import six

from swagger_server.models.sampling_event import SamplingEvent  # noqa: E501
from swagger_server.models.sampling_events import SamplingEvents  # noqa: E501
from swagger_server import util

import logging

from backbone_server.controllers.sampling_event_controller  import SamplingEventController

from local.base_local_api import BaseLocalApi

class LocalSamplingEventApi(BaseLocalApi):

    def __init__(self, api_client=None):

        super().__init__(api_client)

        self.sampling_event_controller = SamplingEventController()

    def create_sampling_event(self, samplingEvent, user = None, token_info = None):
        """
        create_sampling_event
        Create a samplingEvent
        :param samplingEvent: 
        :type samplingEvent: dict | bytes

        :rtype: SamplingEvent
        """

        (ret, retcode) = self.sampling_event_controller.create_sampling_event(samplingEvent, user,
                                                               self.sampling_event_controller.token_info(token_info))

        return self.create_response(ret, retcode, 'SamplingEvent')

    def delete_sampling_event(self, samplingEventId, user = None, token_info = None):
        """
        deletes an samplingEvent
        
        :param samplingEventId: ID of samplingEvent to fetch
        :type samplingEventId: str

        :rtype: None
        """
        (ret, retcode) = self.sampling_event_controller.delete_sampling_event(samplingEventId, user,
                                                               self.sampling_event_controller.token_info(token_info))

        return self.create_response(ret, retcode)


    def download_sampling_event(self, samplingEventId, user = None, token_info = None):
        """
        fetches an samplingEvent
        
        :param samplingEventId: ID of samplingEvent to fetch
        :type samplingEventId: str

        :rtype: SamplingEvent
        """
        (ret, retcode) = self.sampling_event_controller.download_sampling_event(samplingEventId, user,
                                                                 self.sampling_event_controller.token_info(token_info))

        return self.create_response(ret, retcode, 'SamplingEvent')


    def download_sampling_events_by_event_set(self, eventSetId, start=None, count=None, user = None, token_info = None):
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
                                                                               count, user,
                                                                           self.sampling_event_controller.token_info(token_info))

        return self.create_response(ret, retcode, 'SamplingEvents')

    def download_sampling_events_by_identifier(self, propName, propValue, study_name=None, user = None, token_info = None):
        """
        fetches a samplingEvent by property value
        
        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str

        :rtype: SamplingEvents
        """
        (ret, retcode) = self.sampling_event_controller.download_sampling_events_by_identifier(propName, propValue,
                                                                               study_name,
                                                                               user,
                                                                               self.sampling_event_controller.token_info(token_info))

        return self.create_response(ret, retcode, 'SamplingEvents')

    def download_sampling_events_by_location(self, locationId, start=None, count=None, user = None, token_info = None):
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
                                                                              count, user,
                                                                              self.sampling_event_controller.token_info(token_info))

        return self.create_response(ret, retcode, 'SamplingEvents')

    def download_sampling_events_by_study(self, studyName, start=None, count=None, user = None, token_info = None):
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
                                                                           count, user,
                                                                           self.sampling_event_controller.token_info(token_info))

        return self.create_response(ret, retcode, 'SamplingEvents')

    def download_sampling_events_by_taxa(self, taxaId, start=None, count=None, user = None, token_info = None):
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
                                                                          count, user,
                                                                           self.sampling_event_controller.token_info(token_info))

        return self.create_response(ret, retcode, 'SamplingEvents')


    def update_sampling_event(self, samplingEventId, samplingEvent, user = None, token_info = None):
        """
        updates an samplingEvent
        
        :param samplingEventId: ID of samplingEvent to update
        :type samplingEventId: str
        :param samplingEvent: 
        :type samplingEvent: dict | bytes

        :rtype: SamplingEvent
        """
        (ret, retcode) = self.sampling_event_controller.update_sampling_event(samplingEventId, samplingEvent, user,
                                                               self.sampling_event_controller.token_info(token_info))

        return self.create_response(ret, retcode, 'SamplingEvent')

