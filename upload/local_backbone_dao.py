import json
import requests
import os

import urllib.parse

import logging

from abstract_backbone_dao import AbstractBackboneDAO

from backbone_server.controllers.event_set_controller import EventSetController
from backbone_server.controllers.location_controller  import LocationController
from backbone_server.controllers.metadata_controller import MetadataController
from backbone_server.controllers.report_controller import ReportController
from backbone_server.controllers.sampling_event_controller  import SamplingEventController
from backbone_server.controllers.study_controller import StudyController
from backbone_server.controllers.original_sample_controller import OriginalSampleController
from backbone_server.controllers.derived_sample_controller import DerivedSampleController
from backbone_server.controllers.assay_datum_controller import AssayDatumController

from swagger_client.rest import ApiException

class LocalBackboneDAO(AbstractBackboneDAO):

    def __init__(self, user, auths):
        self._logger = logging.getLogger(__name__)
        self._user = user
        self._auths = auths

    def setup(self, config_file):

        self.es_api_instance = EventSetController()
        self.location_api_instance = LocationController()
        self.se_api_instance = SamplingEventController()
        self.os_api_instance = OriginalSampleController()
        self.ds_api_instance = DerivedSampleController()
        self.ad_api_instance = AssayDatumController()
        self.metadata_api_instance = MetadataController()

    def create_event_set(self, event_set_id):

        api_response, retcode = self.es_api_instance.create_event_set(event_set_id, user=self._user, auths=self._auths)

        if retcode >= 400:
            if retcode != 422: #Already exists
                print("Exception when calling EventSetApi->create_event_set: \n" )
                raise ApiException(status=retcode, reason='')

        return api_response

    def create_event_set_item(self, event_set_id, sampling_event_id):

        ret, retcode = self.es_api_instance.create_event_set_item(event_set_id, sampling_event_id, user=self._user, auths=self._auths)

        if retcode >= 400:
            #Probably because it already exists
            self._logger.debug("Error adding sample {} to event set {}".format(sampling_event_id, event_set_id))

        return ret

    def create_location(self, location):

        created, retcode = self.location_api_instance.create_location(location, user=self._user, auths=self._auths)

        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return created

    def create_sampling_event(self, sampling_event):

        created, retcode = self.se_api_instance.create_sampling_event(sampling_event, user=self._user, auths=self._auths)

        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return created

    def delete_sampling_event(self, sampling_event_id):

        ret, retcode = self.se_api_instance.delete_sampling_event(sampling_event_id, user=self._user, auths=self._auths)

        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        if retcode >= 400:
            raise ApiException(status=retcode, reason='')


    def download_gps_location(self, latitude, longitude):

        ret, retcode = self.location_api_instance.download_gps_location(latitude, longitude, user=self._user, auths=self._auths)

        self._logger.debug("GET /v1/location/gps/{}/{} {}".format(latitude,
                                                     longitude, retcode))
        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return ret

    def download_location(self, location_id):

        ret, retcode = self.location_api_instance.download_location(location_id, user=self._user, auths=self._auths)

        self._logger.debug("GET /v1/location/{} {}".format(location_id,
                                              retcode))
        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return ret

    def download_partner_location(self, partner_name):

        ret, retcode = self.location_api_instance.download_partner_location(partner_name, user=self._user, auths=self._auths)

        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return ret

    def download_sampling_event(self, sampling_event_id):

        existing, retcode = self.se_api_instance.download_sampling_event(sampling_event_id, user=self._user, auths=self._auths)

        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return existing

    def download_sampling_events_by_attr(self, attr_type, attr_value):

        found_events, retcode = self.se_api_instance.download_sampling_events_by_attr(attr_type,
                                                                                            urllib.parse.quote_plus(attr_value),
                                                                                            user=self._user, auths=self._auths)

        self._logger.debug("GET /v1/samplingEvents/attr/{}/{} {}".format(attr_type,
                                                                  attr_value, retcode))
        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return found_events

    def download_sampling_events_by_location(self, location_id):

        found_events, retcode = self.se_api_instance.download_sampling_events_by_location(location_id, start=0, count=0,
                                                                                            user=self._user, auths=self._auths)

        self._logger.debug("GET /v1/samplingEvents/location/{} {}".format(location_id,
                                                                  retcode))
        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return found_events

    def update_location(self, location_id, location):

        updated, retcode = self.location_api_instance.update_location(location_id, location, user=self._user, auths=self._auths)

        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return updated

    def update_sampling_event(self, sampling_event_id, sampling_event):
        ret, retcode = self.se_api_instance.update_sampling_event(sampling_event_id, sampling_event, user=self._user, auths=self._auths)

        self._logger.debug("POST /v1/samplingEvent/{} {}".format(sampling_event_id,
                                                    retcode))
        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return ret

    def merge_sampling_events(self, sampling_event_id1, sampling_event_id2):
        ret, retcode = self.se_api_instance.merge_sampling_events(sampling_event_id1,
                                                                  sampling_event_id2, user=self._user, auths=self._auths)

        self._logger.debug("PUT /v1/samplingEvent/merge/{}/{} {}".format(sampling_event_id1,
                                                                sampling_event_id2,
                                                    retcode))
        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return ret

    def get_country_metadata(self, country_value):
        metadata, retcode = self.metadata_api_instance.get_country_metadata(country_value, user=self._user, auths=self._auths)

        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return metadata

    def create_original_sample(self, original_sample):

        found_events, retcode = self.os_api_instance.create_original_sample(original_sample,
                                                                                            user=self._user, auths=self._auths)

        self._logger.debug("POST /v1/originalSample {} {}".format(original_sample
                                                                  , retcode))
        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return found_events

    def update_original_sample(self, original_sample_id, original_sample):

        found_events, retcode = self.os_api_instance.update_original_sample(original_sample_id, original_sample,
                                                                                            user=self._user, auths=self._auths)

        self._logger.debug("PUT /v1/originalSample/{} {} {}".format(original_sample_id, original_sample
                                                                  , retcode))
        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return found_events

    def merge_original_samples(self, original_sample_id1, original_sample_id2):

        found_events, retcode = self.os_api_instance.merge_original_samples(original_sample_id1,
                                                                            original_sample_id2,
                                                                                            user=self._user, auths=self._auths)

        self._logger.debug("PUT /v1/originalSample/{}/{} {} {}".format(original_sample_id1,
                                                                    original_sample_id2
                                                                  , retcode))
        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return found_events

    def delete_original_sample(self, original_sample_id):

        found_events, retcode = self.os_api_instance.delete_original_sample(original_sample_id,
                                                                                            user=self._user, auths=self._auths)

        self._logger.debug("DELETE /v1/originalSample/{}  {}".format(original_sample_id, retcode))
        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return found_events

    def download_original_sample(self, original_sample_id):

        found_events, retcode = self.os_api_instance.download_original_sample(original_sample_id,
                                                                              user=self._user, auths=self._auths)

        self._logger.debug("GET /v1/originalSample/{} {}".format(original_sample_id,
                                                                 retcode))
        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return found_events

    def download_original_samples_by_attr(self, attr_type, attr_value):

        found_events, retcode = self.os_api_instance.download_original_samples_by_attr(attr_type,
                                                                                            urllib.parse.quote_plus(attr_value),
                                                                                            user=self._user, auths=self._auths)

        self._logger.debug("GET /v1/originalSamples/attr/{}/{} {}".format(attr_type,
                                                                  attr_value, retcode))
        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return found_events

    def download_original_samples_by_os_attr(self, attr_type, attr_value):

        found_events, retcode = self.os_api_instance.download_original_samples_by_os_attr(attr_type,
                                                                                            urllib.parse.quote_plus(attr_value),
                                                                                            user=self._user, auths=self._auths)

        self._logger.debug("GET /v1/originalSamples/os/attr/{}/{} {}".format(attr_type,
                                                                  attr_value, retcode))
        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return found_events

    def create_derived_sample(self, derived_sample):

        found_events, retcode = self.ds_api_instance.create_derived_sample(derived_sample,
                                                                                            user=self._user, auths=self._auths)

        self._logger.debug("POST /v1/derivedSample {} {}".format(derived_sample
                                                                  , retcode))
        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return found_events

    def update_derived_sample(self, derived_sample_id, derived_sample):

        found_events, retcode = self.ds_api_instance.update_derived_sample(derived_sample_id, derived_sample,
                                                                                            user=self._user, auths=self._auths)

        self._logger.debug("PUT /v1/derivedSample/{} {} {}".format(derived_sample_id, derived_sample
                                                                  , retcode))
        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return found_events

    def merge_derived_samples(self, derived_sample_id1, derived_sample_id2):

        found_events, retcode = self.ds_api_instance.merge_derived_samples(derived_sample_id1,
                                                                           derived_sample_id2,
                                                                           user=self._user, auths=self._auths)

        self._logger.debug("PUT /v1/derivedSample/merge/{}/{} {}".format(derived_sample_id1,
                                                                         derived_sample_id2,
                                                                         retcode))
        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return found_events

    def delete_derived_sample(self, derived_sample_id):

        found_events, retcode = self.ds_api_instance.delete_derived_sample(derived_sample_id,
                                                                           user=self._user, auths=self._auths)

        self._logger.debug("DELETE /v1/derivedSample/{}  {}".format(derived_sample_id, retcode))
        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return found_events

    def download_derived_sample(self, derived_sample_id):

        found_events, retcode = self.ds_api_instance.download_derived_sample(derived_sample_id,
                                                                             user=self._user, auths=self._auths)

        self._logger.debug("GET /v1/derivedSample/{}  {}".format(derived_sample_id, retcode))
        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return found_events

    def download_derived_samples_by_attr(self, attr_type, attr_value):

        found_events, retcode = self.ds_api_instance.download_derived_samples_by_attr(attr_type,
                                                                                      urllib.parse.quote_plus(attr_value),
                                                                                      user=self._user, auths=self._auths)

        self._logger.debug("GET /v1/derivedSamples/attr/{}/{} {}".format(attr_type,
                                                                  attr_value, retcode))
        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return found_events


    def create_assay_datum(self, assay_datum):

        found_events, retcode = self.ad_api_instance.create_assay_datum(assay_datum,
                                                                                            user=self._user, auths=self._auths)

        self._logger.debug("POST /v1/derivedSample {} {}".format(assay_datum
                                                                  , retcode))
        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return found_events

    def update_assay_datum(self, assay_datum_id, assay_datum):

        found_events, retcode = self.ad_api_instance.update_assay_datum(assay_datum_id, assay_datum,
                                                                                            user=self._user, auths=self._auths)

        self._logger.debug("PUT /v1/derivedSample/{} {} {}".format(assay_datum_id, assay_datum
                                                                  , retcode))
        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return found_events

