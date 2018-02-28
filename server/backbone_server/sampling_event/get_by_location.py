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


    def get(self, location_id, start, count):

        with self._connection:
            with self._connection.cursor() as cursor:

                try:
                    location = LocationFetch.fetch(cursor, location_id)
                except MissingKeyException as mke:
                    raise mke

                stmt = '''SELECT sampling_events.id FROM sampling_events WHERE location_id = %s OR proxy_location_id = %s'''
                cursor.execute(stmt, (location_id, location_id))

                sampling_events = SamplingEvents([], 0)
                event_ids = []

                for sampling_event_id in cursor:
                    event_ids.append(sampling_event_id)
                for sampling_event_id in event_ids:
                    sampling_event = SamplingEventFetch.fetch(cursor, sampling_event_id)

                    #print("Adding sampling_event {}".format(sampling_event))
                    sampling_events.sampling_events.append(sampling_event)
                    sampling_events.count = sampling_events.count + 1


        if sampling_events.count == 0:
            raise MissingKeyException("No sampling_events for {}".format(location))


        return sampling_events
