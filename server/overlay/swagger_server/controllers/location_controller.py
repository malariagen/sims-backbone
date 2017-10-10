import connexion
from swagger_server.models.location import Location
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

import logging

from backbone_server.location.post import LocationPost
from backbone_server.location.put import LocationPut
from backbone_server.location.get import LocationGetById
from backbone_server.location.delete import LocationDelete
from backbone_server.location.get_by_name import LocationGetByPartnerName

from backbone_server.connect  import get_connection

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException


def create_location(location):
    """
    create_location
    Create a location
    :param location: 
    :type location: dict | bytes

    :rtype: Location
    """
    if connexion.request.is_json:
        location = Location.from_dict(connexion.request.get_json())

    retcode = 200
    loc = None

    try:
        post = LocationPost(get_connection())

        loc = post.post(location)
    except DuplicateKeyException as dke:
        logging.getLogger(__name__).error("create_location: {}".format(repr(dke)))
        retcode = 422

    return loc, retcode


def delete_location(locationId):
    """
    deletes an location
    
    :param locationId: ID of location to fetch
    :type locationId: str

    :rtype: None
    """
    delete = LocationDelete(get_connection())

    retcode = 200
    loc = None

    try:
        delete.delete(locationId)
    except MissingKeyException as dme:
        logging.getLogger(__name__).error("delete_location: {}".format(repr(dme)))
        retcode = 404

    return None, retcode


def download_location(locationId):
    """
    fetches an location
    
    :param locationId: ID of location to fetch
    :type locationId: str

    :rtype: Location
    """
    get = LocationGetById(get_connection())

    retcode = 200
    loc = None

    try:
        loc = get.get(locationId)
    except MissingKeyException as dme:
        logging.getLogger(__name__).error("download_location: {}".format(repr(dme)))
        retcode = 404

    return loc, retcode


def download_partner_location(partnerId):
    """
    fetches a location
    
    :param partnerId: ID of location to fetch
    :type partnerId: str

    :rtype: Location
    """
    get = LocationGetByPartnerName(get_connection())

    retcode = 200
    loc = None

    try:
        loc = get.get(partnerId)
    except MissingKeyException as dme:
        logging.getLogger(__name__).error("download_partner_location: {}".format(repr(dme)))
        retcode = 404

    return loc, retcode


def update_location(locationId, location):
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

    retcode = 200
    loc = None

    try:
        put = LocationPut(get_connection())

        loc = put.put(locationId, location)
    except DuplicateKeyException as dke:
        logging.getLogger(__name__).error("update_location: {}".format(repr(dke)))
        retcode = 422
    except MissingKeyException as dme:
        logging.getLogger(__name__).error("update_location: {}".format(repr(dme)))
        retcode = 404

    return loc, retcode
