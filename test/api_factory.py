import swagger_client
from swagger_client.rest import ApiException

class ApiFactory():

    @staticmethod
    def EventSetApi(api_client):

        ret = swagger_client.EventSetApi(api_client)

        return ret

    @staticmethod
    def LocationApi(api_client):

        ret = swagger_client.LocationApi(api_client)

        return ret

    @staticmethod
    def MetadataApi(api_client):

        ret = swagger_client.MetadataApi(api_client)


        return ret

    @staticmethod
    def SamplingEventApi(api_client):

        ret = swagger_client.SamplingEventApi(api_client)

        return ret


    @staticmethod
    def StudyApi(api_client):

        ret = swagger_client.StudyApi(api_client)

        return ret
