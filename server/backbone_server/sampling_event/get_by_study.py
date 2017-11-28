from swagger_server.models.sampling_event import SamplingEvent
from swagger_server.models.sampling_events import SamplingEvents
from swagger_server.models.location import Location
from swagger_server.models.identifier import Identifier
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.location.fetch import LocationFetch
from backbone_server.sampling_event.fetch import SamplingEventFetch

from backbone_server.sampling_event.edit import SamplingEventEdit

import logging

class SamplingEventsGetByStudy():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, study_name):
        with self._connection:
            with self._connection.cursor() as cursor:

                study_id = SamplingEventEdit.fetch_study_id(cursor, study_name, False)

                if not study_id:
                    raise MissingKeyException("No study {}".format(study_name))

                stmt = '''SELECT samples.id FROM samples WHERE study_id = %s'''
                cursor.execute(stmt, (study_id, ))

                samples = SamplingEvents([], 0)
                event_ids = []

                for sample_id in cursor:
                    event_ids.append(sample_id)

                for sample_id in event_ids:
                    sample = SamplingEventFetch.fetch(cursor, sample_id)
                    samples.sampling_events.append(sample)
                    samples.count = samples.count + 1


        return samples
