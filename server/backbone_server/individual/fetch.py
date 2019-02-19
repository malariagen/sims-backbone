from openapi_server.models.individual import Individual
from openapi_server.models.attr import Attr
from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

class IndividualFetch():


    @staticmethod
    def fetch(cursor, individual_id):

        if not individual_id:
            return None

        stmt = '''SELECT id FROM individuals WHERE id = %s'''
        cursor.execute( stmt, (individual_id,))

        individual = None

        for (individual_id, ) in cursor:
            individual = Individual(str(individual_id))

        stmt = '''SELECT DISTINCT attr_type, attr_value, attr_source, studies.study_name
                FROM individual_attrs
                JOIN attrs a ON a.id = individual_attrs.attr_id
                LEFT JOIN studies ON a.study_id = studies.id
                WHERE individual_id = %s'''

        cursor.execute(stmt, (individual_id,))

        if not individual:
            raise MissingKeyException("No individual {}".format(individual_id))

        individual.attrs = []
        for (name, value, source, study) in cursor:
            ident = Attr(attr_type = name,
                               attr_value = value,
                               attr_source = source,
                               study_name = study)
            individual.attrs.append(ident)

        if len(individual.attrs) == 0:
            individual.attrs = None

        return individual
