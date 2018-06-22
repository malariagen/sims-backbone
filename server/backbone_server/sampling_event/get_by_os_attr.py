from swagger_server.models.sampling_event import SamplingEvent
from swagger_server.models.sampling_events import SamplingEvents

from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.sampling_event.fetch import SamplingEventFetch

import logging

class SamplingEventGetByOsAttr():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    def get(self, attr_type, attr_value, study_name):

        with self._connection:
            with self._connection.cursor() as cursor:

                locations = {}

                stmt = '''SELECT DISTINCT sampling_event_id FROM original_sample_attrs
                JOIN attrs ON attrs.id = original_sample_attrs.attr_id
                JOIN original_samples ON original_samples.id = original_sample_attrs.original_sample_id
                WHERE attr_type = %s AND attr_value = %s'''
                args = (attr_type, attr_value)

                if study_name:
                    stmt = '''SELECT DISTINCT sampling_event_id FROM original_sample_attrs
                    JOIN attrs ON attrs.id = original_sample_attrs.attr_id
                    JOIN original_samples ON original_samples.id = original_sample_attrs.original_sample_id
                    LEFT JOIN sampling_events ON original_samples.sampling_event_id=sampling_events.id
                    LEFT JOIN studies ON sampling_events.study_id=studies.id
                WHERE attr_type = %s AND attr_value = %s AND study_code = %s'''
                    args = args + (study_name[:4],)

                cursor.execute(stmt, args)

                sampling_events = SamplingEvents(sampling_events=[], count=0)
                event_ids = []

                for sampling_event_id in cursor:
                    event_ids.append(sampling_event_id)

                for sampling_event_id in event_ids:
                    sampling_event = SamplingEventFetch.fetch(cursor, sampling_event_id, locations)
                    #Because the client doesn't support types in maps
                    #and the result set should be small
                    if sampling_event.location_id:
                        sampling_event.location = locations[sampling_event.location_id]
                    if sampling_event.proxy_location_id:
                        sampling_event.proxy_location = locations[sampling_event.proxy_location_id]
                    sampling_events.sampling_events.append(sampling_event)
                    sampling_events.count = sampling_events.count + 1

                sampling_events.locations = locations

                sampling_events.attr_types = [attr_type]

        #partner_name has a unique key
        if sampling_events.count == 0:
            raise MissingKeyException("SamplingEvent not found {} {}".format(attr_type,
                                                                      attr_value))
#Allow for when partner ident is used in different studies
#        if sampling_events.count > 1:
#            raise MissingKeyException("Too many sampling_events not found {} {}".format(attr_type,
#                                                                      attr_value))

        return sampling_events
