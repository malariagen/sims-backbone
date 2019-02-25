from backbone_server.metadata.country import CountryGet
from backbone_server.metadata.taxonomies import TaxonomiesGet
from backbone_server.metadata.taxonomy_post import TaxonomyPost
from backbone_server.metadata.attr_types import AttrTypesGet
from backbone_server.metadata.history import History

from backbone_server.controllers.base_controller import BaseController

from backbone_server.errors.missing_key_exception import MissingKeyException

import logging
import urllib

from backbone_server.controllers.decorators import apply_decorators


@apply_decorators
class MetadataController(BaseController):

    def create_taxonomy(self, taxonomy, user=None, auths=None):
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


    def download_history(self, record_type, record_id, action_types=None, user=None,
                         auths=None):  # noqa: E501
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

        retcode = 200
        log_items = None

        get = History(self.get_connection())

        try:
            log_items = get.get(record_type, record_id, action_types)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("download_history: {}".format(repr(dme)))
            log_items = str(dme)
            retcode = 404

        return log_items, retcode

    def get_country_metadata(self, countryId, user=None, auths=None):
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
            logging.getLogger(__name__).debug("get_country_metadata: {}".format(repr(dme)))
            retcode = 404

        return country, retcode

    def get_attr_types(self, user=None, auths=None):  # noqa: E501
        """fetches all the attr types

        returns all attr types in use # noqa: E501


        :rtype: List[str]
        """
        get = AttrTypesGet(self.get_connection())

        ident_types = get.get('attrs')

        return ident_types, 200

    def get_location_attr_types(self, user=None, auths=None):  # noqa: E501
        """fetches all the location attr types

        returns all location attr types in use # noqa: E501


        :rtype: List[str]
        """

        get = AttrTypesGet(self.get_connection())

        ident_types = get.get('location_attrs')

        return ident_types, 200

    def get_taxonomy_metadata(self, user=None, auths=None):
        """
        fetches all the registered taxa
        guesses the search criteria

        :rtype: Taxonomies
        """

        get = TaxonomiesGet(self.get_connection())

        taxas = get.get()

        return taxas, 200
