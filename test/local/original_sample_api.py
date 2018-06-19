import six

from swagger_server.models.original_sample import OriginalSample  # noqa: E501
from swagger_server.models.original_samples import OriginalSamples  # noqa: E501
from swagger_server import util

import logging

from backbone_server.controllers.original_sample_controller  import OriginalSampleController

from local.base_local_api import BaseLocalApi

class LocalOriginalSampleApi(BaseLocalApi):

    def __init__(self, api_client, user, auths, method):

        super().__init__(api_client, user, auths, method)

        self.original_sample_controller = OriginalSampleController()

    def create_original_sample(self, samplingEvent):
        """
        create_original_sample
        Create a samplingEvent
        :param samplingEvent: 
        :type samplingEvent: dict | bytes

        :rtype: OriginalSample
        """

        (ret, retcode) = self.original_sample_controller.create_original_sample(samplingEvent, self._user,
                                                               self.auth_tokens())

        return self.create_response(ret, retcode, 'OriginalSample')

    def delete_original_sample(self, samplingEventId):
        """
        deletes an samplingEvent
        
        :param samplingEventId: ID of samplingEvent to fetch
        :type samplingEventId: str

        :rtype: None
        """
        (ret, retcode) = self.original_sample_controller.delete_original_sample(samplingEventId, self._user,
                                                               self.auth_tokens())

        return self.create_response(ret, retcode)


    def download_original_sample(self, samplingEventId):
        """
        fetches an samplingEvent
        
        :param samplingEventId: ID of samplingEvent to fetch
        :type samplingEventId: str

        :rtype: OriginalSample
        """
        (ret, retcode) = self.original_sample_controller.download_original_sample(samplingEventId, self._user,
                                                                 self.auth_tokens())

        return self.create_response(ret, retcode, 'OriginalSample')

    def download_original_samples(self, filter=None, start=None, count=None):
        """
        fetches an samplingEvent
        
        :param samplingEventId: ID of samplingEvent to fetch
        :type samplingEventId: str

        :rtype: OriginalSample
        """
        (ret, retcode) = self.original_sample_controller.download_original_samples(filter, start,
                                                                                 count, self._user,
                                                                                 self.auth_tokens())

        return self.create_response(ret, retcode, 'OriginalSamples')


    def download_original_samples_by_event_set(self, eventSetId, start=None, count=None):
        """
        fetches samplingEvents in a given event set
        
        :param eventSetId: Event Set name
        :type eventSetId: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: OriginalSamples
        """
        (ret, retcode) = self.original_sample_controller.download_original_samples_by_event_set(eventSetId,start,
                                                                               count, self._user,
                                                                           self.auth_tokens())

        return self.create_response(ret, retcode, 'OriginalSamples')

    def download_original_samples_by_attr(self, propName, propValue, study_name=None):
        """
        fetches a samplingEvent by property value
        
        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str

        :rtype: OriginalSamples
        """
        (ret, retcode) = self.original_sample_controller.download_original_samples_by_attr(propName, propValue,
                                                                               study_name,
                                                                               self._user,
                                                                               self.auth_tokens())

        return self.create_response(ret, retcode, 'OriginalSamples')

    def download_original_samples_by_location(self, locationId, start=None, count=None):
        """
        fetches samplingEvents for a location
        
        :param locationId: location
        :type locationId: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: OriginalSamples
        """
        (ret, retcode) = self.original_sample_controller.download_original_samples_by_location(locationId, start,
                                                                              count, self._user,
                                                                              self.auth_tokens())

        return self.create_response(ret, retcode, 'OriginalSamples')

    def download_original_samples_by_study(self, studyName, start=None, count=None):
        """
        fetches samplingEvents for a study
        
        :param studyName: 4 digit study code
        :type studyName: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: OriginalSamples
        """
        (ret, retcode) = self.original_sample_controller.download_original_samples_by_study(studyName, start,
                                                                           count, self._user,
                                                                           self.auth_tokens())

        return self.create_response(ret, retcode, 'OriginalSamples')

    def download_original_samples_by_taxa(self, taxaId, start=None, count=None):
        """
        fetches samplingEvents for a given taxonomy classification code
        
        :param taxaId: NCBI taxonomy code
        :type taxaId: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: OriginalSamples
        """
        (ret, retcode) = self.original_sample_controller.download_original_samples_by_taxa(taxaId, start,
                                                                          count, self._user,
                                                                           self.auth_tokens())

        return self.create_response(ret, retcode, 'OriginalSamples')


    def update_original_sample(self, samplingEventId, samplingEvent):
        """
        updates an samplingEvent
        
        :param samplingEventId: ID of samplingEvent to update
        :type samplingEventId: str
        :param samplingEvent: 
        :type samplingEvent: dict | bytes

        :rtype: OriginalSample
        """
        (ret, retcode) = self.original_sample_controller.update_original_sample(samplingEventId, samplingEvent, self._user,
                                                               self.auth_tokens())

        return self.create_response(ret, retcode, 'OriginalSample')

