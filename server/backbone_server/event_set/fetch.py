import logging

from openapi_server.models.sampling_event import SamplingEvent
from openapi_server.models.sampling_events import SamplingEvents
from openapi_server.models.event_set_note import EventSetNote
from openapi_server.models.event_set import EventSet

from openapi_server.models.location import Location
from openapi_server.models.attr import Attr

from backbone_server.controllers.base_controller import BaseController
from backbone_server.sampling_event.fetch import SamplingEventFetch
from backbone_server.location.fetch import LocationFetch

from backbone_server.errors.missing_key_exception import MissingKeyException

class EventSetFetch():

    @staticmethod
    def fetch_event_set_id(cursor, event_set_name):

        stmt = '''SELECT id FROM event_sets WHERE event_set_name = %s'''

        cursor.execute(stmt, (event_set_name,))

        res = cursor.fetchone()

        if not res:
            raise MissingKeyException("No such event set {}".format(event_set_name))

        return res[0]

    @staticmethod
    def fetch(cursor, event_set_id, studies, start, count):

        if not event_set_id:
            return None

        stmt = '''SELECT event_set_name FROM event_sets WHERE id = %s'''

        cursor.execute(stmt, (event_set_id,))

        res = cursor.fetchone()

        if not res:
            raise MissingKeyException("No such event set {}".format(event_set_id))

        event_set = EventSet(res[0])

        stmt = '''SELECT note_name, note_text FROM event_set_notes WHERE event_set_id = %s'''

        cursor.execute(stmt, (event_set_id,))

        event_set.notes = []
        for (name, value) in cursor:
            note = EventSetNote(name, value)
            event_set.notes.append(note)

        if len(event_set.notes) == 0:
            event_set.notes = None

        fields = '''SELECT DISTINCT sampling_events.id, doc'''
        query_body = ''' FROM sampling_events
                        JOIN event_set_members esm ON esm.sampling_event_id = sampling_events.id
                        LEFT JOIN original_samples ON original_samples.sampling_event_id = sampling_events.id
                        LEFT JOIN studies ON studies.id = original_samples.study_id
                        WHERE esm.event_set_id = %s'''

        args = (event_set_id,)

        count_args = args
        count_query = 'SELECT COUNT(sampling_events.id) ' + query_body

        if studies:
            filt = BaseController.study_filter(studies)
            if filt:
                query_body += ' AND (original_samples.id IS NULL OR ' + filt + ')'
                query_body += ' GROUP BY sampling_events.id'

        query_body = query_body + ''' ORDER BY doc, sampling_events.id'''

        if not (start is None and count is None):
            if count and count > 0:
                query_body = query_body + ' LIMIT %s OFFSET %s'
                args = args + (count, start)

        sampling_events = SamplingEvents([], 0)

        stmt = fields + query_body

        cursor.execute(stmt, args)

        samp_ids = []
        for samp_id, doc in cursor:
            if samp_id not in samp_ids:
                samp_ids.append(samp_id)

        locations = {}
        sampling_events.sampling_events = []
        for samp_id in samp_ids:
            event = SamplingEventFetch.fetch(cursor, samp_id, studies,
                                             locations=locations)
            if event:
                sampling_events.sampling_events.append(event)
        sampling_events.locations = locations


        if not (start is None and count is None):
            cursor.execute(count_query, count_args)
            res = cursor.fetchone()
            if res:
                sampling_events.count = res[0]
        else:
            sampling_events.count = len(sampling_events.sampling_events)

        sampling_events.attr_types = []

        col_query = '''select distinct attr_type from sampling_event_attrs se
                        JOIN attrs a ON se.sampling_event_id=a.id
                        JOIN event_set_members esm ON esm.sampling_event_id = se.sampling_event_id
                        WHERE esm.event_set_id = %s'''

        cursor.execute(col_query, (event_set_id,))
        for (attr_type,) in cursor:
            sampling_events.attr_types.append(attr_type)

        event_set.members = sampling_events

        return event_set
