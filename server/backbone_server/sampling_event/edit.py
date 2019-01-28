from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.nested_edit_exception import NestedEditException
from backbone_server.errors.invalid_date_exception import InvalidDateException

from backbone_server.location.fetch import LocationFetch
import uuid

from datetime import datetime

class SamplingEventEdit():


    @staticmethod
    def check_date(sampling_event):
        present = datetime.date(datetime.now())

        if sampling_event.doc:
            if sampling_event.doc > present:
                raise InvalidDateException("The date of collection is in the future {}".format(sampling_event.doc))

    @staticmethod
    def check_location_details(cursor, location_id, location):

        current_location = None

        if location_id:
            current_location = LocationFetch.fetch(cursor, location_id)

            cli = current_location.attrs

            #It's OK if the location id is set but the location object not filled in
            if location:
                idents = location.attrs

                if location != current_location:
                    raise NestedEditException("Implied location edit not allowed for {}".format(location_id))

        return current_location

    @staticmethod
    def fetch_study_id(cursor, study_name, create):
        study_id = None

        if not study_name:
            return study_id

        cursor.execute('''SELECT id FROM studies WHERE study_code = %s''', (study_name[:4],))
        result = cursor.fetchone()

        if result:
            study_id = result[0]
        else:
            if not create:
                return None
            study_id = uuid.uuid4()
            cursor.execute('''INSERT INTO studies (id, study_code, study_name) VALUES (%s, %s,
                           %s)''', (study_id, study_name[:4], study_name))
        return study_id


    @staticmethod
    def add_attrs(cursor, uuid_val, sampling_event):
        if sampling_event.attrs:
            for ident in sampling_event.attrs:
                study_id = None

                if ident.study_name:
                    study_id = SamplingEventEdit.fetch_study_id(cursor,
                                                                ident.study_name,
                                                                True)

                if not (ident.attr_type == 'partner_id' or \
                        ident.attr_type == 'individual_id'):
                    cursor.execute('''SELECT * FROM attrs
                                   JOIN sampling_event_attrs ON sampling_event_attrs.attr_id =
                                   attrs.id
                                   WHERE attr_type = %s AND attr_value = %s AND
                                   attr_source = %s''',
                                   (ident.attr_type, ident.attr_value,
                                    ident.attr_source))
                    if cursor.fetchone():
                        raise DuplicateKeyException("Error inserting sampling_event attr {} {}"
                                                    .format(ident.attr_type, sampling_event))
                    cursor.execute('''SELECT * FROM attrs
                                   JOIN sampling_event_attrs ON sampling_event_attrs.attr_id =
                                   attrs.id
                                   WHERE attr_type = %s AND attr_value = %s AND
                                   sampling_event_id != %s''',
                                   (ident.attr_type, ident.attr_value,
                                    uuid_val))
                    if cursor.fetchone():
                        raise DuplicateKeyException("Error inserting sampling_event attr {} {}"
                                                    .format(ident.attr_type, sampling_event))

                attr_id = uuid.uuid4()
                stmt = '''INSERT INTO attrs
                    (id, attr_type, attr_value, attr_source, study_id)
                    VALUES (%s, %s, %s, %s, %s)'''
                cursor.execute(stmt, (attr_id, ident.attr_type, ident.attr_value,
                                      ident.attr_source, study_id))

                stmt = '''INSERT INTO sampling_event_attrs
                    (sampling_event_id, attr_id)
                    VALUES (%s, %s)'''
                cursor.execute(stmt, (uuid_val, attr_id))

