from swagger_server.models.sampling_event import SamplingEvent
from swagger_server.models.sampling_events import SamplingEvents

from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.sampling_event.fetch import SamplingEventFetch

import logging

class SamplingEventGetByIdentifier():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    def get(self, identifier_type, identifier_value):

        with self._connection:
            with self._connection.cursor() as cursor:

                cursor.execute("SELECT DISTINCT sampling_event_id FROM identifiers WHERE identifier_type = %s AND identifier_value = %s", (identifier_type, identifier_value,))

                sampling_events = SamplingEvents([], 0)
                event_ids = []

                for sampling_event_id in cursor:
                    event_ids.append(sampling_event_id)

                for sampling_event_id in event_ids:
                    sampling_event = SamplingEventFetch.fetch(cursor, sampling_event_id)
                    sampling_events.sampling_events.append(sampling_event)
                    sampling_events.count = sampling_events.count + 1

        #partner_name has a unique key
        if sampling_events.count == 0:
            raise MissingKeyException("SamplingEvent not found {} {}".format(identifier_type,
                                                                      identifier_value))
#Allow for when partner ident is used in different studies
#        if sampling_events.count > 1:
#            raise MissingKeyException("Too many sampling_events not found {} {}".format(identifier_type,
#                                                                      identifier_value))

        return sampling_events
