from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.incompatible_exception import IncompatibleException

from backbone_server.sampling_event.merge import SamplingEventMerge
from backbone_server.individual.edit import IndividualEdit
from backbone_server.individual.put import IndividualPut
from backbone_server.individual.delete import IndividualDelete
from backbone_server.individual.fetch import IndividualFetch
from backbone_server.location.edit import LocationEdit

from openapi_server.models.individual import Individual

import psycopg2

import logging

class IndividualMerge():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def merge(self, into, merged):

        ret = None

        with self._connection:
            with self._connection.cursor() as cursor:

                individual1 = IndividualFetch.fetch(cursor, into)

                if not individual1:
                    raise MissingKeyException("No individual {}".format(into))

                if individual1.individual_id == merged:
                    return individual1

                individual2 = IndividualFetch.fetch(cursor, merged)

                if not individual2:
                    raise MissingKeyException("No individual {}".format(merged))

                if individual2.attrs:
                    for new_ident in individual2.attrs:
                        found = False
                        for existing_ident in individual1.attrs:
                            if new_ident == existing_ident:
                                found = True
                        if not found:
                            new_ident_value = True
                            individual1.attrs.append(new_ident)

                stmt = '''UPDATE sampling_events SET individual_id = %s WHERE
                individual_id = %s'''
                cursor.execute(stmt, (individual1.individual_id,
                                      individual2.individual_id))

                delete = IndividualDelete(self._connection)

                delete.delete(individual2.individual_id)

                put = IndividualPut(self._connection)

                ret = put.run_command(cursor, individual1.individual_id, individual1)

        return ret
