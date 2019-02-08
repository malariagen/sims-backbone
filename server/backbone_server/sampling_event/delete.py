from backbone_server.individual.delete import IndividualDelete

from backbone_server.errors.missing_key_exception import MissingKeyException


import logging

class SamplingEventDelete():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def delete(self, sampling_event_id):

        with self._connection:
            with self._connection.cursor() as cursor:

                return self.run_command(cursor, sampling_event_id)

    def run_command(self, cursor, sampling_event_id):

        stmt = '''SELECT individual_id FROM sampling_events WHERE id = %s'''

        cursor.execute( stmt, (sampling_event_id,))

        individual_id = cursor.fetchone()[0]

        individual_ids = 0

        if individual_id:
            stmt = '''SELECT COUNT(individual_id) FROM sampling_events WHERE individual_id = %s'''

            cursor.execute( stmt, (individual_id,))
            individual_ids = cursor.fetchone()[0]


        stmt = '''UPDATE original_samples SET sampling_event_id = NULL WHERE sampling_event_id = %s'''

        cursor.execute( stmt, (sampling_event_id,))

        stmt = '''DELETE FROM sampling_event_attrs WHERE sampling_event_id = %s'''

        cursor.execute( stmt, (sampling_event_id,))

        stmt = '''DELETE FROM event_set_members WHERE sampling_event_id = %s'''

        cursor.execute( stmt, (sampling_event_id,))

        stmt = '''DELETE FROM sampling_events WHERE id = %s'''

        cursor.execute( stmt, (sampling_event_id,))

        rc = cursor.rowcount

        if individual_ids == 1:
            i_delete = IndividualDelete(self._connection)
            i_delete.run_command(cursor, individual_id)


        if rc != 1:
            raise MissingKeyException("Error deleting sampling_event {}".format(sampling_event_id))


