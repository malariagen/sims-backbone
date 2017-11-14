from swagger_server.models.country import Country
from swagger_server.models.taxonomies import Taxonomies
from swagger_server.models.taxonomy import Taxonomy
from datetime import date, datetime
from typing import List, Dict
from six import iteritems

from backbone_server.metadata.country import CountryGet
from backbone_server.metadata.taxonomies import TaxonomiesGet

from backbone_server.connect  import get_connection

from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

class MetadataController():

    @staticmethod
    def create_taxonomy(taxonomy):
        """
        create_taxonomy
        Create a Taxonomy
        :param taxonomy: 
        :type taxonomy: dict | bytes

        :rtype: Taxonomy
        """
        return 'do some magic!'


    @staticmethod
    def get_country_metadata(countryId):
        """
        fetches all the names for a country
        guesses the search criteria
        :param countryId: location
        :type countryId: str

        :rtype: Country
        """
        get = CountryGet(get_connection())

        retcode = 200
        country = None

        try:
            country = get.get(countryId)
        except MissingKeyException as dme:
            logging.getLogger(__name__).error("download_sample: {}".format(repr(dme)))
            retcode = 404

        return country, retcode

    @staticmethod
    def get_taxonomy_metadata():
        """
        fetches all the registered taxa
        guesses the search criteria

        :rtype: Taxonomies
        """
        get = TaxonomiesGet(get_connection())

        taxas = get.get()

        return taxas, 200
