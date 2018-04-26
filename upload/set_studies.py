import json
import os
import sys

import requests

from cmislib import CmisClient
import swagger_client

class SetStudies():


    _auth_token = ''
    _api_client = None

    def __init__(self, config_file, cmis_config):
        # Configure OAuth2 access token for authorization: OauthSecurity
        auth_token = self.get_access_token(config_file)

        configuration = swagger_client.Configuration()
        if auth_token:
            configuration.access_token = auth_token

        if os.getenv('REMOTE_HOST_URL'):
          configuration.host = os.getenv('REMOTE_HOST_URL')

        self._api_client = swagger_client.ApiClient(configuration)

        self.get_cmis_client(cmis_config)

    def get_access_token(self, config_file):

        if not self._auth_token:
            if os.getenv('TOKEN_URL'):
                with open(config_file) as json_file:
                    args = json.load(json_file)
                    r = requests.get(os.getenv('TOKEN_URL'), args, headers = { 'service': 'http://localhost/full-map' })
                    at = r.text.split('=')
                    token = at[1].split('&')[0]
                    self._auth_token = token

        return self._auth_token

    def get_cmis_client(self, config_file):

        with open(config_file) as json_file:
            config = json.load(json_file)

        self.cmis_client = CmisClient(config['endpoint'], config['username'], config['password'])
        self.repo = self.cmis_client.defaultRepository

    def update_study_names(self):

        study_api = swagger_client.StudyApi(self._api_client)

        studies = study_api.download_studies()

        studies_dict = {}
        for study in studies.studies:
            studies_dict[study.code] = study.name

        results = self.repo.query("select * from cggh:collaborationFolder")

        for result in results:
            print(result.getName())
            code = result.getName()[:4]
            if code in studies_dict:
                if studies_dict[code] != result.getName():
                    print('Updating {} to {}'.format(studies_dict[code],
                                                     result.getName()))
                    study_detail = study_api.download_study(code)
                    study_detail.name = result.getName()
                    study_api.update_study(code, study_detail)


if __name__ == '__main__':
    studies_setter = SetStudies(sys.argv[1], sys.argv[2])
    studies_setter.update_study_names()

