import connexion
from swagger_server.models.location import Location
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from decimal import *
import logging


from backbone_server.controllers.location_controller  import LocationController


location_controller = LocationController()

def create_location(location, user = None):
    """
    create_location
    Create a location
    :param location: 
    :type location: dict | bytes

    :rtype: Location
    """
    if connexion.request.is_json:
        location = Location.from_dict(connexion.request.get_json())

    return location_controller.create_location(location, user)


def delete_location(locationId, user = None):
    """
    deletes an location
    
    :param locationId: ID of location to fetch
    :type locationId: str

    :rtype: None
    """
    return location_controller.delete_location(locationId, user)


def download_gps_location(latitude, longitude, user = None):
    """
    fetches location(s) by GPS
    Params must be string as negative numbers not handled - https://github.com/pallets/werkzeug/issues/729 - also want to avoid using float
    :param latitude: Latitude of location to fetch
    :type latitude: str
    :param longitude: Longitude of location to fetch
    :type longitude: str

    :rtype: Location
    """
    return location_controller.download_gps_location(latitude, longitude, user)

def download_location(locationId, user = None):
    """
    fetches an location
    
    :param locationId: ID of location to fetch
    :type locationId: str

    :rtype: Location
    """
    return location_controller.download_location(locationId, user)


def download_locations(studyName=None, start=None, count=None, orderby=None, user = None):
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
    return location_controller.download_locations(studyName, start, count, orderby, user)


def download_partner_location(partnerId, user = None):
    """
    fetches location(s) by partner name
    
    :param partnerId: ID of location to fetch
    :type partnerId: str

    :rtype: Locations
    """
    return location_controller.download_partner_location(partnerId, user)


def update_location(locationId, location, user = None):
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

    return location_controller.update_location(locationId, location, user)

