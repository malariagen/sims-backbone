import logging

from backbone_server.event_set.edit import EventSetEdit
from backbone_server.event_set.fetch import EventSetFetch

class EventSetPut():

    def __init__(self, conn, cursor=None):
        self._logger = logging.getLogger(__name__)
        self._connection = conn
        self._cursor = cursor


    def put(self, event_set_name, event_set, studies):

        with self._connection:
            with self._connection.cursor() as cursor:
                return self.run_command(cursor, event_set_name, event_set,
                                        studies)

    def run_command(self, cursor, event_set_name, event_set, studies):

        event_set_id = EventSetFetch.fetch_event_set_id(cursor, event_set_name)

        args = (event_set_id,)

        #Allows the possibility of editing the metadata without the events
        if event_set.members and len(event_set.members.sampling_events) > 0:
            stmt = '''DELETE FROM event_set_members WHERE event_set_id = %s'''
            cursor.execute(stmt, args)

            EventSetEdit.add_sampling_events(cursor, event_set_id,
                                             event_set.members.sampling_events)

        stmt = '''DELETE FROM event_set_notes WHERE event_set_id = %s'''
        cursor.execute(stmt, args)

        EventSetEdit.add_notes(cursor, event_set_id, event_set.notes)


        ret = EventSetFetch.fetch(cursor, event_set_id, studies, None, None)

        return ret
