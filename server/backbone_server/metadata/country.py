from swagger_server.models.country import Country
from backbone_server.errors.missing_key_exception import MissingKeyException


import logging

class CountryGet():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def __del__(self):
        if self._connection:
            self._connection.close()

    def get(self, country_id):

        cursor = self._connection.cursor()

        stmt = '''SELECT english, alpha2, alpha3 FROM countries WHERE '''
        if len(country_id) == 2:
            stmt = stmt + ''' alpha2 =%s'''
        elif len(country_id) == 3:
            stmt = stmt + ''' alpha3 =%s'''
        else:
            stmt = stmt + ''' english =%s'''
        cursor.execute( stmt, (country_id,))

        country = None

        for (english, alpha2, alpha3) in cursor:
            country = Country(english, alpha2, alpha3)

        cursor.close()

        if not country:
            raise MissingKeyException("No country {}".format(country_id))


        return country
