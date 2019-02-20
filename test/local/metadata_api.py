import six

from openapi_server.models.country import Country  # noqa: E501
from openapi_server.models.taxonomies import Taxonomies  # noqa: E501
from openapi_server.models.taxonomy import Taxonomy  # noqa: E501
from openapi_server.models.log_items import LogItems  # noqa: E501
from openapi_server import util

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

    def download_history(self, record_type, record_id, record_types=None):  # noqa: E501

        (ret, retcode) = self.metadata_controller.download_history(record_type,
                                                                   record_id,
                                                                   record_types,
                                                                   self._user,
                                                                   self.auth_tokens())
        return self.create_response(ret, retcode, 'LogItems')

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

    def get_attr_types(self):  # noqa: E501
        """fetches all the attr types

        returns all attr types in use # noqa: E501


        :rtype: List[str]
        """
        (ret, retcode) = self.metadata_controller.get_attr_types(self._user,
                                                                       self.auth_tokens())

        return self.create_response(ret, retcode)


    def get_location_attr_types(self):  # noqa: E501
        """fetches all the location attr types

        returns all location attr types in use # noqa: E501


        :rtype: List[str]
        """
        (ret, retcode) = self.metadata_controller.get_location_attr_types(self._user,
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

