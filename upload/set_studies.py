import json
import os
import sys
import datetime
import logging

import requests

from cmislib import CmisClient
import swagger_client

from remote_backbone_dao import RemoteBackboneDAO
from local_backbone_dao import LocalBackboneDAO

class SetStudies():


    _auth_token = ''
    _api_client = None

    def __init__(self, config_file, cmis_config):

        self.get_cmis_client(cmis_config)

        self._dao = RemoteBackboneDAO()

        self._config_file = config_file

        try:
            with open(config_file) as json_file:
                args = json.load(json_file)
                if 'dao_type' in args:
                    if args['dao_type'] == 'local':
                        if 'database' in args:
                            os.environ['POSTGRES_DB'] = args['database']
                        print('Using database {}'.format(os.getenv('POSTGRES_DB','backbone_service')))
                        self._dao = LocalBackboneDAO(args['username'], args['auths'])
                if 'debug' in args:
                    if args['debug']:
                        log_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
                        log_file = 'uploader_{}.log'.format(log_time)
                        print("Debugging to {}".format(log_file))
                        logging.basicConfig(level=logging.DEBUG, filename=log_file)
        except FileNotFoundError as fnfe:
            print('No config file found: {}'.format(config_file))
            pass

        self._dao.setup(config_file)

    def get_cmis_client(self, config_file):

        with open(config_file) as json_file:
            config = json.load(json_file)

        self.cmis_client = CmisClient(config['endpoint'], config['username'], config['password'])
        self.repo = self.cmis_client.defaultRepository

    def update_study_names(self):

        studies = self._dao.download_studies()

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
                    study_detail = self._dao.download_study(code)
                    study_detail.name = result.getName()
                    self._dao.update_study(code, study_detail)


if __name__ == '__main__':
    studies_setter = SetStudies(sys.argv[1], sys.argv[2])
    studies_setter.update_study_names()

