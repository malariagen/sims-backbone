from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from backbone_server.individual.edit import IndividualEdit
from backbone_server.individual.fetch import IndividualFetch

from openapi_server.models.individual import Individual

import psycopg2

import logging
import uuid

class IndividualPost(IndividualEdit):

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def post(self, individual):

        with self._connection:
            with self._connection.cursor() as cursor:

                IndividualEdit.check_for_duplicate(cursor, individual, None)

                uuid_val = uuid.uuid4()

                stmt = '''INSERT INTO individuals
                            (id)
                            VALUES (%s)'''
                args = (uuid_val,)

                cursor.execute(stmt, args)

                IndividualEdit.add_attrs(cursor, uuid_val, individual)

                individual = IndividualFetch.fetch(cursor, uuid_val)

        return individual

