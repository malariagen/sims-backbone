from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.incompatible_exception import IncompatibleException

from backbone_server.sampling_event.edit import SamplingEventEdit
from backbone_server.sampling_event.put import SamplingEventPut
from backbone_server.sampling_event.delete import SamplingEventDelete
from backbone_server.sampling_event.fetch import SamplingEventFetch
from backbone_server.location.edit import LocationEdit

from openapi_server.models.sampling_event import SamplingEvent

import psycopg2

import logging

class SamplingEventMerge():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def merge(self, into, merged, studies):

        with self._connection:
            with self._connection.cursor() as cursor:

                return self.run_command(cursor, into, merged, studies)


    def run_command(self, cursor, into, merged, studies):

        sampling_event1 = SamplingEventFetch.fetch(cursor, into, studies)

        if not sampling_event1:
            raise MissingKeyException("No sampling_event {}".format(into))

        if into == merged:
            return sampling_event1

        sampling_event2 = SamplingEventFetch.fetch(cursor, merged, studies)

        if not sampling_event2:
            raise MissingKeyException("No sampling_event {}".format(merged))

        if sampling_event1.doc:
            if sampling_event2.doc:
                if sampling_event1.doc != sampling_event2.doc:
                    msg = 'Incompatible doc {} {}'.format(sampling_event1.doc,
                                                          sampling_event2.doc)
                    raise IncompatibleException(msg)
        else:
            sampling_event1.doc = sampling_event2.doc

        if sampling_event1.doc_accuracy:
            if sampling_event2.doc_accuracy:
                if sampling_event1.doc_accuracy != sampling_event2.doc_accuracy:
                    msg = 'Incompatible doc_accuracy {} {}'.format(sampling_event1.doc_accuracy,
                                                                   sampling_event2.doc_accuracy)
                    raise IncompatibleException(msg)
        else:
            if sampling_event2.doc_accuracy:
                sampling_event1.doc_accuracy = sampling_event2.doc_accuracy

        if sampling_event1.location_id:
            if sampling_event2.location_id:
                if sampling_event1.location_id != sampling_event2.location_id:
                    msg = 'Incompatible location_id {} {}'.format(sampling_event1.location_id,
                                                                  sampling_event2.location_id)
                    raise IncompatibleException(msg)
        else:
            sampling_event1.location_id = sampling_event2.location_id

        if sampling_event1.proxy_location_id == 'None':
            sampling_event1.proxy_location_id = None
        if sampling_event2.proxy_location_id == 'None':
            sampling_event2.proxy_location_id = None

        if sampling_event1.proxy_location_id:
            if sampling_event2.proxy_location_id:
                if sampling_event1.proxy_location_id != sampling_event2.proxy_location_id:
                    msg = 'Incompatible proxy_location_id {} {}'.format(sampling_event1.proxy_location_id,
                                                                        sampling_event2.proxy_location_id)
                    raise IncompatibleException(msg)
        else:
            sampling_event1.proxy_location_id = sampling_event2.proxy_location_id

        if sampling_event2.attrs:
            for new_ident in sampling_event2.attrs:
                found = False
                for existing_ident in sampling_event1.attrs:
                    if new_ident == existing_ident:
                        found = True
                if not found:
                    new_ident_value = True
                    sampling_event1.attrs.append(new_ident)

        stmt = '''UPDATE original_samples SET sampling_event_id = %s WHERE sampling_event_id = %s'''

        cursor.execute(stmt,
                       (sampling_event1.sampling_event_id,
                        sampling_event2.sampling_event_id))


        delete = SamplingEventDelete(self._connection)

        delete.run_command(cursor, sampling_event2.sampling_event_id)

        put = SamplingEventPut(self._connection)

        return put.run_command(cursor, sampling_event1.sampling_event_id,
                               sampling_event1, studies)
