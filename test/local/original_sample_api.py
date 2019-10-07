import six

from openapi_server.models.original_sample import OriginalSample  # noqa: E501
from openapi_server.models.original_samples import OriginalSamples  # noqa: E501
from openapi_server import util

import logging

from backbone_server.controllers.original_sample_controller import OriginalSampleController

from local.base_local_api import BaseLocalApi


class LocalOriginalSampleApi(BaseLocalApi):

    def __init__(self, api_client, user, auths, method):

        super().__init__(api_client, user, auths, method)

        self.original_sample_controller = OriginalSampleController()

    def create_original_sample(self, original_sample, uuid_val=None):
        """
        create_original_sample
        Create a samplingEvent
        :param original_sample:
        :type original_sample: dict | bytes

        :rtype: OriginalSample
        """

        (ret, retcode) = self.original_sample_controller.create_original_sample(original_sample,
                                                                                uuid_val=uuid_val,
                                                                                user=self._user,
                                                                                auths=self.original_sample_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'OriginalSample')

    def delete_original_sample(self, original_sample_id):
        """
        deletes an original_sample_id

        :param original_sample_id: ID of samplingEvent to fetch
        :type original_sample_id: str

        :rtype: None
        """
        (ret, retcode) = self.original_sample_controller.delete_original_sample(original_sample_id, self._user,
                                                                                self.original_sample_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode)

    def download_original_sample(self, original_sample_id):
        """
        fetches an samplingEvent

        :param original_sample_id: ID of samplingEvent to fetch
        :type original_sample_id: str

        :rtype: OriginalSample
        """
        (ret, retcode) = self.original_sample_controller.download_original_sample(original_sample_id, self._user,
                                                                                  self.original_sample_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'OriginalSample')

    def download_original_samples(self, search_filter=None, start=None, count=None):
        """
        fetches an samplingEvent

        :param samplingEventId: ID of samplingEvent to fetch
        :type samplingEventId: str

        :rtype: OriginalSample
        """
        (ret, retcode) = self.original_sample_controller.download_original_samples(search_filter, start,
                                                                                   count, self._user,
                                                                                   self.original_sample_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'OriginalSamples')

    def download_original_samples_by_event_set(self, event_set_id, start=None, count=None):
        """
        fetches samplingEvents in a given event set

        :param event_set_id: Event Set name
        :type event_set_id: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: OriginalSamples
        """
        (ret, retcode) = self.original_sample_controller.download_original_samples_by_event_set(event_set_id, start,
                                                                                                count, self._user,
                                                                                                self.original_sample_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'OriginalSamples')

    def download_original_samples_by_attr(self, prop_name, prop_value, study_name=None):
        """
        fetches a samplingEvent by property value

        :param prop_name: name of property to search
        :type prop_name: str
        :param prop_value: matching value of property to search
        :type prop_value: str

        :rtype: OriginalSamples
        """
        (ret, retcode) = self.original_sample_controller.download_original_samples_by_attr(prop_name, prop_value,
                                                                                           study_name,
                                                                                           self._user,
                                                                                           self.original_sample_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'OriginalSamples')

    def download_original_samples_by_location(self, location_id, start=None, count=None):
        """
        fetches samplingEvents for a location

        :param location_id: location
        :type location_id: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: OriginalSamples
        """
        (ret, retcode) = self.original_sample_controller.download_original_samples_by_location(location_id, start,
                                                                                               count, self._user,
                                                                                               self.original_sample_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'OriginalSamples')

    def download_original_samples_by_study(self, study_name, start=None, count=None):
        """
        fetches samplingEvents for a study

        :param study_name: 4 digit study code
        :type study_name: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: OriginalSamples
        """
        (ret, retcode) = self.original_sample_controller.download_original_samples_by_study(study_name, start,
                                                                                            count, self._user,
                                                                                            self.original_sample_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'OriginalSamples')

    def download_original_samples_by_taxa(self, taxa_id, start=None, count=None):
        """
        fetches samplingEvents for a given taxonomy classification code

        :param taxa_id: NCBI taxonomy code
        :type taxa_id: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: OriginalSamples
        """
        (ret, retcode) = self.original_sample_controller.download_original_samples_by_taxa(taxa_id, start,
                                                                                           count, self._user,
                                                                                           self.original_sample_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'OriginalSamples')

    def update_original_sample(self, sampling_event_id, sampling_event):
        """
        updates an samplingEvent

        :param sampling_event_id: ID of samplingEvent to update
        :type sampling_event_id: str
        :param sampling_event:
        :type sampling_event: dict | bytes

        :rtype: OriginalSample
        """
        (ret, retcode) = self.original_sample_controller.update_original_sample(sampling_event_id,
                                                                                sampling_event,
                                                                                self._user,
                                                                                self.original_sample_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'OriginalSample')

    def merge_original_samples(self, samplingEventId, samplingEventId2):
        """
        merges OriginalSamples

        :param samplingEventId1: ID of samplingEvent to update
        :type samplingEventId1: str
        :param samplingEventId2: ID of samplingEvent to update
        :type samplingEventId2: str

        :rtype: OriginalSample
        """
        (ret, retcode) = self.original_sample_controller.merge_original_samples(samplingEventId,
                                                                                samplingEventId2,
                                                                                self._user,
                                                                                self.original_sample_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'OriginalSample')
