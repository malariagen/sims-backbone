import logging

from decimal import Decimal, InvalidOperation

from backbone_server.model.location import BaseLocation

from backbone_server.controllers.base_controller import BaseController

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.permission_exception import PermissionException
from backbone_server.errors.integrity_exception import IntegrityException

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
            post = BaseLocation(self.get_engine(), self.get_session())

            loc = post.post(location, None, studies, user)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug("create_location: %s", repr(dke))
            retcode = 422
        except PermissionException as pme:
            logging.getLogger(__name__).debug("create_location: %s, %s", repr(pme), user)
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

        loc = None

        delete = BaseLocation(self.get_engine(), self.get_session())

        retcode = 200

        try:
            delete.delete(location_id, studies)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("delete_location: %s", repr(dme))
            retcode = 404
            loc = str(dme)
        except PermissionException as pme:
            logging.getLogger(__name__).debug("delete_location: %s, %s", repr(pme), user)
            retcode = 403
            loc = str(pme)
        except IntegrityException as pme:
            logging.getLogger(__name__).debug("delete_location: %s, %s", repr(pme), user)
            retcode = 422
            loc = str(pme)

        return loc, retcode

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

        get = BaseLocation(self.get_engine(), self.get_session())

        retcode = 200
        loc = None

        try:
            lat = Decimal(latitude)
            lng = Decimal(longitude)
            start = None
            count = None
            loc = get.get_by_gps(lat, lng, studies, start, count)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("download_partner_location: %s", repr(dme))
            retcode = 404
            loc = str(dme)
        except InvalidOperation as nfe:
            logging.getLogger(__name__).debug("download_partner_location: %s", repr(nfe))
            retcode = 422
            loc = str(nfe)
        except PermissionException as pme:
            logging.getLogger(__name__).debug("download_gps_location: %s, %s", repr(pme), user)
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

        get = BaseLocation(self.get_engine(), self.get_session())

        retcode = 200
        loc = None

        try:
            loc = get.get(location_id, studies)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("download_location: %s", repr(dme))
            retcode = 404
            loc = str(dme)
        except PermissionException as pme:
            logging.getLogger(__name__).debug("download_location: %s, %s", repr(pme), user)
            retcode = 403
            loc = str(pme)

        return loc, retcode

    def download_locations_by_attr(self, attr_type, attr_value, study_code,
                                  value_type=None, start=None, count=None, studies=None, user=None, auths=None):
        """
        fetches an location

        :param locationId: ID of location to fetch
        :type locationId: str

        :rtype: Location
        """

        get = BaseLocation(self.get_engine(), self.get_session())

        retcode = 200
        loc = None

        loc = get.get_by_attr(attr_type, attr_value, study_code,
                              value_type=value_type,
                              start=start, count=count, studies=studies)

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

        get = BaseLocation(self.get_engine(), self.get_session())

        retcode = 200
        loc = None

        loc = get.gets(study_name, studies, start, count, orderby)

        return loc, retcode

    def download_partner_location(self, partner_id, studies=None, user=None, auths=None):
        """
        fetches location(s) by partner name

        :param partner_id: ID of location to fetch
        :type partner_id: str

        :rtype: Locations
        """

        return self.download_locations_by_attr('partner_name', partner_id,
                                               study_code=None,
                                               value_type='str',
                                               start=None, count=None,
                                               studies=studies, user=user,
                                               auths=auths)

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
            put = BaseLocation(self.get_engine(), self.get_session())

            study = None
            loc = put.put(location_id, location, study, studies, user)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug("update_location: %s", repr(dke))
            retcode = 422
            loc = str(dke)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("update_location: %s", repr(dme))
            retcode = 404
            loc = str(dme)
        except PermissionException as pme:
            logging.getLogger(__name__).debug("update_location: %s, %s", repr(pme), user)
            retcode = 403
            loc = str(pme)

        return loc, retcode
