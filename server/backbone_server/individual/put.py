from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.individual.edit import IndividualEdit
from backbone_server.individual.fetch import IndividualFetch

from swagger_server.models.individual import Individual
from swagger_server.models.attr import Attr

import psycopg2

import logging

class IndividualPut(IndividualEdit):

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def put(self, individual_id, individual):

        with self._connection:
            with self._connection.cursor() as cursor:

                stmt = '''SELECT id FROM individuals WHERE  id = %s'''
                cursor.execute( stmt, (individual_id,))

                existing_individual = None

                for (individual_id, ) in cursor:
                    existing_individual = Individual(individual_id)

                if not existing_individual:
                    raise MissingKeyException("Error updating individual {}".format(individual_id))

                IndividualEdit.check_for_duplicate(cursor, individual, individual_id)

                stmt = '''UPDATE individuals
                            SET id = %s
                            WHERE id = %s'''
                args = (individual_id, individual_id)
                try:
                    cursor.execute(stmt, args)
                    rc = cursor.rowcount

                    cursor.execute('''DELETE FROM individual_attrs WHERE individual_id = %s''',
                                   (individual_id,))

                    IndividualEdit.add_attrs(cursor, individual_id, individual)

                except psycopg2.IntegrityError as err:
                    raise DuplicateKeyException("Error updating individual {}".format(individual)) from err

                individual = IndividualFetch.fetch(cursor, individual_id)


        if rc != 1:
            raise MissingKeyException("Error updating individual {}".format(individual_id))
#
        return individual
