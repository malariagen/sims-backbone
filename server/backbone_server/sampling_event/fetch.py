from swagger_server.models.location import Location
from swagger_server.models.identifier import Identifier
from swagger_server.models.sampling_event import SamplingEvent
from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

from backbone_server.location.fetch import LocationFetch

class SamplingEventFetch():


    @staticmethod
    def fetch(cursor, sampling_event_id):

        if not sampling_event_id:
            return None

        stmt = '''SELECT samples.id, studies.study_name AS study_id, doc, location_id, proxy_location_id
        FROM samples
        JOIN studies ON studies.id = samples.study_id
        WHERE samples.id = %s'''
        cursor.execute( stmt, (sampling_event_id,))

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
            return sample

        stmt = '''SELECT identifier_type, identifier_value FROM identifiers WHERE sample_id = %s'''

        cursor.execute(stmt, (sample_id,))

        sample.identifiers = []
        for (name, value) in cursor:
            ident = Identifier(name, value)
            sample.identifiers.append(ident)

        if len(sample.identifiers) == 0:
            sample.identifiers = None

        return sample

