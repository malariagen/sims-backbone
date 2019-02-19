from openapi_server.models.original_sample import OriginalSample
from openapi_server.models.location import Location
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.location.fetch import LocationFetch
from backbone_server.original_sample.fetch import OriginalSampleFetch

import logging

class OriginalSampleGetById():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, original_sample_id):

        with self._connection:
            with self._connection.cursor() as cursor:

                original_sample = OriginalSampleFetch.fetch(cursor, original_sample_id)

        if not original_sample:
            raise MissingKeyException("No original_sample {}".format(original_sample_id))

        return original_sample
