import logging

from decimal import Decimal, InvalidOperation

from backbone_server.location.post import LocationPost
from backbone_server.location.put import LocationPut
from backbone_server.location.get import LocationGetById
from backbone_server.location.get_by_attr import LocationGetByAttr
from backbone_server.location.gets import LocationsGet
from backbone_server.location.delete import LocationDelete
from backbone_server.location.get_by_name import LocationGetByPartnerName
from backbone_server.location.get_by_gps import LocationGetByGPS

from backbone_server.controllers.base_controller import BaseController

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.permission_exception import PermissionException

from backbone_server.controllers.decorators import apply_decorators


@apply_decorators
class LocationController(BaseController):

    def create_location(self, location, studies=None, user=None, auths=None):
        """
        create_location
        Create a location
        :param location:
        :type location: dict | bytes

        :rtype: Location
        """

        retcode = 201
        loc = None

        try:
            post = LocationPost(self.get_connection())

            loc = post.post(location, studies)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug(
                "create_location: {}".format(repr(dke)))
            retcode = 422
        except PermissionException as pme:
            logging.getLogger(__name__).debug(
                "create_location: {}, {}".format(repr(pme), user))
            retcode = 403
            loc = str(pme)

        return loc, retcode

    def delete_location(self, location_id, studies=None, user=None, auths=None):
        """
        deletes an location

        :param location_id: ID of location to fetch
        :type location_id: str

        :rtype: None
        """

        delete = LocationDelete(self.get_connection())

        retcode = 200

        try:
            delete.delete(location_id, studies)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "delete_location: {}".format(repr(dme)))
            retcode = 404
        except PermissionException as pme:
            logging.getLogger(__name__).debug(
                "delete_location: {}, {}".format(repr(pme), user))
            retcode = 403
            loc = str(pme)

        return None, retcode

    def download_gps_location(self, latitude, longitude, studies=None, user=None, auths=None):
        """
        fetches location(s) by GPS
        Params must be string as negative numbers not handled - https://github.com/pallets/werkzeug/issues/729 - also want to avoid using float
        :param latitude: Latitude of location to fetch
        :type latitude: str
        :param longitude: Longitude of location to fetch
        :type longitude: str

        :rtype: Location
        """

        get = LocationGetByGPS(self.get_connection())

        retcode = 200
        loc = None

        try:
            lat = Decimal(latitude)
            lng = Decimal(longitude)
            loc = get.get(lat, lng, studies)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "download_partner_location: {}".format(repr(dme)))
            retcode = 404
            loc = str(dme)
        except InvalidOperation as nfe:
            logging.getLogger(__name__).debug(
                "download_partner_location: {}".format(repr(nfe)))
            retcode = 422
            loc = str(nfe)
        except PermissionException as pme:
            logging.getLogger(__name__).debug(
                "download_gps_location: {}, {}".format(repr(pme), user))
            retcode = 403
            loc = str(pme)

        return loc, retcode

    def download_location(self, location_id, studies=None, user=None, auths=None):
        """
        fetches an location

        :param locationId: ID of location to fetch
        :type locationId: str

        :rtype: Location
        """

        get = LocationGetById(self.get_connection())

        retcode = 200
        loc = None

        try:
            loc = get.get(location_id, studies)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "download_location: {}".format(repr(dme)))
            retcode = 404
            loc = str(dme)
        except PermissionException as pme:
            logging.getLogger(__name__).debug(
                "download_location: {}, {}".format(repr(pme), user))
            retcode = 403
            loc = str(pme)

        return loc, retcode

    def download_locations_by_attr(self, attr_type, attr_value, study_code,
                                  studies=None, user=None, auths=None):
        """
        fetches an location

        :param locationId: ID of location to fetch
        :type locationId: str

        :rtype: Location
        """

        get = LocationGetByAttr(self.get_connection())

        retcode = 200
        loc = None

        loc = get.get(attr_type, attr_value, study_code, studies)

        return loc, retcode

    def download_locations(self, study_name=None, start=None, count=None,
                           orderby=None, studies=None, user=None,
                           auths=None):
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

        get = LocationsGet(self.get_connection())

        retcode = 200
        loc = None

        loc = get.get(study_name, studies, start, count, orderby)

        return loc, retcode

    def download_partner_location(self, partner_id, studies=None, user=None, auths=None):
        """
        fetches location(s) by partner name

        :param partner_id: ID of location to fetch
        :type partner_id: str

        :rtype: Locations
        """

        get = LocationGetByPartnerName(self.get_connection())

        retcode = 200
        loc = None

        try:
            loc = get.get(partner_id, studies)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "download_partner_location: {}".format(repr(dme)))
            retcode = 404
            loc = str(dme)

        return loc, retcode

    def update_location(self, location_id, location, studies=None, user=None, auths=None):
        """
        updates an location

        :param location_id: ID of location to update
        :type location_id: str
        :param location:
        :type location: dict | bytes

        :rtype: Location
        """

        retcode = 200
        loc = None

        try:
            put = LocationPut(self.get_connection())

            loc = put.put(location_id, location, studies)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug(
                "update_location: {}".format(repr(dke)))
            retcode = 422
            loc = str(dke)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "update_location: {}".format(repr(dme)))
            retcode = 404
            loc = str(dme)
        except PermissionException as pme:
            logging.getLogger(__name__).debug(
                "update_location: {}, {}".format(repr(pme), user))
            retcode = 403
            loc = str(pme)

        return loc, retcode
