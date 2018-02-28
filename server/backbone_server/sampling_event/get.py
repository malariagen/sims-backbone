from swagger_server.models.sampling_event import SamplingEvent
from swagger_server.models.location import Location
from swagger_server.models.identifier import Identifier
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.location.fetch import LocationFetch
from backbone_server.sampling_event.fetch import SamplingEventFetch

import logging

class SamplingEventGetById():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, sampling_event_id):

        with self._connection:
            with self._connection.cursor() as cursor:

                sampling_event = SamplingEventFetch.fetch(cursor, sampling_event_id)

        if not sampling_event:
            raise MissingKeyException("No sampling_event {}".format(sampling_event_id))

        return sampling_event
