import six

from swagger_server.models.derived_sample import DerivedSample  # noqa: E501
from swagger_server.models.derived_samples import DerivedSamples  # noqa: E501
from swagger_server import util

import logging

from backbone_server.controllers.derived_sample_controller  import DerivedSampleController

from local.base_local_api import BaseLocalApi

class LocalDerivedSampleApi(BaseLocalApi):

    def __init__(self, api_client, user, auths, method):

        super().__init__(api_client, user, auths, method)

        self.derived_sample_controller = DerivedSampleController()

    def create_derived_sample(self, samplingEvent):
        """
        create_derived_sample
        Create a samplingEvent
        :param samplingEvent: 
        :type samplingEvent: dict | bytes

        :rtype: DerivedSample
        """

        (ret, retcode) = self.derived_sample_controller.create_derived_sample(samplingEvent, self._user,
                                                               self.auth_tokens())

        return self.create_response(ret, retcode, 'DerivedSample')

    def delete_derived_sample(self, samplingEventId):
        """
        deletes an samplingEvent
        
        :param samplingEventId: ID of samplingEvent to fetch
        :type samplingEventId: str

        :rtype: None
        """
        (ret, retcode) = self.derived_sample_controller.delete_derived_sample(samplingEventId, self._user,
                                                               self.auth_tokens())

        return self.create_response(ret, retcode)


    def download_derived_sample(self, derivedSampleId):
        """
        fetches an samplingEvent
        
        :param samplingEventId: ID of samplingEvent to fetch
        :type samplingEventId: str

        :rtype: DerivedSample
        """
        (ret, retcode) = self.derived_sample_controller.download_derived_sample(derivedSampleId, self._user,
                                                                 self.auth_tokens())

        return self.create_response(ret, retcode, 'DerivedSample')

    def download_derived_samples(self, filter=None, start=None, count=None):
        """
        fetches an samplingEvent
        
        :param samplingEventId: ID of samplingEvent to fetch
        :type samplingEventId: str

        :rtype: DerivedSample
        """
        (ret, retcode) = self.derived_sample_controller.download_derived_samples(filter, start,
                                                                                 count, self._user,
                                                                                 self.auth_tokens())

        return self.create_response(ret, retcode, 'DerivedSamples')


    def download_derived_samples_by_attr(self, propName, propValue, study_name=None):
        """
        fetches a samplingEvent by property value
        
        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str

        :rtype: DerivedSamples
        """
        (ret, retcode) = self.derived_sample_controller.download_derived_samples_by_attr(propName, propValue,
                                                                               self._user,
                                                                               self.auth_tokens())

        return self.create_response(ret, retcode, 'DerivedSamples')


    def update_derived_sample(self, derivedSampleId, derivedSample):
        """
        updates an samplingEvent
        
        :param samplingEventId: ID of samplingEvent to update
        :type samplingEventId: str
        :param samplingEvent: 
        :type samplingEvent: dict | bytes

        :rtype: DerivedSample
        """
        (ret, retcode) = self.derived_sample_controller.update_derived_sample(derivedSampleId,
                                                                              derivedSample, self._user,
                                                               self.auth_tokens())

        return self.create_response(ret, retcode, 'DerivedSample')

