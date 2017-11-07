from swagger_server.models.sampling_event import SamplingEvent
from swagger_server.models.location import Location
from swagger_server.models.identifier import Identifier
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.location.fetch import LocationFetch

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

        stmt = '''SELECT samples.id, study_id, doc, location_id, proxy_location_id
        FROM samples
        WHERE samples.id = %s'''
        cursor.execute( stmt, (sample_id,))

        sample = None

        for (sample_id, study_id, doc, location_id, proxy_location_id) in cursor:
            sample = SamplingEvent(sample_id, study_id, doc)
            sample.location_id = location_id
            sample.proxy_location_id = proxy_location_id
            if location_id:
                location = LocationFetch.fetch(cursor, location_id)
                sample.location = location
            if proxy_location_id:
                proxy_location = LocationFetch.fetch(cursor, proxy_location_id)
                sample.proxy_location = proxy_location

        if not sample:
            cursor.close()
            raise MissingKeyException("No sample {}".format(sample_id))

        stmt = '''SELECT identifier_type, identifier_value FROM identifiers WHERE sample_id = %s'''

        cursor.execute(stmt, (sample_id,))

        sample.identifiers = []
        for (name, value) in cursor:
            ident = Identifier(name, value)
            sample.identifiers.append(ident)

        if len(sample.identifiers) == 0:
            sample.identifiers = None

        cursor.close()

        return sample
