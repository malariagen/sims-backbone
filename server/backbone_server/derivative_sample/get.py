from openapi_server.models.derivative_sample import DerivativeSample
from openapi_server.models.location import Location
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.location.fetch import LocationFetch
from backbone_server.derivative_sample.fetch import DerivativeSampleFetch

import logging

class DerivativeSampleGetById():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, derivative_sample_id):

        with self._connection:
            with self._connection.cursor() as cursor:

                derivative_sample = DerivativeSampleFetch.fetch(cursor, derivative_sample_id)

        if not derivative_sample:
            raise MissingKeyException("No derivative_sample {}".format(derivative_sample_id))

        return derivative_sample
