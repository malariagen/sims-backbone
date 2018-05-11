import connexion
import six

from swagger_server.models.country import Country  # noqa: E501
from swagger_server.models.taxonomies import Taxonomies  # noqa: E501
from swagger_server.models.taxonomy import Taxonomy  # noqa: E501
from swagger_server import util

from backbone_server.controllers.metadata_controller import MetadataController
import logging

metadata_controller = MetadataController()

def create_taxonomy(taxonomy, user=None, token_info=None):
    """create_taxonomy

    Create a Taxonomy # noqa: E501
    :param taxonomy: 
    :type taxonomy: dict | bytes

    :rtype: Taxonomy
    """
    if connexion.request.is_json:
        taxonomy = Taxonomy.from_dict(connexion.request.get_json())

    return metadata_controller.create_taxonomy(taxonomy, user,
                                               metadata_controller.token_info(token_info))

def get_country_metadata(countryId, user=None, token_info=None):
    """
    fetches all the names for a country
    guesses the search criteria
    :param countryId: location
    :type countryId: str

    :rtype: Country
    """

    return metadata_controller.get_country_metadata(countryId, user,
                                                    metadata_controller.token_info(token_info))

def get_attr_types(user=None, token_info=None):  # noqa: E501
    """fetches all the attr types

    returns all attr types in use # noqa: E501


    :rtype: List[str]
    """
    return metadata_controller.get_attr_types(user,
                                                    metadata_controller.token_info(token_info))


def get_location_attr_types(user=None, token_info=None):  # noqa: E501
    """fetches all the location attr types

    returns all location attr types in use # noqa: E501


    :rtype: List[str]
    """
    return metadata_controller.get_location_attr_types(user,
                                                             metadata_controller.token_info(token_info))

def get_taxonomy_metadata(user=None, token_info=None):  # noqa: E501
    """fetches all the registered taxa

    returns all taxa # noqa: E501


    :rtype: Taxonomies
    """
    return metadata_controller.get_taxonomy_metadata(user,
                                                     metadata_controller.token_info(token_info))
