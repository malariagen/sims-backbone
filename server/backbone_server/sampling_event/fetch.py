from openapi_server.models.location import Location
from openapi_server.models.attr import Attr
from openapi_server.models.taxonomy import Taxonomy
from openapi_server.models.sampling_event import SamplingEvent
from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

from backbone_server.location.fetch import LocationFetch

class SamplingEventFetch():


    @staticmethod
    def fetch_attrs(cursor, sampling_event_id):

        stmt = '''SELECT attr_type, attr_value, attr_source FROM attrs
        JOIN sampling_event_attrs ON sampling_event_attrs.attr_id = attrs.id
        WHERE sampling_event_id = %s
                ORDER BY attr_type, attr_value, attr_source'''

        cursor.execute(stmt, (sampling_event_id,))

        attrs = []
        for (name, value, source) in cursor:
            ident = Attr(name, value, source)
            attrs.append(ident)

        if len(attrs) == 0:
            attrs = None

        return attrs

    @staticmethod
    def fetch_event_sets(cursor, sampling_event_id):

        stmt = '''select event_set_name FROM event_set_members
        JOIN event_sets ON event_set_id = event_sets.id
        WHERE sampling_event_id = %s'''

        cursor.execute(stmt, (sampling_event_id,))

        attrs = []
        for (name,) in cursor:
            attrs.append(name)

        if len(attrs) == 0:
            attrs = None

        return attrs

    @staticmethod
    def fetch(cursor, sampling_event_id, locations=None):

        if not sampling_event_id:
            return None

        stmt = '''SELECT sampling_events.id, doc, doc_accuracy,
                            location_id, proxy_location_id, individual_id
        FROM sampling_events
        WHERE sampling_events.id = %s'''
        cursor.execute( stmt, (sampling_event_id,))

        sampling_event = None

        for (sampling_event_id, doc, doc_accuracy, location_id,
             proxy_location_id, individual_id) in cursor:
            sampling_event = SamplingEvent(str(sampling_event_id),
                                           doc=doc, doc_accuracy=doc_accuracy,
                                           individual_id=individual_id)
            if location_id:
                sampling_event.location_id = str(location_id)
                sampling_event.public_location_id = str(location_id)
            if proxy_location_id:
                sampling_event.proxy_location_id = str(proxy_location_id)
                sampling_event.public_location_id = str(proxy_location_id)

        if not sampling_event:
            return sampling_event

        sampling_event.attrs = SamplingEventFetch.fetch_attrs(cursor, sampling_event_id)

        sampling_event.event_sets = SamplingEventFetch.fetch_event_sets(cursor, sampling_event_id)

        if sampling_event.location_id:
            location = LocationFetch.fetch(cursor, sampling_event.location_id)
            if locations is not None:
                if sampling_event.location_id not in locations:
                    locations[sampling_event.location_id] = location
            else:
                sampling_event.location = location
        if sampling_event.proxy_location_id:
            proxy_location = LocationFetch.fetch(cursor, sampling_event.proxy_location_id)
            if locations is not None:
                if sampling_event.proxy_location_id not in locations:
                    locations[sampling_event.proxy_location_id] = proxy_location
            else:
                sampling_event.proxy_location = proxy_location

        return sampling_event

