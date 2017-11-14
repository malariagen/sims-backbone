import connexion
from swagger_server.models.country import Country
from swagger_server.models.taxonomies import Taxonomies
from swagger_server.models.taxonomy import Taxonomy
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from backbone_server.controllers.metadata_controller import MetadataController

import logging

def create_taxonomy(taxonomy):
    """
    create_taxonomy
    Create a Taxonomy
    :param taxonomy: 
    :type taxonomy: dict | bytes

    :rtype: Taxonomy
    """
    if connexion.request.is_json:
        taxonomy = Taxonomy.from_dict(connexion.request.get_json())
    return 'do some magic!'

def get_country_metadata(countryId):
    """
    fetches all the names for a country
    guesses the search criteria
    :param countryId: location
    :type countryId: str

    :rtype: Country
    """

    return MetadataController.get_country_metadata(countryId)


def get_taxonomy_metadata():
    """
    fetches all the registered taxa
    guesses the search criteria

    :rtype: Taxonomies
    """
    return MetadataController.get_taxonomy_metadata()
