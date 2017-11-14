from swagger_server.models.sampling_event import SamplingEvent
from swagger_server.models.sampling_events import SamplingEvents
from swagger_server.models.location import Location
from swagger_server.models.identifier import Identifier
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.location.fetch import LocationFetch
from backbone_server.sampling_event.fetch import SamplingEventFetch

import logging

class SamplingEventsGetByStudy():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def __del__(self):
        if self._connection:
            self._connection.close()

    def get(self, study_name):

        cursor = self._connection.cursor()

        stmt = '''SELECT samples.id FROM samples WHERE study_id = %s'''
        cursor.execute(stmt, (study_name, ))

        samples = SamplingEvents([], 0)
        event_ids = []

        for sample_id in cursor:
            event_ids.append(sample_id)

        for sample_id in event_ids:
            sample = SamplingEventFetch.fetch(cursor, sample_id)
            samples.sampling_events.append(sample)
            samples.count = samples.count + 1

        if samples.count == 0:
            cursor.close()
            raise MissingKeyException("No samples for {}".format(study_name))

        cursor.close()

        return samples
