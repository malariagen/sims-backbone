import six

from openapi_server.models.location import Location  # noqa: E501
from openapi_server.models.locations import Locations  # noqa: E501
from openapi_server import util

from decimal import *
import logging

from local.base_local_api import BaseLocalApi

from backbone_server.controllers.location_controller import LocationController


class LocalLocationApi(BaseLocalApi):

    def __init__(self, api_client, user, auths, method):

        super().__init__(api_client, user, auths, method)

        self.location_controller = LocationController()

    def create_location(self, location):
        """
        create_location
        Create a location
        :param location:
        :type location: dict | bytes

        :rtype: Location
        """

        (ret, retcode) = self.location_controller.create_location(location, self._user,
                                                                  self.location_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'Location')

    def delete_location(self, location_id):
        """
        deletes an location

        :param locationId: ID of location to fetch
        :type locationId: str

        :rtype: None
        """
        (ret, retcode) = self.location_controller.delete_location(location_id, self._user,
                                                                  self.location_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode)

    def download_gps_location(self, latitude, longitude):
        """
        fetches location(s) by GPS
        Params must be string as negative numbers not handled - https://github.com/pallets/werkzeug/issues/729 - also want to avoid using float
        :param latitude: Latitude of location to fetch
        :type latitude: str
        :param longitude: Longitude of location to fetch
        :type longitude: str

        :rtype: Location
        """
        (ret, retcode) = self.location_controller.download_gps_location(latitude, longitude, self._user,
                                                                        self.location_controller.token_info(self.auth_tokens()))
        return self.create_response(ret, retcode, 'Locations')

    def download_location(self, location_id):
        """
        fetches an location

        :param location_id: ID of location to fetch
        :type location_id: str

        :rtype: Location
        """
        (ret, retcode) = self.location_controller.download_location(location_id, self._user,
                                                                    self.location_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'Location')

    def download_locations(self, study_name=None, start=None, count=None, orderby=None):
        """
        fetches locations

        :param study_name: restrict to a particular study
        :type study_name: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int
        :param orderby: how to order the result set
        :type orderby: str

        :rtype: Locations
        """
        (ret, retcode) = self.location_controller.download_locations(study_name, start, count, orderby, self._user,
                                                                     self.location_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'Locations')

    def download_partner_location(self, partner_id):
        """
        fetches location(s) by partner name

        :param partnerId: ID of location to fetch
        :type partnerId: str

        :rtype: Locations
        """
        (ret, retcode) = self.location_controller.download_partner_location(partner_id, self._user,
                                                                            self.location_controller.token_info(self.auth_tokens()))
        return self.create_response(ret, retcode, 'Locations')

    def update_location(self, location_id, location):
        """
        updates an location

        :param location_id: ID of location to update
        :type location_id: str
        :param location:
        :type location: dict | bytes

        :rtype: Location
        """

        (ret, retcode) = self.location_controller.update_location(location_id, location, self._user,
                                                                  self.location_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'Location')
