from swagger_server.models.sampling_event import SamplingEvent
from swagger_server.models.sampling_events import SamplingEvents
from swagger_server.models.location import Location
from swagger_server.models.identifier import Identifier
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.location.fetch import LocationFetch

import logging

class SamplingEventsGetByStudy():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def __del__(self):
        if self._connection:
            self._connection.close()

    def get(self, study_name):

        cursor = self._connection.cursor()

        stmt = '''SELECT samples.id, study_id, doc, location_id, proxy_location_id
        FROM samples
        WHERE study_id = %s'''
        cursor.execute(stmt, (study_name, ))

        samples = SamplingEvents([], 0)

        for (sample_id, study_id, doc, loc_id, proxy_location_id) in cursor:
            sample = SamplingEvent(sample_id, study_id, doc)
            sample.location_id = loc_id
            sample.proxy_location_id = proxy_location_id
            samples.sampling_events.append(sample)
            samples.count = samples.count + 1

        for sample in samples.sampling_events:
            if sample.location_id:
                samp_location = LocationFetch.fetch(cursor, sample.location_id)
                sample.location = samp_location
            if sample.proxy_location_id:
                proxy_location = LocationFetch.fetch(cursor, sample.proxy_location_id)
                sample.proxy_location = proxy_location

            stmt = '''SELECT identifier_type, identifier_value FROM identifiers WHERE sample_id = %s'''

            cursor.execute(stmt, (sample.sampling_event_id,))

            sample.identifiers = []
            for (name, value) in cursor:
                ident = Identifier(name, value)
                sample.identifiers.append(ident)

            if len(sample.identifiers) == 0:
                sample.identifiers = None


        if samples.count == 0:
            cursor.close()
            raise MissingKeyException("No samples for {}".format(study_name))

        cursor.close()

        return samples
