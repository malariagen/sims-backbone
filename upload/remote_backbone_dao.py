import json
import requests
import os

import urllib.parse

import logging

from abstract_backbone_dao import AbstractBackboneDAO

import openapi_client
from openapi_client.rest import ApiException

class RemoteBackboneDAO(AbstractBackboneDAO):

    _auth_token = None

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def setup(self, config_file):
        # Configure OAuth2 access token for authorization: OauthSecurity
        auth_token = self.get_access_token(config_file)

        configuration = openapi_client.Configuration()
        if auth_token:
            configuration.access_token = auth_token

        if os.getenv('REMOTE_HOST_URL'):
            configuration.host = os.getenv('REMOTE_HOST_URL')

        self.create_apis(configuration)

    def create_apis(self, configuration):

        self.es_api_instance = openapi_client.EventSetApi(openapi_client.ApiClient(configuration))
        self.location_api_instance = openapi_client.LocationApi(openapi_client.ApiClient(configuration))
        self.se_api_instance = openapi_client.SamplingEventApi(openapi_client.ApiClient(configuration))
        self.os_api_instance = openapi_client.OriginalSampleApi(openapi_client.ApiClient(configuration))
        self.ds_api_instance = openapi_client.DerivativeSampleApi(openapi_client.ApiClient(configuration))
        self.ad_api_instance = openapi_client.AssayDataApi(openapi_client.ApiClient(configuration))
        self.metadata_api_instance = openapi_client.MetadataApi(openapi_client.ApiClient(configuration))
        self.study_api_instance = openapi_client.StudyApi(openapi_client.ApiClient(configuration))
        self.i_api_instance = openapi_client.IndividualApi(openapi_client.ApiClient(configuration))

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
            api_response = self.es_api_instance.create_event_set(event_set_id)
        except ApiException as e:
            if e.status != 422: #Already exists
                print("Exception when calling EventSetApi->create_event_set: %s\n" % e)
        return api_response

    def download_event_set(self, eventSetId, user=None):
        return self.es_api_instance.download_event_set(eventSetId)

    def delete_event_set(self, eventSetId, user=None):
        return self.es_api_instance.delete_event_set(eventSetId)


    def create_event_set_item(self, event_set_id, sampling_event_id, user=None):
        self.es_api_instance.create_event_set_item(event_set_id, sampling_event_id)

    def create_location(self, location, user=None):

        created = self.location_api_instance.create_location(location)

        return created

    def create_sampling_event(self, sampling_event, user=None):
        created = self.se_api_instance.create_sampling_event(sampling_event)

        return created

    def merge_sampling_events(self, sampling_event_id1, sampling_event_id2, user=None):
        self.se_api_instance.merge_sampling_events(sampling_event_id1, sampling_event_id2)

    def delete_sampling_event(self, sampling_event_id, user=None):
        self.se_api_instance.delete_sampling_event(sampling_event_id)

    def download_gps_location(self, latitude, longitude, user=None):

        ret = self.location_api_instance.download_gps_location(str(latitude), str(longitude))
        return ret

    def download_location(self, location_id, user=None):

        ret = self.location_api_instance.download_location(location_id)

        return ret

    def download_locations_by_attr(self, attr_type, attr_value,
                                   study_name=None, user=None):

        ret = self.location_api_instance.download_locations_by_attr(attr_type,
                                                                    attr_value,
                                                                    study_name=study_name)

        return ret

    def delete_location(self, location_id, user=None):
        ret = self.location_api_instance.delete_location(location_id)

        return ret

    def download_partner_location(self, partner_name, user=None):

        ret = self.location_api_instance.download_partner_location(partner_name)
        return ret

    def download_sampling_event(self, sampling_event_id, user=None):

        existing = self.se_api_instance.download_sampling_event(sampling_event_id)

        return existing

    def download_sampling_events_by_event_set(self, eventSetId, user=None):
        return self.se_api_instance.download_sampling_events_by_event_set(eventSetId)

    def download_sampling_events_by_study(self, study_id, user=None):
        return self.se_api_instance.download_sampling_events_by_study(study_id)

    def download_sampling_events_by_attr(self, attr_type, attr_value):

        value = urllib.parse.quote_plus(attr_value)
        found_events = self.se_api_instance.download_sampling_events_by_attr(attr_type,
                                                                             value)

        return found_events

    def download_sampling_events_by_os_attr(self, attr_type, attr_value, user=None):

        value = urllib.parse.quote_plus(attr_value)
        found_events = self.se_api_instance.download_sampling_events_by_os_attr(attr_type,
                                                                                value)

        return found_events

    def download_original_samples(self, search_filter, user=None):

        found_events = self.os_api_instance.download_original_samples(search_filter)

        return found_events

    def download_original_samples_by_attr(self, attr_type, attr_value, user=None):

        found_events = self.os_api_instance.download_original_samples_by_attr(attr_type,
                                                                              urllib.parse.quote_plus(attr_value))

        return found_events

    def download_sampling_events_by_location(self, location_id, user=None):

        found_events = self.se_api_instance.download_sampling_events_by_location(location_id)

        return found_events

    def update_location(self, location_id, location, user=None):

        updated = self.location_api_instance.update_location(location_id, location)

        return updated

    def update_sampling_event(self, sampling_event_id, sampling_event, user=None):
        ret = self.se_api_instance.update_sampling_event(sampling_event_id, sampling_event)
        return ret

    def get_country_metadata(self, country_value, user=None):
        metadata = self.metadata_api_instance.get_country_metadata(country_value)

        return metadata

    def create_original_sample(self, original_sample, user=None):

        return self.os_api_instance.create_original_sample(original_sample)


    def update_original_sample(self, original_sample_id, original_sample, user=None):

        return self.os_api_instance.update_original_sample(original_sample_id,
                                                                            original_sample)

    def merge_original_samples(self, original_sample_id1, original_sample_id2, user=None):

        return self.os_api_instance.merge_original_samples(original_sample_id1,
                                                                            original_sample_id2)

    def delete_original_sample(self, original_sample_id , user=None):

        return self.os_api_instance.delete_original_sample(original_sample_id)

    def download_original_sample(self, original_sample_id, user=None):

        return self.os_api_instance.download_original_sample(original_sample_id)

    def download_original_samples_by_attr(self, attr_type, attr_value, user=None):

        return self.os_api_instance.download_original_samples_by_attr(attr_type, attr_value)

    def download_original_samples_by_event_set(self, event_set_id, start=None,
                                               count=None, user=None):

        return self.os_api_instance.download_original_samples_by_event_set(event_set_id)

    def create_derivative_sample(self, derivative_sample, user=None):

        return self.ds_api_instance.create_derivative_sample(derivative_sample)


    def update_derivative_sample(self, derivative_sample_id, derivative_sample, user=None):

        return self.ds_api_instance.update_derivative_sample(derivative_sample_id,
                                                                            derivative_sample)

    def delete_derivative_sample(self, derivative_sample_id , user=None):

        return self.ds_api_instance.delete_derivative_sample(derivative_sample_id)

    def download_derivative_sample(self, derivative_sample_id, user=None):

        return self.ds_api_instance.download_derivative_sample(derivative_sample_id)

    def download_derivative_samples_by_attr(self, attr_type, attr_value, user=None):

        return self.ds_api_instance.download_derivative_samples_by_attr(attr_type, attr_value)

    def download_derivative_samples_by_os_attr(self, attr_type, attr_value, user=None):

        return self.ds_api_instance.download_derivative_samples_by_os_attr(attr_type, attr_value)


    def create_assay_datum(self, assay_datum, user=None):

        return self.ad_api_instance.create_assay_datum(assay_datum)


    def update_assay_datum(self, assay_datum_id, assay_datum, user=None):

        return self.ad_api_instance.update_assay_datum(assay_datum_id, assay_datum)

    def delete_assay_datum(self, assay_datum_id, user=None):

        return self.ad_api_instance.delete_assay_datum(assay_datum_id)

    def download_assay_data_by_attr(self, attr_type, attr_value, user=None):

        return self.ad_api_instance.download_assay_data_by_attr(attr_type, attr_value)

    def download_study(self, study_code, user=None):
        return self.study_api_instance.download_study(study_code)

    def download_studies(self, user=None):
        return self.study_api_instance.download_studies()

    def update_study(self, study_code, study_detail, user=None):
        return self.study_api_instance.update_study(study_code, study_detail)

    def create_individual(self, individual, user=None):

        return self.i_api_instance.create_individual(individual)


    def update_individual(self, individual_id, individual, user=None):

        return self.i_api_instance.update_individual(individual_id, individual)

    def merge_individuals(self, individual_id1, individual_id2, user=None):

        return self.i_api_instance.merge_individuals(individual_id1, individual_id2)

    def delete_individual(self, individual_id , user=None):

        return self.i_api_instance.delete_individual(individual_id)

    def download_individual(self, individual_id, user=None):

        return self.i_api_instance.download_individual(individual_id)

    def download_individuals(self, search_filter, study_name=None, user=None):

        return self.i_api_instance.download_individuals_by_attr(search_filter,
                                                                study_name=study_name)

    def download_individuals_by_attr(self, prop_name, prop_value,
                                     study_name=None, user=None):

        return self.i_api_instance.download_individuals_by_attr(prop_name,
                                                                prop_value,
                                                                study_name=study_name)

    def download_history(self, record_type, record_id, user=None):
        history = self.metadata_api_instance.download_history(record_type,
                                                               record_id)

        return history
