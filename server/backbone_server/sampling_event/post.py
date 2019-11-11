import logging
import uuid

from openapi_server.models.sampling_event import SamplingEvent

from backbone_server.errors.nested_edit_exception import NestedEditException
from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from backbone_server.sampling_event.edit import SamplingEventEdit
from backbone_server.sampling_event.fetch import SamplingEventFetch


class SamplingEventPost():
    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    def post(self, sampling_event, studies):

        with self._connection:
            with self._connection.cursor() as cursor:

                # It is allowed to create a sampling event that's not
                # associated with an original_sample,
                # hence study so don't check for permission
                SamplingEventEdit.check_location_details(cursor, sampling_event.location_id,
                                                         sampling_event.location,
                                                         studies=None)
                SamplingEventEdit.check_location_details(cursor, sampling_event.proxy_location_id,
                                                         sampling_event.proxy_location,
                                                         studies=None)

                SamplingEventEdit.check_date(sampling_event)

                uuid_val = uuid.uuid4()

                stmt = '''INSERT INTO sampling_events
                            (id, doc, doc_accuracy, location_id,
                            acc_date,
                            individual_id)
                            VALUES (%s, %s, %s, %s, %s, %s)'''
                args = (uuid_val, sampling_event.doc, sampling_event.doc_accuracy,
                        sampling_event.location_id,
                        sampling_event.acc_date,
                        sampling_event.individual_id)

                cursor.execute(stmt, args)

                SamplingEventEdit.add_attrs(cursor, uuid_val, sampling_event)

                new_sampling_event = SamplingEventFetch.fetch(cursor, uuid_val,
                                                              studies=None)
                if new_sampling_event and new_sampling_event.proxy_location_id != sampling_event.proxy_location_id:
                    raise NestedEditException(f"Incompatible proxy locations {new_sampling_event.proxy_location_id} {sampling_event.proxy_location_id}")

        return new_sampling_event
