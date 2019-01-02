import json
import requests
import os

import urllib.parse

import logging

from abstract_backbone_dao import AbstractBackboneDAO

import swagger_client
from swagger_client.rest import ApiException

class RemoteBackboneDAO(AbstractBackboneDAO):

    _auth_token = None

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def setup(self, config_file):
        # Configure OAuth2 access token for authorization: OauthSecurity
        auth_token = self.get_access_token(config_file)

        configuration = swagger_client.Configuration()
        if auth_token:
            configuration.access_token = auth_token

        if os.getenv('REMOTE_HOST_URL'):
          configuration.host = "http://localhost:8080/v1"

        self.es_api_instance = swagger_client.EventSetApi(swagger_client.ApiClient(configuration))
        self.location_api_instance = swagger_client.LocationApi(swagger_client.ApiClient(configuration))
        self.se_api_instance = swagger_client.SamplingEventApi(swagger_client.ApiClient(configuration))
        self.os_api_instance = swagger_client.OriginalSampleApi(swagger_client.ApiClient(configuration))
        self.ds_api_instance = swagger_client.DerivativeSampleApi(swagger_client.ApiClient(configuration))
        self.ad_api_instance = swagger_client.AssayDataApi(swagger_client.ApiClient(configuration))
        self.metadata_api_instance = swagger_client.MetadataApi(swagger_client.ApiClient(configuration))
        self.study_api_instance = swagger_client.StudyApi(swagger_client.ApiClient(configuration))

    def get_access_token(self, config_file):

        if not self._auth_token:
            if os.getenv('TOKEN_URL'):
                try:
                    with open(config_file) as json_file:
                        args = json.load(json_file)
                        r = requests.get(os.getenv('TOKEN_URL'), args, headers = { 'service': 'http://localhost/full-map' })
                        at = r.text.split('=')
                        token = at[1].split('&')[0]
                        self._auth_token = token
                except FileNotFoundError as fnfe:
                    #Should already be reported in uploader
                    pass

        return self._auth_token

    def create_event_set(self, event_set_id):

        api_response = None

        try:
            # creates an eventSet
            api_response = super(RemoteBackboneDAO, self).create_event_set(event_set_id)
        except ApiException as e:
            if e.status != 422: #Already exists
                print("Exception when calling EventSetApi->create_event_set: %s\n" % e)
        return api_response

    def create_event_set_item(self, event_set_id, sampling_event_id):
        try:
            super(RemoteBackboneDAO, self).create_event_set_item(event_set_id, sampling_event_id)
        except ApiException as err:
            #Probably because it already exists
            self._logger.debug("Error adding sample {} to event set {} {}".format(sampling_event_id, event_set_id, err))

    def download_gps_location(self, latitude, longitude):

        ret = super(RemoteBackboneDAO, self).download_gps_location(str(latitude), str(longitude))

        return ret

    def download_sampling_events_by_attr(self, attr_type, attr_value):

        value = urllib.parse.quote_plus(attr_value)
        found_events = super(RemoteBackboneDAO, self).download_sampling_events_by_attr(attr_type,
                                                                                   value)

        return found_events

    def download_sampling_events_by_os_attr(self, attr_type, attr_value):

        value = urllib.parse.quote_plus(attr_value)
        found_events = super(RemoteBackboneDAO, self).download_sampling_events_by_os_attr(attr_type,
                                                                                   value)

        return found_events

    def download_original_samples_by_attr(self, attr_type, attr_value):

        found_events = super(RemoteBackboneDAO, self).download_original_samples_by_attr(attr_type,
                                                                                            urllib.parse.quote_plus(attr_value))

        return found_events

