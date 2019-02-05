from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.individual.fetch import IndividualFetch

import logging

class IndividualGetById():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, individual_id):

        individual = None

        with self._connection:
            with self._connection.cursor() as cursor:

                individual = IndividualFetch.fetch(cursor, individual_id)


        return individual
