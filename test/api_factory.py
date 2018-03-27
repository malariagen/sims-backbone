import os

import swagger_client
from swagger_client.rest import ApiException

from local.event_set_api import LocalEventSetApi
from local.location_api import LocalLocationApi
from local.metadata_api import LocalMetadataApi
from local.sampling_event_api import LocalSamplingEventApi
from local.study_api import LocalStudyApi


class ApiFactory():

    @staticmethod
    def isLocal():

        if os.getenv('LOCAL_TEST'):
            return True
        else:
            return False

    @staticmethod
    def EventSetApi(api_client):

        ret = None

        if ApiFactory.isLocal():
            ret = LocalEventSetApi(api_client)
        else:
            ret = swagger_client.EventSetApi(api_client)

        return ret

    @staticmethod
    def LocationApi(api_client):

        ret = None

        if ApiFactory.isLocal():
            ret = LocalLocationApi(api_client)
        else:
            ret = swagger_client.LocationApi(api_client)

        return ret

    @staticmethod
    def MetadataApi(api_client):

        ret = None

        if ApiFactory.isLocal():
            ret = LocalMetadataApi(api_client)
        else:
            ret = swagger_client.MetadataApi(api_client)

        return ret

    @staticmethod
    def SamplingEventApi(api_client):

        ret = None

        if ApiFactory.isLocal():
            ret = LocalSamplingEventApi(api_client)
        else:
            ret = swagger_client.SamplingEventApi(api_client)

        return ret


    @staticmethod
    def StudyApi(api_client):

        ret = None

        if ApiFactory.isLocal():
            ret = LocalStudyApi(api_client)
        else:
            ret = swagger_client.StudyApi(api_client)

        return ret
