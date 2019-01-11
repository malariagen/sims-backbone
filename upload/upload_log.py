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

class UploadLog():


    _auth_token = ''
    _api_client = None

    def __init__(self, cmis_config):

        self.get_cmis_client(cmis_config)

        self._dao = RemoteBackboneDAO()

    def get_cmis_client(self, config_file):

        with open(config_file) as json_file:
            config = json.load(json_file)

        self.cmis_client = CmisClient(config['endpoint'], config['username'], config['password'])
        self.repo = self.cmis_client.defaultRepository

    def upload(self, instance_type, log_file):

        log_folder = self.repo.getObjectByPath('/sims/import/logs/' + instance_type)

        with open(log_file, 'rb') as content_file:
            filename = os.path.basename(log_file)
            log_folder.createDocument(filename, contentFile=content_file)



if __name__ == '__main__':
    upload_log = UploadLog(sys.argv[1])
    upload_log.upload(sys.argv[2], sys.argv[3])

