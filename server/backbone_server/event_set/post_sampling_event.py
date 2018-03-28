from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from backbone_server.event_set.edit import EventSetEdit
from backbone_server.event_set.fetch import EventSetFetch

from swagger_server.models.sampling_event import SamplingEvent

import psycopg2

import logging

class EventSetPostSamplingEvent():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def post(self, event_set_name, sampling_event_id):

        resp = None

        with self._connection:
            with self._connection.cursor() as cursor:

                event_set_id = EventSetFetch.fetch_event_set_id(cursor,event_set_name)

                try:

                    sampling_event = SamplingEvent(sampling_event_id)
                    EventSetEdit.add_sampling_event(cursor, event_set_id, sampling_event)

                except psycopg2.IntegrityError as err:
                    raise DuplicateKeyException("Error inserting sampling event to event set {} {}".format(event_set_name, sampling_event_id)) from err

        return resp

