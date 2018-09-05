import six

from swagger_server.models.derivative_sample import DerivativeSample  # noqa: E501
from swagger_server.models.derivative_samples import DerivativeSamples  # noqa: E501
from swagger_server import util

import logging

from backbone_server.controllers.derivative_sample_controller  import DerivativeSampleController

from local.base_local_api import BaseLocalApi

class LocalDerivativeSampleApi(BaseLocalApi):

    def __init__(self, api_client, user, auths, method):

        super().__init__(api_client, user, auths, method)

        self.derivative_sample_controller = DerivativeSampleController()

    def create_derivative_sample(self, samplingEvent):
        """
        create_derivative_sample
        Create a samplingEvent
        :param samplingEvent: 
        :type samplingEvent: dict | bytes

        :rtype: DerivativeSample
        """

        (ret, retcode) = self.derivative_sample_controller.create_derivative_sample(samplingEvent, self._user,
                                                               self.auth_tokens())

        return self.create_response(ret, retcode, 'DerivativeSample')

    def delete_derivative_sample(self, samplingEventId):
        """
        deletes an samplingEvent
        
        :param samplingEventId: ID of samplingEvent to fetch
        :type samplingEventId: str

        :rtype: None
        """
        (ret, retcode) = self.derivative_sample_controller.delete_derivative_sample(samplingEventId, self._user,
                                                               self.auth_tokens())

        return self.create_response(ret, retcode)


    def download_derivative_sample(self, derivativeSampleId):
        """
        fetches an samplingEvent
        
        :param samplingEventId: ID of samplingEvent to fetch
        :type samplingEventId: str

        :rtype: DerivativeSample
        """
        (ret, retcode) = self.derivative_sample_controller.download_derivative_sample(derivativeSampleId, self._user,
                                                                 self.auth_tokens())

        return self.create_response(ret, retcode, 'DerivativeSample')

    def download_derivative_samples(self, filter=None, start=None, count=None):
        """
        fetches an samplingEvent
        
        :param samplingEventId: ID of samplingEvent to fetch
        :type samplingEventId: str

        :rtype: DerivativeSample
        """
        (ret, retcode) = self.derivative_sample_controller.download_derivative_samples(filter, start,
                                                                                 count, self._user,
                                                                                 self.auth_tokens())

        return self.create_response(ret, retcode, 'DerivativeSamples')


    def download_derivative_samples_by_attr(self, propName, propValue, study_name=None):
        """
        fetches a samplingEvent by property value
        
        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str

        :rtype: DerivativeSamples
        """
        (ret, retcode) = self.derivative_sample_controller.download_derivative_samples_by_attr(propName, propValue,
                                                                               self._user,
                                                                               self.auth_tokens())

        return self.create_response(ret, retcode, 'DerivativeSamples')

    def download_derivative_samples_by_os_attr(self, propName, propValue, study_name=None):
        """
        fetches a samplingEvent by property value
        
        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str

        :rtype: DerivativeSamples
        """
        (ret, retcode) = self.derivative_sample_controller.download_derivative_samples_by_os_attr(propName, propValue,
                                                                               self._user,
                                                                               self.auth_tokens())

        return self.create_response(ret, retcode, 'DerivativeSamples')


    def download_derivative_samples(self, search_filter, start=None, count=None):
        """
        fetches a samplingEvent by property value
        
        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str

        :rtype: DerivativeSamples
        """
        (ret, retcode) = self.derivative_sample_controller.download_derivative_samples(search_filter,
                                                                                       start, count,
                                                                                       self._user,
                                                                                       self.auth_tokens())

        return self.create_response(ret, retcode, 'DerivativeSamples')

    def download_derivative_samples_by_taxa(self, taxaId, start=None, count=None):
        """
        fetches a samplingEvent by property value
        
        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str

        :rtype: DerivativeSamples
        """
        (ret, retcode) = self.derivative_sample_controller.download_derivative_samples_by_taxa(taxaId,
                                                                                               start, count,
                                                                                               self._user,
                                                                                               self.auth_tokens())

        return self.create_response(ret, retcode, 'DerivativeSamples')

    def update_derivative_sample(self, derivativeSampleId, derivativeSample):
        """
        updates an samplingEvent
        
        :param samplingEventId: ID of samplingEvent to update
        :type samplingEventId: str
        :param samplingEvent: 
        :type samplingEvent: dict | bytes

        :rtype: DerivativeSample
        """
        (ret, retcode) = self.derivative_sample_controller.update_derivative_sample(derivativeSampleId,
                                                                              derivativeSample, self._user,
                                                               self.auth_tokens())

        return self.create_response(ret, retcode, 'DerivativeSample')

