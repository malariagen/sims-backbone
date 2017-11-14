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


    def __del__(self):
        if self._connection:
            self._connection.close()

    def get(self, sample_id):

        cursor = self._connection.cursor()

        sample = SamplingEventFetch.fetch(cursor, sample_id)

        cursor.close()

        if not sample:
            raise MissingKeyException("No sample {}".format(sample_id))

        return sample
