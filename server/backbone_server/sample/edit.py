from backbone_server.errors.duplicate_key_exception import DuplicateKeyException


class SampleEdit():


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



