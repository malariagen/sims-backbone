import six

from swagger_server.models.location import Location  # noqa: E501
from swagger_server.models.locations import Locations  # noqa: E501
from swagger_server import util

from decimal import *
import logging

from local.base_local_api import BaseLocalApi

from backbone_server.controllers.location_controller  import LocationController

class LocalLocationApi(BaseLocalApi):

    def __init__(self, api_client=None):

        super().__init__(api_client)

        self.location_controller = LocationController()

    def create_location(self, location, user = None, token_info = None):
        """
        create_location
        Create a location
        :param location: 
        :type location: dict | bytes

        :rtype: Location
        """

        (ret, retcode) = self.location_controller.create_location(location, user,
                                                   self.location_controller.token_info(token_info))

        return self.create_response(ret, retcode, 'Location')

    def delete_location(self, locationId, user = None, token_info = None):
        """
        deletes an location
        
        :param locationId: ID of location to fetch
        :type locationId: str

        :rtype: None
        """
        (ret, retcode) = self.location_controller.delete_location(locationId, user,
                                                   self.location_controller.token_info(token_info))

        return self.create_response(ret, retcode)

    def download_gps_location(self, latitude, longitude, user = None, token_info = None):
        """
        fetches location(s) by GPS
        Params must be string as negative numbers not handled - https://github.com/pallets/werkzeug/issues/729 - also want to avoid using float
        :param latitude: Latitude of location to fetch
        :type latitude: str
        :param longitude: Longitude of location to fetch
        :type longitude: str

        :rtype: Location
        """
        (ret, retcode) = self.location_controller.download_gps_location(latitude, longitude, user,
                                                         self.location_controller.token_info(token_info))
        return self.create_response(ret, retcode, 'Location')

    def download_location(self, locationId, user = None, token_info = None):
        """
        fetches an location
        
        :param locationId: ID of location to fetch
        :type locationId: str

        :rtype: Location
        """
        (ret, retcode) = self.location_controller.download_location(locationId, user,
                                                     self.location_controller.token_info(token_info))

        return self.create_response(ret, retcode, 'Location')

    def download_locations(self, studyName=None, start=None, count=None, orderby=None, user = None,
                           token_info = None):
        """
        fetches locations
        
        :param studyName: restrict to a particular study
        :type studyName: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int
        :param orderby: how to order the result set
        :type orderby: str

        :rtype: Locations
        """
        (ret, retcode) = self.location_controller.download_locations(studyName, start, count, orderby, user,
                                                      self.location_controller.token_info(token_info))

        return self.create_response(ret, retcode, 'Locations')

    def download_partner_location(self, partnerId, user = None, token_info = None):
        """
        fetches location(s) by partner name
        
        :param partnerId: ID of location to fetch
        :type partnerId: str

        :rtype: Locations
        """
        (ret, retcode) = self.location_controller.download_partner_location(partnerId, user,
                                                             self.location_controller.token_info(token_info))
        return self.create_response(ret, retcode, 'Locations')


    def update_location(self, locationId, location, user = None, token_info = None):
        """
        updates an location
        
        :param locationId: ID of location to update
        :type locationId: str
        :param location: 
        :type location: dict | bytes

        :rtype: Location
        """

        (ret, retcode) = self.location_controller.update_location(locationId, location, user,
                                                   self.location_controller.token_info(token_info))

        return self.create_response(ret, retcode, 'Location')
