from openapi_server.models.individual import Individual
from openapi_server.models.individuals import Individuals
from openapi_server.models.attr import Attr
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.individual.fetch import IndividualFetch

import logging

class IndividualsGet():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, study_code=None, start=None, count=None, orderby='individual'):

        result = Individuals()

        with self._connection:
            with self._connection.cursor() as cursor:

                query_body = ' FROM individuals l'
                args = ()
                if study_code or orderby == 'study_name':
                    query_body = query_body + ''' LEFT JOIN individual_attrs li ON li.individual_id = l.id
                    JOIN attrs a ON li.attr_id = a.id
                    LEFT JOIN studies s ON s.id = a.study_id'''
                    if study_code:
                        query_body = query_body + " WHERE study_code = %s"
                        args = (study_code[:4], )

                count_args = args
                count_query = 'SELECT COUNT(DISTINCT l.id) ' + query_body

                if orderby:
                    query_body = query_body + " ORDER BY " + orderby + ", l.id"

                if not (start is None and count is None):
                    query_body = query_body + ' LIMIT %s OFFSET %s'
                    args = args + (count, start)

                if orderby:
                    cursor.execute('SELECT DISTINCT l.id, ' + orderby + query_body, args)
                else:
                    cursor.execute('SELECT DISTINCT l.id, l.id ' + query_body, args)

                individuals = []
                for (individual_id, ignored) in cursor:
                    with self._connection.cursor() as lcursor:
                        individual = IndividualFetch.fetch(lcursor, individual_id)
                        individuals.append(individual)


                if not (start is None and count is None):
                    cursor.execute(count_query, count_args)
                    result.count = cursor.fetchone()[0]
                else:
                    result.count = len(individuals)

        result.individuals = individuals

        return result
