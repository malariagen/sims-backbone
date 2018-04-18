from swagger_server.models.country import Country
from swagger_server.models.taxonomies import Taxonomies
from swagger_server.models.taxonomy import Taxonomy

from backbone_server.metadata.country import CountryGet
from backbone_server.metadata.taxonomies import TaxonomiesGet
from backbone_server.metadata.taxonomy_post import TaxonomyPost
from backbone_server.metadata.identifier_types import IdentifierTypesGet

from backbone_server.controllers.base_controller  import BaseController

from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.permission_exception import PermissionException

import logging
import urllib

from backbone_server.controllers.decorators  import apply_decorators

@apply_decorators
class MetadataController(BaseController):

    def create_taxonomy(self, taxonomy, user=None, auths = None):
        """
        create_taxonomy
        Create a Taxonomy
        :param taxonomy: 
        :type taxonomy: dict | bytes

        :rtype: Taxonomy
        """

        retcode = 201

        post = TaxonomyPost(self.get_connection())

        taxa = post.post(taxonomy)

        return taxa, retcode


    def get_country_metadata(self, countryId, user=None, auths = None):
        """
        fetches all the names for a country
        guesses the search criteria
        :param countryId: location
        :type countryId: str

        :rtype: Country
        """

        get = CountryGet(self.get_connection())

        retcode = 200
        country = None

        countryId = urllib.parse.unquote_plus(countryId)

        try:
            country = get.get(countryId)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("get_country_metadata: {}".format(repr(dme)))
            retcode = 404

        return country, retcode

    def get_identifier_types(self, user=None, auths=None):  # noqa: E501
        """fetches all the identifier types

        returns all identifier types in use # noqa: E501


        :rtype: List[str]
        """
        get = IdentifierTypesGet(self.get_connection())

        ident_types = get.get('identifiers')

        return ident_types, 200


    def get_location_identifier_types(self, user=None, auths=None):  # noqa: E501
        """fetches all the location identifier types

        returns all location identifier types in use # noqa: E501


        :rtype: List[str]
        """

        get = IdentifierTypesGet(self.get_connection())

        ident_types = get.get('location_identifiers')

        return ident_types, 200


    def get_taxonomy_metadata(self, user=None, auths = None):
        """
        fetches all the registered taxa
        guesses the search criteria

        :rtype: Taxonomies
        """

        get = TaxonomiesGet(self.get_connection())

        taxas = get.get()

        return taxas, 200
