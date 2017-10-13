from swagger_server.models.sample import Sample
from swagger_server.models.samples import Samples

from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

class SampleGetByIdentifier():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    def __del__(self):
        if self._connection:
            self._connection.close()

    def get(self, identifier_type, identifier_value):

        cursor = self._connection.cursor()

        cursor.execute("SELECT sample_id FROM identifiers WHERE identifier_type = %s AND identifier_value = %s", (identifier_type, identifier_value,))

        samples = Samples()
        samples.samples = []
        samples.count = 0

        #partner_name has a unique key
        for (sample_id,) in cursor:
            sample = Sample(sample_id)
            samples.samples.append(sample)
            samples.count = samples.count + 1

        cursor.close()

        if samples.count == 0:
            raise MissingKeyException("Sample not found {} {}".format(identifier_type,
                                                                      identifier_value))
        if samples.count > 1:
            raise MissingKeyException("Too many samples not found {} {}".format(identifier_type,
                                                                      identifier_value))

        return samples.samples[0]
