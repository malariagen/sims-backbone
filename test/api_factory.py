import os

import swagger_client

from local.event_set_api import LocalEventSetApi
from local.location_api import LocalLocationApi
from local.metadata_api import LocalMetadataApi
from local.sampling_event_api import LocalSamplingEventApi
from local.study_api import LocalStudyApi

from backbone_server.controllers.base_controller  import BaseController


class ApiFactory():

    def __init__(self, user, auths, method, api_client):
        self._user = user
        self._auths = auths
        self._method = method
        self._api_client = api_client

        self.base_controller = BaseController()


    def isLocal(self):

        if os.getenv('LOCAL_TEST'):
            return True
        else:
            return False


    def is_authorized(self, study_id):

        if self.isLocal():
            try:
                self.base_controller.check_permissions(study_id, self._auths)
            except Exception as excp:
                return False

            return True
        else:
            #Assumes if authenticated then authorized
            #Local test does this better
            if self._api_client.configuration.access_token and not \
            self._api_client.configuration.access_token == 'abcd':
                return True
            else:
                return False


    def EventSetApi(self):

        ret = None

        if self.isLocal():
            ret = LocalEventSetApi(self._api_client, self._user, self._auths, self._method)
        else:
            ret = swagger_client.EventSetApi(self._api_client)

        return ret


    def LocationApi(self):

        ret = None

        if self.isLocal():
            ret = LocalLocationApi(self._api_client, self._user, self._auths, self._method)
        else:
            ret = swagger_client.LocationApi(self._api_client)

        return ret


    def MetadataApi(self):

        ret = None

        if self.isLocal():
            ret = LocalMetadataApi(self._api_client, self._user, self._auths, self._method)
        else:
            ret = swagger_client.MetadataApi(self._api_client)

        return ret


    def SamplingEventApi(self):

        ret = None

        if self.isLocal():
            ret = LocalSamplingEventApi(self._api_client, self._user, self._auths, self._method)
        else:
            ret = swagger_client.SamplingEventApi(self._api_client)

        return ret



    def StudyApi(self):

        ret = None

        if self.isLocal():
            ret = LocalStudyApi(self._api_client, self._user, self._auths, self._method)
        else:
            ret = swagger_client.StudyApi(self._api_client)

        return ret
