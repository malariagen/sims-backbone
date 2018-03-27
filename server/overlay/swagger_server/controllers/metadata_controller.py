import connexion
import six

from swagger_server.models.country import Country  # noqa: E501
from swagger_server.models.taxonomies import Taxonomies  # noqa: E501
from swagger_server.models.taxonomy import Taxonomy  # noqa: E501
from swagger_server import util

from backbone_server.controllers.metadata_controller import MetadataController
import logging

metadata_controller = MetadataController()

def create_taxonomy(taxonomy, user=None, token_info = None):
    """create_taxonomy

    Create a Taxonomy # noqa: E501
    :param taxonomy: 
    :type taxonomy: dict | bytes

    :rtype: Taxonomy
    """
    if connexion.request.is_json:
        taxonomy = Taxonomy.from_dict(connexion.request.get_json())

    return metadata_controller.create_taxonomy(taxonomy, user, token_info)

def get_country_metadata(countryId, user=None, token_info = None):
    """
    fetches all the names for a country
    guesses the search criteria
    :param countryId: location
    :type countryId: str

    :rtype: Country
    """

    return metadata_controller.get_country_metadata(countryId, user, token_info)

def get_identifier_types(user=None, token_info = None):  # noqa: E501
    """fetches all the identifier types

    returns all identifier types in use # noqa: E501


    :rtype: List[str]
    """
    return metadata_controller.get_identifier_types(user, token_info)


def get_location_identifier_types(user=None, token_info = None):  # noqa: E501
    """fetches all the location identifier types

    returns all location identifier types in use # noqa: E501


    :rtype: List[str]
    """
    return metadata_controller.get_location_identifier_types(user, token_info)

def get_taxonomy_metadata(user=None, token_info = None):  # noqa: E501
    """fetches all the registered taxa

    returns all taxa # noqa: E501


    :rtype: Taxonomies
    """
    return metadata_controller.get_taxonomy_metadata(user, token_info)
