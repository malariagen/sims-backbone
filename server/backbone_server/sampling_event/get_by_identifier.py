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

        cursor = self._connection.cursor()

        cursor.execute("SELECT sample_id FROM identifiers WHERE identifier_type = %s AND identifier_value = %s", (identifier_type, identifier_value,))

        samples = SamplingEvents([], 0)
        event_ids = []

        for sample_id in cursor:
            event_ids.append(sample_id)

        for sample_id in event_ids:
            sample = SamplingEventFetch.fetch(cursor, sample_id)
            samples.sampling_events.append(sample)
            samples.count = samples.count + 1

        cursor.close()

        #partner_name has a unique key
        if samples.count == 0:
            raise MissingKeyException("SamplingEvent not found {} {}".format(identifier_type,
                                                                      identifier_value))
        if samples.count > 1:
            raise MissingKeyException("Too many samples not found {} {}".format(identifier_type,
                                                                      identifier_value))

        return samples.sampling_events[0]
