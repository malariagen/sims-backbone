from openapi_server.models.individual import Individual
from openapi_server.models.individuals import Individuals

from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.individual.fetch import IndividualFetch

import logging

class IndividualGetByAttr():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    def get(self, attr_type, attr_value, study_name):

        with self._connection:
            with self._connection.cursor() as cursor:

                sampling_events = {}

                stmt = '''SELECT DISTINCT individual_id FROM individual_attrs
                JOIN attrs ON attrs.id = individual_attrs.attr_id
                WHERE attr_type = %s AND attr_value = %s'''
                args = (attr_type, attr_value)

                if study_name:
                    stmt = '''SELECT DISTINCT individual_id FROM individual_attrs
                    JOIN attrs ON attrs.id = individual_attrs.attr_id
                    LEFT JOIN individuals ON individual_attrs.individual_id=individuals.id
                    LEFT JOIN studies ON attrs.study_id=studies.id
                WHERE attr_type = %s AND attr_value = %s AND study_code = %s'''
                    args = args + (study_name[:4],)

                cursor.execute(stmt, args)

                individuals = Individuals(individuals=[], count=0)
                event_ids = []

                for individual_id in cursor:
                    event_ids.append(individual_id)

                for individual_id in event_ids:
                    individual = IndividualFetch.fetch(cursor, individual_id)
                    individuals.individuals.append(individual)
                    individuals.count = individuals.count + 1

                individuals.sampling_events = sampling_events

                individuals.attr_types = [attr_type]

#Allow for when partner ident is used in different studies
#        if individuals.count > 1:
#            raise MissingKeyException("Too many individuals not found {} {}".format(attr_type,
#                                                                      attr_value))

        return individuals
