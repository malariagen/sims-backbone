from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from backbone_server.sampling_event.edit import SamplingEventEdit
from backbone_server.sampling_event.fetch import SamplingEventFetch

from swagger_server.models.sampling_event import SamplingEvent

import psycopg2

import logging
import uuid

class SamplingEventPost():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def post(self, sampling_event):

        with self._connection:
            with self._connection.cursor() as cursor:

                SamplingEventEdit.check_location_details(cursor, sampling_event.location_id,
                                                         sampling_event.location)
                SamplingEventEdit.check_location_details(cursor, sampling_event.proxy_location_id,
                                                         sampling_event.proxy_location)

                SamplingEventEdit.check_date(sampling_event)

                uuid_val = uuid.uuid4()

                study_id = SamplingEventEdit.fetch_study_id(cursor, sampling_event.study_name, True)

                stmt = '''INSERT INTO sampling_events
                            (id, study_id, doc, doc_accuracy, location_id, proxy_location_id)
                            VALUES (%s, %s, %s, %s, %s, %s)'''
                args = (uuid_val,study_id, sampling_event.doc, sampling_event.doc_accuracy,
                        sampling_event.location_id, sampling_event.proxy_location_id)

                try:
                    cursor.execute(stmt, args)

                    SamplingEventEdit.add_attrs(cursor, uuid_val, sampling_event)

                except psycopg2.IntegrityError as err:
                    print(err.pgcode)
                    print(err.pgerror)
                    raise DuplicateKeyException("Error inserting sampling_event {}".format(sampling_event)) from err
                except DuplicateKeyException as err:
                    raise err

                sampling_event = SamplingEventFetch.fetch(cursor, uuid_val)

        return sampling_event

