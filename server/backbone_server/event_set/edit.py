
class EventSetEdit():


    @staticmethod
    def add_sampling_event(cursor, event_set_id, sampling_event):
        if sampling_event:
            stmt = '''INSERT INTO event_set_members (event_set_id, sampling_event_id) VALUES (%s, %s)'''
            cursor.execute(stmt, (event_set_id, sampling_event.sampling_event_id))


    @staticmethod
    def add_sampling_events(cursor, event_set_id, sampling_events):
        if sampling_events:
            for event in sampling_events:
                EventSetEdit.add_sampling_event(cursor, event_set_id, event)



    @staticmethod
    def add_note(cursor, event_set_id, note):
        if note:
            stmt = '''INSERT INTO event_set_notes (event_set_id, note_name, note_text) VALUES
            (%s, %s, %s)'''
            cursor.execute(stmt, (event_set_id, note.note_name, note.note_text))


    @staticmethod
    def add_notes(cursor, event_set_id, notes):
        if notes:
            for note in notes:
                EventSetEdit.add_note(cursor, event_set_id, note)

