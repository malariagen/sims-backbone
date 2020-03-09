import json
import requests
import os

import urllib.parse
from urllib3.response import HTTPResponse
import logging

from abstract_backbone_dao import AbstractBackboneDAO

from backbone_server.controllers.event_set_controller import EventSetController
from backbone_server.controllers.location_controller import LocationController
from backbone_server.controllers.metadata_controller import MetadataController
from backbone_server.controllers.report_controller import ReportController
from backbone_server.controllers.sampling_event_controller import SamplingEventController
from backbone_server.controllers.study_controller import StudyController
from backbone_server.controllers.original_sample_controller import OriginalSampleController
from backbone_server.controllers.derivative_sample_controller import DerivativeSampleController
from backbone_server.controllers.assay_datum_controller import AssayDatumController
from backbone_server.controllers.individual_controller import IndividualController

from openapi_client.rest import ApiException


class LocalBackboneDAO(AbstractBackboneDAO):

    def __init__(self, user, auths):
        self._logger = logging.getLogger(__name__)
        self._user = user
        self._auths = auths
        self.es_api_instance = EventSetController()
        self.location_api_instance = LocationController()
        self.se_api_instance = SamplingEventController()
        self.os_api_instance = OriginalSampleController()
        self.ds_api_instance = DerivativeSampleController()
        self.ad_api_instance = AssayDatumController()
        self.metadata_api_instance = MetadataController()
        self.study_api_instance = StudyController()
        self.i_api_instance = IndividualController()

    def setup(self, config):
        pass

    def create_event_set(self, event_set_id, user=None):

        if not user:
            user = self._user

        api_response, retcode = self.es_api_instance.create_event_set(
            event_set_id, user=user, auths=self._auths)

        if retcode >= 400:
            if retcode != 422:  # Already exists
                self._logger.debug(
                    "Exception when calling EventSetApi->create_event_set: \n")
                raise ApiException(http_resp=HTTPResponse(
                    body=api_response, status=retcode))

        return api_response

    def delete_event_set(self, event_set_id, user=None):

        if not user:
            user = self._user

        api_response, retcode = self.es_api_instance.delete_event_set(
            event_set_id, user=user, auths=self._auths)

        if retcode >= 400:
            if retcode != 422:  # Already exists
                self._logger.debug(
                    "Exception when calling EventSetApi->delete_event_set: \n")
                raise ApiException(http_resp=HTTPResponse(
                    body=api_response, status=retcode))

        return api_response

    def download_event_set(self, event_set_id, studies=None, start=None, count=None,
                           user=None):

        if not user:
            user = self._user

        api_response, retcode = self.es_api_instance.download_event_set(
            event_set_id, studies=studies, start=start, count=count, user=user, auths=self._auths)

        if retcode >= 400:
            if retcode != 422:  # Already exists
                self._logger.debug(
                    "Exception when calling EventSetApi->download_event_set: \n")
                raise ApiException(http_resp=HTTPResponse(
                    body=api_response, status=retcode))

        return api_response

    def create_event_set_item(self, event_set_id, sampling_event_id, user=None):

        if not user:
            user = self._user

        ret, retcode = self.es_api_instance.create_event_set_item(
            event_set_id, sampling_event_id, user=user, auths=self._auths)

        if retcode >= 400:
            # Probably because it already exists
            self._logger.debug("Error adding sample %s to event set %s", sampling_event_id, event_set_id)

        return ret

    def delete_event_set_item(self, event_set_id, sampling_event_id, user=None):

        if not user:
            user = self._user

        ret, retcode = self.es_api_instance.delete_event_set_item(
            event_set_id, sampling_event_id, user=user, auths=self._auths)

        if retcode >= 400:
            # Probably because it already exists
            self._logger.debug("Error deleting sample %s to event set %s", sampling_event_id, event_set_id)

        return ret
    def create_location(self, location, user=None):

        if not user:
            user = self._user

        created, retcode = self.location_api_instance.create_location(
            location, user=user, auths=self._auths)

        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=created, status=retcode))

        return created

    def create_sampling_event(self, sampling_event, user=None):

        if not user:
            user = self._user

        created, retcode = self.se_api_instance.create_sampling_event(
            sampling_event, user=user, auths=self._auths)

        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=f'"{created}"\n', status=retcode))

        return created

    def delete_sampling_event(self, sampling_event_id, user=None):

        if not user:
            user = self._user

        ret, retcode = self.se_api_instance.delete_sampling_event(
            sampling_event_id, user=user, auths=self._auths)

        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=ret, status=retcode))

    def download_gps_location(self, latitude, longitude, user=None):

        if not user:
            user = self._user

        ret, retcode = self.location_api_instance.download_gps_location(
            latitude, longitude, user=user, auths=self._auths)

        self._logger.debug("GET /v1/location/gps/{}/{} {}".format(latitude,
                                                                  longitude, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=ret, status=retcode))

        return ret

    def download_location(self, location_id, user=None):

        if not user:
            user = self._user

        ret, retcode = self.location_api_instance.download_location(
            location_id, user=user, auths=self._auths)

        self._logger.debug("GET /v1/location/{} {}".format(location_id,
                                                           retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=ret, status=retcode))

        return ret

    def delete_location(self, location_id, user=None):

        if not user:
            user = self._user

        ret, retcode = self.location_api_instance.delete_location(
            location_id, studies=None, user=user, auths=self._auths)

        self._logger.debug("DELETE /v1/location/%s %s", location_id, retcode)
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=ret, status=retcode))

        return ret

    def download_locations_by_attr(self, attr_type, attr_value,
                                   study_name=None, user=None):

        if not user:
            user = self._user

        ret, retcode = self.location_api_instance.download_locations_by_attr(
            attr_type, attr_value, study_name,
            user=user, auths=self._auths)

        self._logger.debug("GET /v1/locations/attr/{}/{} {}".format(attr_type,
                                                                    attr_value,
                                                                    retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=ret, status=retcode))

        return ret

    def download_partner_location(self, partner_name, user=None):

        if not user:
            user = self._user

        ret, retcode = self.location_api_instance.download_partner_location(
            partner_name, user=user, auths=self._auths)

        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=ret, status=retcode))

        return ret

    def download_sampling_event(self, sampling_event_id, user=None):

        if not user:
            user = self._user

        existing, retcode = self.se_api_instance.download_sampling_event(
            sampling_event_id, user=user, auths=self._auths)

        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=existing, status=retcode))

        return existing

    def download_sampling_events_by_event_set(self, event_set_name,
                                              studies=None, start=None,
                                              count=None, user=None):

        if not user:
            user = self._user

        found_events, retcode = self.se_api_instance.download_sampling_events_by_event_set(urllib.parse.quote_plus(event_set_name),
                                                                                           studies=studies,
                                                                                           start=start,
                                                                                           count=count,
                                                                                           user=user,
                                                                                           auths=self._auths)

        self._logger.debug(
            "GET /v1/samplingEvents/event_set/{} {}".format(event_set_name, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def download_sampling_events_by_attr(self, attr_type, attr_value, user=None):

        if not user:
            user = self._user

        found_events, retcode = self.se_api_instance.download_sampling_events_by_attr(attr_type,
                                                                                      urllib.parse.quote_plus(
                                                                                          attr_value),
                                                                                      user=user, auths=self._auths)

        self._logger.debug("GET /v1/samplingEvents/attr/{}/{} {}".format(attr_type,
                                                                         attr_value, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def download_sampling_events_by_study(self, study_name, studies=None, start=None,
                                          count=None, user=None):

        if not user:
            user = self._user

        found_events, retcode = self.se_api_instance.download_sampling_events_by_study(study_name,
                                                                                       studies=studies,
                                                                                       start=start,
                                                                                       count=count,
                                                                                       user=user, auths=self._auths)

        self._logger.debug("GET /v1/samplingEvents/study/{} {}".format(study_name,
                                                                       retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def download_sampling_events_by_os_attr(self, attr_type, attr_value,
                                            user=None):

        if not user:
            user = self._user

        found_events, retcode = self.se_api_instance.download_sampling_events_by_os_attr(attr_type,
                                                                                         urllib.parse.quote_plus(
                                                                                             attr_value),
                                                                                         studies=None,
                                                                                         user=user, auths=self._auths)

        self._logger.debug("GET /v1/samplingEvents/os/attr/{}/{} {}".format(attr_type,
                                                                            attr_value, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def download_sampling_events_by_location(self, location_id, user=None):

        if not user:
            user = self._user

        found_events, retcode = self.se_api_instance.download_sampling_events_by_location(location_id, start=0, count=0,
                                                                                          user=user, auths=self._auths)

        self._logger.debug("GET /v1/samplingEvents/location/{} {}".format(location_id,
                                                                          retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def update_location(self, location_id, location, user=None):

        if not user:
            user = self._user

        updated, retcode = self.location_api_instance.update_location(
            location_id, location, user=user, auths=self._auths)

        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=updated, status=retcode))

        return updated

    def update_sampling_event(self, sampling_event_id, sampling_event,
                              user=None):

        if not user:
            user = self._user
        ret, retcode = self.se_api_instance.update_sampling_event(
            sampling_event_id, sampling_event, user=user, auths=self._auths)

        self._logger.debug("POST /v1/samplingEvent/{} {}".format(sampling_event_id,
                                                                 retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=f'"{ret}"\n', status=retcode))

        return ret

    def merge_sampling_events(self, sampling_event_id1, sampling_event_id2,
                              user=None):

        if not user:
            user = self._user
        ret, retcode = self.se_api_instance.merge_sampling_events(sampling_event_id1,
                                                                  sampling_event_id2,
                                                                  user=user, auths=self._auths)

        self._logger.debug("PUT /v1/samplingEvent/merge/{}/{} {}".format(sampling_event_id1,
                                                                         sampling_event_id2,
                                                                         retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=ret, status=retcode))

        return ret

    def get_country_metadata(self, country_value, user=None):

        if not user:
            user = self._user
        metadata, retcode = self.metadata_api_instance.get_country_metadata(
            country_value, user=user, auths=self._auths)

        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=metadata, status=retcode))

        return metadata

    def create_original_sample(self, original_sample, user=None):

        if not user:
            user = self._user

        found_events, retcode = self.os_api_instance.create_original_sample(original_sample,
                                                                            user=user, auths=self._auths)

        self._logger.debug(
            "POST /v1/originalSample {} {}".format(original_sample, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def update_original_sample(self, original_sample_id, original_sample,
                               user=None):

        if not user:
            user = self._user

        found_events, retcode = self.os_api_instance.update_original_sample(original_sample_id, original_sample,
                                                                            user=user, auths=self._auths)

        self._logger.debug(
            "PUT /v1/originalSample/{} {} {}".format(original_sample_id, original_sample, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def merge_original_samples(self, original_sample_id1, original_sample_id2,
                              user=None):

        if not user:
            user = self._user

        found_events, retcode = self.os_api_instance.merge_original_samples(original_sample_id1,
                                                                            original_sample_id2,
                                                                            user=user, auths=self._auths)

        self._logger.debug("PUT /v1/originalSample/{}/{} {}".format(original_sample_id1,
                                                                    original_sample_id2, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def delete_original_sample(self, original_sample_id, user=None):

        if not user:
            user = self._user

        found_events, retcode = self.os_api_instance.delete_original_sample(original_sample_id,
                                                                            user=user, auths=self._auths)

        self._logger.debug(
            "DELETE /v1/originalSample/{}  {}".format(original_sample_id, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def download_original_sample(self, original_sample_id, studies=None, user=None):

        if not user:
            user = self._user

        found_events, retcode = self.os_api_instance.download_original_sample(original_sample_id,
                                                                              studies=studies,
                                                                              user=user, auths=self._auths)

        self._logger.debug("GET /v1/originalSample/{} {}".format(original_sample_id,
                                                                 retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def download_original_samples(self, search_filter, start=None, count=None, user=None):

        if not user:
            user = self._user

        found_events, retcode = self.os_api_instance.download_original_samples(search_filter,
                                                                               start=start,
                                                                               count=count,
                                                                               user=user, auths=self._auths)

        self._logger.debug(f"GET /v1/originalSamples/{search_filter} {retcode}")

        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def download_original_samples_by_attr(self, attr_type, attr_value,
                                          user=None):

        if not user:
            user = self._user

        found_events, retcode = self.os_api_instance.download_original_samples_by_attr(attr_type,
                                                                                       urllib.parse.quote_plus(
                                                                                           attr_value),
                                                                                       user=user, auths=self._auths)

        self._logger.debug("GET /v1/originalSamples/attr/{}/{} {}".format(attr_type,
                                                                          attr_value, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def download_original_samples_by_event_set(self, event_set_id, start=None,
                                               count=None, user=None):

        if not user:
            user = self._user

        found_events, retcode = self.os_api_instance.download_original_samples_by_event_set(urllib.parse.quote_plus(event_set_id),
                                                                                            start,
                                                                                            count,
                                                                                            user=user, auths=self._auths)

        self._logger.debug(
            "GET /v1/originalSamples/eventSetId/{} {}".format(event_set_id, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def download_original_samples_by_os_attr(self, attr_type, attr_value,
                                             user=None):

        if not user:
            user = self._user

        found_events, retcode = self.os_api_instance.download_original_samples_by_os_attr(attr_type,
                                                                                          urllib.parse.quote_plus(
                                                                                              attr_value),
                                                                                          user=user, auths=self._auths)

        self._logger.debug("GET /v1/originalSamples/os/attr/{}/{} {}".format(attr_type,
                                                                             attr_value, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def create_derivative_sample(self, derivative_sample, user=None):

        if not user:
            user = self._user

        found_events, retcode = self.ds_api_instance.create_derivative_sample(derivative_sample,
                                                                              user=user, auths=self._auths)

        self._logger.debug(
            "POST /v1/derivativeSample {} {}".format(derivative_sample, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def update_derivative_sample(self, derivative_sample_id, derivative_sample,
                                user=None):

        if not user:
            user = self._user

        found_events, retcode = self.ds_api_instance.update_derivative_sample(derivative_sample_id, derivative_sample,
                                                                              user=user, auths=self._auths)

        self._logger.debug("PUT /v1/derivativeSample/{} {} {}".format(
            derivative_sample_id, derivative_sample, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def merge_derivative_samples(self, derivative_sample_id1,
                                 derivative_sample_id2, user=None):

        if not user:
            user = self._user

        found_events, retcode = self.ds_api_instance.merge_derivative_samples(derivative_sample_id1,
                                                                              derivative_sample_id2,
                                                                              user=user, auths=self._auths)

        self._logger.debug("PUT /v1/derivativeSample/merge/{}/{} {}".format(derivative_sample_id1,
                                                                            derivative_sample_id2,
                                                                            retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def delete_derivative_sample(self, derivative_sample_id, user=None):

        if not user:
            user = self._user

        found_events, retcode = self.ds_api_instance.delete_derivative_sample(derivative_sample_id,
                                                                              user=user, auths=self._auths)

        self._logger.debug(
            "DELETE /v1/derivativeSample/{}  {}".format(derivative_sample_id, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def download_derivative_sample(self, derivative_sample_id, user=None):

        if not user:
            user = self._user

        found_events, retcode = self.ds_api_instance.download_derivative_sample(derivative_sample_id,
                                                                                user=user, auths=self._auths)

        self._logger.debug(
            "GET /v1/derivativeSample/{}  {}".format(derivative_sample_id, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def download_derivative_samples_by_attr(self, attr_type, attr_value,
                                            user=None):

        if not user:
            user = self._user

        found_events, retcode = self.ds_api_instance.download_derivative_samples_by_attr(attr_type,
                                                                                         urllib.parse.quote_plus(
                                                                                             attr_value),
                                                                                         user=user, auths=self._auths)

        self._logger.debug("GET /v1/derivativeSamples/attr/{}/{} {}".format(attr_type,
                                                                            attr_value, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def download_derivative_samples_by_os_attr(self, attr_type, attr_value,
                                               user=None):

        if not user:
            user = self._user

        found_events, retcode = self.ds_api_instance.download_derivative_samples_by_os_attr(attr_type,
                                                                                            urllib.parse.quote_plus(
                                                                                                attr_value),
                                                                                            user=user, auths=self._auths)

        self._logger.debug("GET /v1/derivativeSamples/os/attr/{}/{} {}".format(attr_type,
                                                                               attr_value, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def create_assay_datum(self, assay_datum, user=None):

        if not user:
            user = self._user

        found_events, retcode = self.ad_api_instance.create_assay_datum(assay_datum,
                                                                        user=user, auths=self._auths)

        self._logger.debug(
            "POST /v1/derivativeSample {} {}".format(assay_datum, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def update_assay_datum(self, assay_datum_id, assay_datum, user=None):

        if not user:
            user = self._user

        found_events, retcode = self.ad_api_instance.update_assay_datum(assay_datum_id, assay_datum,
                                                                        user=user, auths=self._auths)

        self._logger.debug(
            "PUT /v1/derivativeSample/{} {} {}".format(assay_datum_id, assay_datum, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

#    def merge_assay_data(self, assay_datum_id1, assay_datum_id2, user=None):

#    if not user:
#        user = self._user
#
#        found_events, retcode = self.ad_api_instance.merge_assay_data(assay_datum_id1,
#                                                                            assay_datum_id2,
#                                                                                            user=self._user, auths=self._auths)
#
#        self._logger.debug("PUT /v1/derivativeSample/{}/{} {} {}".format(assay_datum_id1,
#                                                                    assay_datum_id2
#                                                                  , retcode))
#        if retcode >= 400:
#            raise ApiException(http_resp=HTTPResponse(body=ret, status=retcode))
#
#        return found_events
#
    def delete_assay_datum(self, assay_datum_id, user=None):

        if not user:
            user = self._user

        found_events, retcode = self.ad_api_instance.delete_assay_datum(assay_datum_id,
                                                                        user=user, auths=self._auths)

        self._logger.debug(
            "DELETE /v1/derivativeSample/{}  {}".format(assay_datum_id, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def download_assay_data_by_attr(self, attr_type, attr_value, user=None):

        if not user:
            user = self._user

        found_events, retcode = self.ad_api_instance.download_assay_data_by_attr(attr_type,
                                                                                 urllib.parse.quote_plus(
                                                                                     attr_value),
                                                                                 user=user, auths=self._auths)

        self._logger.debug("GET /v1/derivativeSamples/attr/{}/{} {}".format(attr_type,
                                                                            attr_value, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def download_study(self, study_code, user=None):

        if not user:
            user = self._user

        ret_data, retcode = self.study_api_instance.download_study(study_code,
                                                                   studies=None,
                                                                   user=user,
                                                                   auths=self._auths)
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=ret_data, status=retcode))

        return ret_data

    def download_studies(self, studies=None, user=None, auths=None):

        if not user:
            user = self._user

        ret_data, retcode = self.study_api_instance.download_studies(studies=studies, user=user,
                                                                     auths=self._auths)
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=ret_data, status=retcode))

        return ret_data

    def update_study(self, study_code, study_detail, user=None):

        if not user:
            user = self._user
        ret_data, retcode = self.study_api_instance.update_study(study_code,
                                                                 study_detail, user=user,
                                                                 auths=self._auths)
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=ret_data, status=retcode))

        return ret_data

    def create_individual(self, individual, user=None):

        if not user:
            user = self._user

        found_events, retcode = self.i_api_instance.create_individual(individual,
                                                                      user=user, auths=self._auths)

        self._logger.debug(
            "POST /v1/individual {} {}".format(individual, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def update_individual(self, individual_id, individual, user=None):

        if not user:
            user = self._user

        found_events, retcode = self.i_api_instance.update_individual(individual_id, individual,
                                                                      user=user, auths=self._auths)

        self._logger.debug(
            "PUT /v1/individual/{} {} {}".format(individual_id, individual, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def merge_individuals(self, individual_id1, individual_id2, user=None):

        if not user:
            user = self._user

        found_events, retcode = self.i_api_instance.merge_individuals(individual_id1,
                                                                      individual_id2,
                                                                      user=user, auths=self._auths)

        self._logger.debug("PUT /v1/individual/{}/{} {}".format(individual_id1,
                                                                individual_id2, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def delete_individual(self, individual_id, user=None):

        if not user:
            user = self._user

        found_events, retcode = self.i_api_instance.delete_individual(individual_id,
                                                                      user=user, auths=self._auths)

        self._logger.debug(
            "DELETE /v1/individual/{}  {}".format(individual_id, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def download_individual(self, individual_id, user=None):

        if not user:
            user = self._user

        found_events, retcode = self.i_api_instance.download_individual(individual_id,
                                                                        user=user, auths=self._auths)

        self._logger.debug("GET /v1/individual/{} {}".format(individual_id,
                                                             retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def download_individuals(self, search_filter, study_name=None,
                                     user=None):

        if not user:
            user = self._user

        found_events, retcode = self.i_api_instance.download_individuals(search_filter,
                                                                         study_name=study_name,
                                                                         user=user, auths=self._auths)

        self._logger.debug("GET /v1/individuals/{} {}".format(search_filter, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def download_individuals_by_attr(self, prop_name, prop_value, study_name,
                                     user=None):

        if not user:
            user = self._user

        found_events, retcode = self.i_api_instance.download_individuals_by_attr(prop_name,
                                                                                 urllib.parse.quote_plus(
                                                                                     prop_value),
                                                                                 study_name,
                                                                                 user=user, auths=self._auths)

        self._logger.debug("GET /v1/individuals/attr/{}/{} {}".format(prop_name,
                                                                      prop_value, retcode))
        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=found_events, status=retcode))

        return found_events

    def download_history(self, record_type, record_id, studies=None, user=None, auths=None):
        if not user:
            user = self._user

        history, retcode = self.metadata_api_instance.download_history(record_type,
                                                                       str(record_id),
                                                                       user=user,
                                                                       auths=self._auths)

        if retcode >= 400:
            raise ApiException(http_resp=HTTPResponse(
                body=history, status=retcode))

        return history
