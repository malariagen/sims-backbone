import six

from swagger_server.models.country import Country  # noqa: E501
from swagger_server.models.taxonomies import Taxonomies  # noqa: E501
from swagger_server.models.taxonomy import Taxonomy  # noqa: E501
from swagger_server import util

from backbone_server.controllers.metadata_controller import MetadataController
import logging

from local.base_local_api import BaseLocalApi

class LocalMetadataApi(BaseLocalApi):

    def __init__(self, api_client, user, auths, method):

        super().__init__(api_client, user, auths, method)

        self.metadata_controller = MetadataController()

    def create_taxonomy(self, taxonomy):
        """create_taxonomy

        Create a Taxonomy # noqa: E501
        :param taxonomy: 
        :type taxonomy: dict | bytes

        :rtype: Taxonomy
        """

        (ret, retcode) = self.metadata_controller.create_taxonomy(taxonomy, self._user, self.auth_tokens())

        return self.create_response(ret, retcode, 'Taxonomy')

    def get_country_metadata(self, countryId):
        """
        fetches all the names for a country
        guesses the search criteria
        :param countryId: location
        :type countryId: str

        :rtype: Country
        """

        (ret, retcode) = self.metadata_controller.get_country_metadata(countryId, self._user,
                                                                       self.auth_tokens())

        return self.create_response(ret, retcode, 'Country')

    def get_identifier_types(self):  # noqa: E501
        """fetches all the identifier types

        returns all identifier types in use # noqa: E501


        :rtype: List[str]
        """
        (ret, retcode) = self.metadata_controller.get_identifier_types(self._user,
                                                                       self.auth_tokens())

        return self.create_response(ret, retcode)


    def get_location_identifier_types(self):  # noqa: E501
        """fetches all the location identifier types

        returns all location identifier types in use # noqa: E501


        :rtype: List[str]
        """
        (ret, retcode) = self.metadata_controller.get_location_identifier_types(self._user,
                                                                                self.auth_tokens())

        return self.create_response(ret, retcode)

    def get_taxonomy_metadata(self):  # noqa: E501
        """fetches all the registered taxa

        returns all taxa # noqa: E501


        :rtype: Taxonomies
        """
        (ret, retcode) = self.metadata_controller.get_taxonomy_metadata(self._user,
                                                                        self.auth_tokens())

        return self.create_response(ret, retcode, 'Taxonomies')
