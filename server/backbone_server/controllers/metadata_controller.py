from swagger_server.models.country import Country
from swagger_server.models.taxonomies import Taxonomies
from swagger_server.models.taxonomy import Taxonomy

from backbone_server.metadata.country import CountryGet
from backbone_server.metadata.taxonomies import TaxonomiesGet

from backbone_server.controllers.base_controller  import BaseController

from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.permission_exception import PermissionException

import logging

class MetadataController(BaseController):

    def create_taxonomy(self, taxonomy, user=None, auths = None):
        """
        create_taxonomy
        Create a Taxonomy
        :param taxonomy: 
        :type taxonomy: dict | bytes

        :rtype: Taxonomy
        """

        try:
            self.check_permissions(None, auths)
        except PermissionException as pe:
            self.log_action(user, 'create_taxonomy', None, taxonomy, None, 403)
            return pe.message, 403

        return 'do some magic!'


    def get_country_metadata(self, countryId, user=None, auths = None):
        """
        fetches all the names for a country
        guesses the search criteria
        :param countryId: location
        :type countryId: str

        :rtype: Country
        """

        try:
            self.check_permissions(None, auths)
        except PermissionException as pe:
            self.log_action(user, 'get_country_metadata', countryId, None, None, 403)
            return pe.message, 403

        get = CountryGet(self.get_connection())

        retcode = 200
        country = None

        try:
            country = get.get(countryId)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("get_country_metadata: {}".format(repr(dme)))
            retcode = 404

        self.log_action(user, 'get_country_metadata', countryId, None, country, retcode)

        return country, retcode

    def get_taxonomy_metadata(self, user=None, auths = None):
        """
        fetches all the registered taxa
        guesses the search criteria

        :rtype: Taxonomies
        """

        try:
            self.check_permissions(None, auths)
        except PermissionException as pe:
            self.log_action(user, 'get_taxonomy_metadata', None, None, None, 403)
            return pe.message, 403

        get = TaxonomiesGet(self.get_connection())

        taxas = get.get()

        self.log_action(user, 'get_taxonomy_metadata', None, None, taxas, 200)

        return taxas, 200
