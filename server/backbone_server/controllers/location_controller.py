import logging

from decimal import *

from backbone_server.location.post import LocationPost
from backbone_server.location.put import LocationPut
from backbone_server.location.get import LocationGetById
from backbone_server.location.gets import LocationsGet
from backbone_server.location.delete import LocationDelete
from backbone_server.location.get_by_name import LocationGetByPartnerName
from backbone_server.location.get_by_gps import LocationGetByGPS

from backbone_server.controllers.base_controller  import BaseController

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.permission_exception import PermissionException


class LocationController(BaseController):

    def create_location(self, location, user = None, auths = None):
        """
        create_location
        Create a location
        :param location: 
        :type location: dict | bytes

        :rtype: Location
        """

        try:
            self.check_permissions(None, auths)
        except PermissionException as pe:
            self.log_action(user, 'create_location', None, location, None, 403)
            return pe.message, 403

        retcode = 200
        loc = None

        try:
            post = LocationPost(self.get_connection())

            loc = post.post(location)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).error("create_location: {}".format(repr(dke)))
            retcode = 422

        self.log_action(user, 'create_location', None, location, loc, retcode)

        return loc, retcode


    def delete_location(self, locationId, user = None, auths = None):
        """
        deletes an location
        
        :param locationId: ID of location to fetch
        :type locationId: str

        :rtype: None
        """

        try:
            self.check_permissions(None, auths)
        except PermissionException as pe:
            self.log_action(user, 'delete_location', locationId, None, None, 403)

            return pe.message, 403

        delete = LocationDelete(self.get_connection())

        retcode = 200
        loc = None

        try:
            delete.delete(locationId)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("delete_location: {}".format(repr(dme)))
            retcode = 404

        self.log_action(user, 'delete_location', locationId, None, None, retcode)

        return None, retcode


    def download_gps_location(self, latitude, longitude, user = None, auths = None):
        """
        fetches location(s) by GPS
        Params must be string as negative numbers not handled - https://github.com/pallets/werkzeug/issues/729 - also want to avoid using float
        :param latitude: Latitude of location to fetch
        :type latitude: str
        :param longitude: Longitude of location to fetch
        :type longitude: str

        :rtype: Location
        """

        try:
            self.check_permissions(None, auths)
        except PermissionException as pe:
            self.log_action(user, 'download_gps_location', None, None, None, 403)

            return pe.message, 403

        get = LocationGetByGPS(self.get_connection())

        retcode = 200
        loc = None

        try:
            lat = Decimal(latitude)
            lng = Decimal(longitude)
            loc = get.get(lat, lng)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_partner_location: {}".format(repr(dme)))
            retcode = 404
        except InvalidOperation as nfe:
            logging.getLogger(__name__).error("download_partner_location: {}".format(repr(nfe)))
            retcode = 422

        self.log_action(user, 'download_gps_location', None, None, loc, retcode)

        return loc, retcode

    def download_location(self, locationId, user = None, auths = None):
        """
        fetches an location
        
        :param locationId: ID of location to fetch
        :type locationId: str

        :rtype: Location
        """

        try:
            self.check_permissions(None, auths)
        except PermissionException as pe:
            self.log_action(user, 'download_location', locationId, None, None, 403)
            return pe.message, 403

        get = LocationGetById(self.get_connection())

        retcode = 200
        loc = None

        try:
            loc = get.get(locationId)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_location: {}".format(repr(dme)))
            retcode = 404

        self.log_action(user, 'download_location', locationId, None, loc, retcode)

        return loc, retcode


    def download_locations(self, studyName=None, start=None, count=None, orderby=None, user = None,
                          auths = None):
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

        try:
            self.check_permissions(None, auths)
        except PermissionException as pe:
            self.log_action(user, 'download_locations', None, None, None, 403)
            return pe.message, 403

        get = LocationsGet(self.get_connection())

        retcode = 200
        loc = None

        loc = get.get(studyName, start, count, orderby)

        self.log_action(user, 'download_locations', None, None, loc, retcode)

        return loc, retcode


    def download_partner_location(self, partnerId, user = None, auths = None):
        """
        fetches location(s) by partner name
        
        :param partnerId: ID of location to fetch
        :type partnerId: str

        :rtype: Locations
        """

        try:
            self.check_permissions(None, auths)
        except PermissionException as pe:
            self.log_action(user, 'download_partner_location', partnerId, None, None, 403)
            return pe.message, 403

        get = LocationGetByPartnerName(self.get_connection())

        retcode = 200
        loc = None

        try:
            loc = get.get(partnerId)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_partner_location: {}".format(repr(dme)))
            retcode = 404

        self.log_action(user, 'download_partner_location', partnerId, None, loc, retcode)

        return loc, retcode


    def update_location(self, locationId, location, user = None, auths = None):
        """
        updates an location
        
        :param locationId: ID of location to update
        :type locationId: str
        :param location: 
        :type location: dict | bytes

        :rtype: Location
        """

        try:
            self.check_permissions(None, auths)
        except PermissionException as pe:
            self.log_action(user, 'update_location', locationId, location, None, 403)
            return pe.message, 403


        retcode = 200
        loc = None

        try:
            put = LocationPut(self.get_connection())

            loc = put.put(locationId, location)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).error("update_location: {}".format(repr(dke)))
            retcode = 422
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("update_location: {}".format(repr(dme)))
            retcode = 404

        self.log_action(user, 'update_location', locationId, location, loc, retcode)

        return loc, retcode
