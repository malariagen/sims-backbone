import six

from openapi_server.models.derivative_sample import DerivativeSample  # noqa: E501
from openapi_server.models.derivative_samples import DerivativeSamples  # noqa: E501
from openapi_server import util

import logging

from backbone_server.controllers.derivative_sample_controller import DerivativeSampleController

from local.base_local_api import BaseLocalApi


class LocalDerivativeSampleApi(BaseLocalApi):

    def __init__(self, api_client, user, auths, method):

        super().__init__(api_client, user, auths, method)

        self.derivative_sample_controller = DerivativeSampleController()

    def create_derivative_sample(self, sampling_event):
        """
        create_derivative_sample
        Create a samplingEvent
        :param sampling_event:
        :type sampling_event: dict | bytes

        :rtype: DerivativeSample
        """

        (ret, retcode) = self.derivative_sample_controller.create_derivative_sample(sampling_event, user=self._user,
                                                                                    auths=self.derivative_sample_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'DerivativeSample')

    def delete_derivative_sample(self, sampling_event_id):
        """
        deletes an samplingEvent

        :param sampling_event_id: ID of samplingEvent to fetch
        :type sampling_event_id: str

        :rtype: None
        """
        (ret, retcode) = self.derivative_sample_controller.delete_derivative_sample(sampling_event_id,
                                                                                    studies=None,
                                                                                    user=self._user,
                                                                                    auths=self.derivative_sample_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode)

    def download_derivative_sample(self, derivative_sample_id):
        """
        fetches an samplingEvent

        :param sampling_event_id: ID of samplingEvent to fetch
        :type sampling_event_id: str

        :rtype: DerivativeSample
        """
        (ret, retcode) = self.derivative_sample_controller.download_derivative_sample(derivative_sample_id, user=self._user,
                                                                                      auths=self.derivative_sample_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'DerivativeSample')

    def download_derivative_samples(self, search_filter=None, start=None, count=None):
        """
        fetches an samplingEvent

        :param samplingEventId: ID of samplingEvent to fetch
        :type samplingEventId: str

        :rtype: DerivativeSample
        """
        (ret, retcode) = self.derivative_sample_controller.download_derivative_samples(search_filter, start,
                                                                                       count, user=self._user,
                                                                                       auths=self.derivative_sample_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'DerivativeSamples')

    def download_derivative_samples_by_attr(self, prop_name, prop_value,
                                            study_name=None, value_type=None,
                                            start=None, count=None):
        """
        fetches a samplingEvent by property value

        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str

        :rtype: DerivativeSamples
        """
        (ret, retcode) = self.derivative_sample_controller.download_derivative_samples_by_attr(prop_name, prop_value,
                                                                                               value_type=value_type,
                                                                                               start=start,
                                                                                               count=count,
                                                                                               user=self._user,
                                                                                               auths=self.derivative_sample_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'DerivativeSamples')

    def download_derivative_samples_by_os_attr(self, prop_name, prop_value,
                                               study_name=None,
                                               value_type=None, start=None,
                                               count=None):
        """
        fetches a samplingEvent by property value

        :param prop_name: name of property to search
        :type prop_name: str
        :param prop_value: matching value of property to search
        :type prop_value: str

        :rtype: DerivativeSamples
        """
        (ret, retcode) = self.derivative_sample_controller.download_derivative_samples_by_os_attr(prop_name, prop_value,
                                                                                                  value_type=value_type,
                                                                                                  start=start,
                                                                                                  count=count,
                                                                                                  user=self._user,
                                                                                                  auths=self.derivative_sample_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'DerivativeSamples')

    def download_derivative_samples(self, search_filter, value_type=None, start=None,
                                    count=None):
        """
        fetches a samplingEvent by property value

        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str

        :rtype: DerivativeSamples
        """
        (ret, retcode) = self.derivative_sample_controller.download_derivative_samples(search_filter,
                                                                                       value_type=value_type,
                                                                                       start=start,
                                                                                       count=count,
                                                                                       user=self._user,
                                                                                       auths=self.derivative_sample_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'DerivativeSamples')

    def download_derivative_samples_by_study(self, study_name, start=None, count=None):
        """
        fetches samplingEvents for a study

        :param studyName: 4 digit study code
        :type studyName: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: DerivativeSamples
        """
        (ret, retcode) = self.derivative_sample_controller.download_derivative_samples_by_study(study_name,
                                                                                                studies=None,
                                                                                                start=start,
                                                                                                count=count, user=self._user,
                                                                                                auths=self.derivative_sample_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'DerivativeSamples')

    def download_derivative_samples_by_event_set(self, event_set_id, start=None, count=None):
        """
        fetches samplingEvents in a given event set

        :param event_set_id: Event Set name
        :type event_set_id: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: DerivativeSamples
        """
        (ret, retcode) = self.derivative_sample_controller.download_derivative_samples_by_event_set(event_set_id, start,
                                                                                                    count, user=self._user,
                                                                                                    auths=self.derivative_sample_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'DerivativeSamples')

    def download_derivative_samples_by_taxa(self, taxa_id, start=None, count=None):
        """
        fetches a samplingEvent by property value

        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str

        :rtype: DerivativeSamples
        """
        (ret, retcode) = self.derivative_sample_controller.download_derivative_samples_by_taxa(taxa_id,
                                                                                               studies=None,
                                                                                               start=start,
                                                                                               count=count,
                                                                                               user=self._user,
                                                                                               auths=self.derivative_sample_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'DerivativeSamples')

    def update_derivative_sample(self, derivative_sample_id, derivative_sample):
        """
        updates an samplingEvent

        :param samplingEventId: ID of samplingEvent to update
        :type samplingEventId: str
        :param samplingEvent:
        :type samplingEvent: dict | bytes

        :rtype: DerivativeSample
        """
        (ret, retcode) = self.derivative_sample_controller.update_derivative_sample(derivative_sample_id,
                                                                                    derivative_sample, user=self._user,
                                                                                    auths=self.derivative_sample_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'DerivativeSample')