#    def merge_assay_data(self, assay_datum_id1, assay_datum_id2):
#
#        found_events, retcode = self.ad_api_instance.merge_assay_data(assay_datum_id1,
#                                                                            assay_datum_id2,
#                                                                                            user=self._user, auths=self._auths)
#
#        self._logger.debug("PUT /v1/derivedSample/{}/{} {} {}".format(assay_datum_id1,
#                                                                    assay_datum_id2
#                                                                  , retcode))
#        if retcode >= 400:
#            raise ApiException(status=retcode, reason='')
#
#        return found_events
#
    def delete_assay_datum(self, assay_datum_id):

        found_events, retcode = self.ad_api_instance.delete_assay_datum(assay_datum_id,
                                                                                            user=self._user, auths=self._auths)

        self._logger.debug("DELETE /v1/derivedSample/{}  {}".format(assay_datum_id, retcode))
        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return found_events

    def download_assay_data_by_attr(self, attr_type, attr_value):

        found_events, retcode = self.ad_api_instance.download_assay_data_by_attr(attr_type,
                                                                                            urllib.parse.quote_plus(attr_value),
                                                                                            user=self._user, auths=self._auths)

        self._logger.debug("GET /v1/derivedSamples/attr/{}/{} {}".format(attr_type,
                                                                  attr_value, retcode))
        if retcode >= 400:
            raise ApiException(status=retcode, reason='')

        return found_events

