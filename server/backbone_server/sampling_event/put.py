import logging

import psycopg2

from openapi_server.models.sampling_event import SamplingEvent

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.nested_edit_exception import NestedEditException

from backbone_server.sampling_event.edit import SamplingEventEdit
from backbone_server.sampling_event.fetch import SamplingEventFetch

class SamplingEventPut():

    def __init__(self, conn, cursor=None):
        self._logger = logging.getLogger(__name__)
        self._connection = conn
        self._cursor = cursor


    def put(self, sampling_event_id, sampling_event):

        with self._connection:
            with self._connection.cursor() as cursor:
                return self.run_command(cursor, sampling_event_id, sampling_event)

    def run_command(self, cursor, sampling_event_id, sampling_event):

        stmt = '''SELECT id FROM sampling_events WHERE  id = %s'''
        cursor.execute(stmt, (sampling_event_id,))

        existing_sampling_event = None

        for (samp_event_id, ) in cursor:
            existing_sampling_event = SamplingEvent(samp_event_id)

        if not existing_sampling_event:
            raise MissingKeyException("Could not find sampling_event to update {}".format(sampling_event_id))

        SamplingEventEdit.check_date(sampling_event)

        SamplingEventEdit.check_location_details(cursor, sampling_event.location_id,
                                                 sampling_event.location)
        SamplingEventEdit.check_location_details(cursor, sampling_event.proxy_location_id,
                                                 sampling_event.proxy_location)

        stmt = '''UPDATE sampling_events
                    SET doc = %s, doc_accuracy = %s,
                    acc_date = %s,
                    location_id = %s,
                    individual_id = %s
                    WHERE id = %s'''
        args = (sampling_event.doc, sampling_event.doc_accuracy,
                sampling_event.acc_date,
                sampling_event.location_id,
                sampling_event.individual_id,
                sampling_event_id)

        try:
            cursor.execute(stmt, args)
            rc = cursor.rowcount

            cursor.execute('DELETE FROM sampling_event_attrs WHERE sampling_event_id = %s',
                           (sampling_event_id,))

            SamplingEventEdit.add_attrs(cursor, sampling_event_id, sampling_event)

        except psycopg2.IntegrityError as err:
            raise DuplicateKeyException("Error updating sampling_event {}".format(sampling_event)) from err
        except DuplicateKeyException as err:
            raise err


        new_sampling_event = SamplingEventFetch.fetch(cursor, sampling_event_id)

        if new_sampling_event.proxy_location_id != sampling_event.proxy_location_id:
            raise NestedEditException(f"Incompatible proxy locations {new_sampling_event.proxy_location_id} {sampling_event.proxy_location_id}")
        if rc != 1:
            raise MissingKeyException("Error updating sampling_event {}".format(sampling_event_id))


        return new_sampling_event
