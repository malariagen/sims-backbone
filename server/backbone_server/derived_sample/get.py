from swagger_server.models.derived_sample import DerivedSample
from swagger_server.models.location import Location
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.location.fetch import LocationFetch
from backbone_server.derived_sample.fetch import DerivedSampleFetch

import logging

class DerivedSampleGetById():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, derived_sample_id):

        with self._connection:
            with self._connection.cursor() as cursor:

                derived_sample = DerivedSampleFetch.fetch(cursor, derived_sample_id)

        if not derived_sample:
            raise MissingKeyException("No derived_sample {}".format(derived_sample_id))

        return derived_sample
