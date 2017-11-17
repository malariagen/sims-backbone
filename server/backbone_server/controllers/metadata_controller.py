from swagger_server.models.country import Country
from swagger_server.models.taxonomies import Taxonomies
from swagger_server.models.taxonomy import Taxonomy

from backbone_server.metadata.country import CountryGet
from backbone_server.metadata.taxonomies import TaxonomiesGet

from backbone_server.controllers.base_controller  import BaseController

from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

class MetadataController(BaseController):

    def create_taxonomy(self, taxonomy):
        """
        create_taxonomy
        Create a Taxonomy
        :param taxonomy: 
        :type taxonomy: dict | bytes

        :rtype: Taxonomy
        """
        return 'do some magic!'


    def get_country_metadata(self, countryId):
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

        try:
            country = get.get(countryId)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_sample: {}".format(repr(dme)))
            retcode = 404

        return country, retcode

    def get_taxonomy_metadata(self):
        """
        fetches all the registered taxa
        guesses the search criteria

        :rtype: Taxonomies
        """
        get = TaxonomiesGet(self.get_connection())

        taxas = get.get()

        return taxas, 200
