from swagger_server.models.sampling_event import SamplingEvent
from swagger_server.models.sampling_events import SamplingEvents
from swagger_server.models.location import Location
from swagger_server.models.identifier import Identifier
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.location.fetch import LocationFetch
from backbone_server.sampling_event.fetch import SamplingEventFetch

import logging

class SamplingEventsGetByLocation():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, location_id):

        with self._connection:
            with self._connection.cursor() as cursor:

                try:
                    location = LocationFetch.fetch(cursor, location_id)
                except MissingKeyException as mke:
                    raise mke

                stmt = '''SELECT samples.id FROM samples WHERE location_id = %s OR proxy_location_id = %s'''
                cursor.execute(stmt, (location_id, location_id))

                samples = SamplingEvents([], 0)
                event_ids = []

                for sample_id in cursor:
                    event_ids.append(sample_id)
                for sample_id in event_ids:
                    sample = SamplingEventFetch.fetch(cursor, sample_id)

                    #print("Adding sample {}".format(sample))
                    samples.sampling_events.append(sample)
                    samples.count = samples.count + 1


        if samples.count == 0:
            raise MissingKeyException("No samples for {}".format(location))


        return samples
