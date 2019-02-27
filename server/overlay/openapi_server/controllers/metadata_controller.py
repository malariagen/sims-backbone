import connexion
import six

from openapi_server.models.country import Country  # noqa: E501
from openapi_server.models.log_items import LogItems  # noqa: E501
from openapi_server.models.taxonomies import Taxonomies  # noqa: E501
from openapi_server.models.taxonomy import Taxonomy  # noqa: E501
from openapi_server import util

from backbone_server.controllers.metadata_controller import MetadataController
import logging

metadata_controller = MetadataController()


def create_taxonomy(body, user=None, token_info=None):
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


def download_history(record_type, record_id, action_types=None, user=None,
                     token_info=None):  # noqa: E501
    """fetches the history of a record

     # noqa: E501

    :param record_type: type
    :type record_type: str
    :param record_id: the id (uuid) of the record for which you want the history
    :type record_id:
    :param record_types: if you want to restrict the search to a type of record
    :type record_types: str

    :rtype: LogItems
    """
    return metadata_controller.download_history(record_type, record_id, action_types, user,
                                                metadata_controller.token_info(token_info))


def get_country_metadata(country_id, user=None, token_info=None):
    """
    fetches all the names for a country
    guesses the search criteria
    :param countryId: location
    :type countryId: str

    :rtype: Country
    """

    return metadata_controller.get_country_metadata(country_id, user,
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
