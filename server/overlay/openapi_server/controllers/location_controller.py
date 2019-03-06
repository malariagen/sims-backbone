import connexion
import six

from openapi_server.models.location import Location  # noqa: E501
from openapi_server.models.locations import Locations  # noqa: E501
from openapi_server import util

from decimal import *
import logging


from backbone_server.controllers.location_controller import LocationController


location_controller = LocationController()


def create_location(body, user=None, token_info=None):
    """
    create_location
    Create a location
    :param location:
    :type location: dict | bytes

    :rtype: Location
    """
    if connexion.request.is_json:
        location = Location.from_dict(connexion.request.get_json())

    return location_controller.create_location(location, user,
                                               location_controller.token_info(token_info))


def delete_location(location_id, user=None, token_info=None):
    """
    deletes an location

    :param locationId: ID of location to fetch
    :type locationId: str

    :rtype: None
    """
    return location_controller.delete_location(location_id, user,
                                               location_controller.token_info(token_info))


def download_gps_location(latitude, longitude, user=None, token_info=None):
    """
    fetches location(s) by GPS
    Params must be string as negative numbers not handled - https://github.com/pallets/werkzeug/issues/729 - also want to avoid using float
    :param latitude: Latitude of location to fetch
    :type latitude: str
    :param longitude: Longitude of location to fetch
    :type longitude: str

    :rtype: Location
    """
    return location_controller.download_gps_location(latitude, longitude, user,
                                                     location_controller.token_info(token_info))


def download_location(location_id, user=None, token_info=None):
    """
    fetches an location

    :param locationId: ID of location to fetch
    :type locationId: str

    :rtype: Location
    """
    return location_controller.download_location(location_id, user,
                                                 location_controller.token_info(token_info))


def download_locations(study_name=None, start=None, count=None, orderby=None, user=None,
                       token_info=None):
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
    return location_controller.download_locations(study_name, start, count, orderby, user,
                                                  location_controller.token_info(token_info))


def download_locations_by_attr(prop_name, prop_value,
                               study_name=None, user=None,
                               token_info=None):  # noqa: E501
    """fetches one or more location by property value

     # noqa: E501

    :param prop_name: name of property to search
    :type prop_name: str
    :param prop_value: matching value of property to search
    :type prop_value: str
    :param study_name: if you want to restrict the search to a study e.g. for partner_id
    :type study_name: str

    :rtype: Locations
    """
    return location_controller.download_locations_by_attr(prop_name,
                                                          prop_value, study_name, user,
                                                          location_controller.token_info(token_info))


def download_partner_location(partner_id, user=None, token_info=None):
    """
    fetches location(s) by partner name

    :param partnerId: ID of location to fetch
    :type partnerId: str

    :rtype: Locations
    """
    return location_controller.download_partner_location(partner_id, user,
                                                         location_controller.token_info(token_info))


def update_location(location_id, body, user=None, token_info=None):
    """
    updates an location

    :param locationId: ID of location to update
    :type locationId: str
    :param location:
    :type location: dict | bytes

    :rtype: Location
    """
    if connexion.request.is_json:
        location = Location.from_dict(connexion.request.get_json())

    return location_controller.update_location(location_id, location, user,
                                               location_controller.token_info(token_info))
