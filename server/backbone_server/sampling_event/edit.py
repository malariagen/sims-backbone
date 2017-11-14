from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

import uuid

class SamplingEventEdit():


    @staticmethod
    def fetch_study_id(cursor, sample):
        study_id = None

        if not sample.study_id:
            return study_id

        if len(sample.study_id) == 4:
            cursor.execute('''SELECT id FROM studies WHERE study_code = %s''',
                           (sample.study_id,))
        else:
            cursor.execute('''SELECT id FROM studies WHERE study_name = %s''',
                           (sample.study_id,))
        result = cursor.fetchone()

        if result:
            study_id = result[0]
        else:
            study_id = uuid.uuid4()
            cursor.execute('''INSERT INTO studies (id, study_code, study_name) VALUES (%s, %s,
                           %s)''', (study_id, sample.study_id[:4], sample.study_id))
        return study_id

    @staticmethod
    def add_identifiers(cursor, uuid_val, sample):
        if sample.identifiers:
            for ident in sample.identifiers:
                if ident.identifier_type != 'partner_id':
                    cursor.execute('''SELECT * FROM identifiers
                                   WHERE identifier_type = %s AND identifier_value = %s''',
                                   (ident.identifier_type, ident.identifier_value))
                    if cursor.fetchone():
                        raise DuplicateKeyException("Error inserting sample identifier {} {}"
                                                    .format(ident.identifier_type, sample))

                stmt = '''INSERT INTO identifiers (sample_id, identifier_type, identifier_value)
                VALUES (%s, %s, %s)'''
                cursor.execute(stmt, (uuid_val, ident.identifier_type, ident.identifier_value))



