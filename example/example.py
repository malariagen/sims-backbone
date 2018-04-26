import json
import os
import sys

import requests

import swagger_client

class Example():


    _auth_token = ''
    _api_client = None

    def __init__(self, config_file):
        # Configure OAuth2 access token for authorization: OauthSecurity
        auth_token = self.get_access_token(config_file)

        configuration = swagger_client.Configuration()
        if auth_token:
            configuration.access_token = auth_token

        if os.getenv('REMOTE_HOST_URL'):
            configuration.host = os.getenv('REMOTE_HOST_URL')

        self._api_client = swagger_client.ApiClient(configuration)

    def get_access_token(self, config_file):

        if not self._auth_token:
            if os.getenv('TOKEN_URL'):
                with open(config_file) as json_file:
                    args = json.load(json_file)
                    headers = {'service': 'http://localhost/studies'}
                    token_response = requests.get(os.getenv('TOKEN_URL'), args,
                                                  headers=headers)
                    auth_token = token_response.text.split('=')
                    token = auth_token[1].split('&')[0]
                    self._auth_token = token

        return self._auth_token

    def get_study_details(self):

        study_api = swagger_client.StudyApi(self._api_client)

        studies = study_api.download_studies()

        for study in studies.studies:
            print(repr(study))


    def get_sampling_event_details(self):

        sampling_event_api = swagger_client.SamplingEventApi(self._api_client)

        #start and count are not necessary for small result sets but you will need to use
        #them for larger results sets as the API will time out if you try and retrieve too many
        #Note that the first invocation is likely to take longer to respond
        fetched = sampling_event_api.download_sampling_events_by_taxa(62324, start=0, count=1000)

        #See also:
        #    download_sampling_events_by_study
        #    download_sampling_events_by_event_set
        #    download_sampling_events_by_location

        print('Total sampling events: {}'.format(fetched.count))
        for event in fetched.sampling_events:
            #For performance the location details are only returned once rather
            #than being filled in for each event so here the details are filled in
            if event.location_id:
                event.location = fetched.locations[event.location_id]
            if event.proxy_location_id:
                event.proxy_location = fetched.locations[event.proxy_location_id]
            if event.public_location_id:
                event.public_location = fetched.locations[event.public_location_id]
            print(repr(event))




if __name__ == '__main__':
    example = Example(sys.argv[1])
    example.get_sampling_event_details()

