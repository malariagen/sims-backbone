from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

import uuid

class DerivedSampleEdit():


    @staticmethod
    def add_attrs(cursor, uuid_val, derived_sample):
        if derived_sample.attrs:
            for ident in derived_sample.attrs:
                cursor.execute('''SELECT * FROM attrs
                               JOIN derived_sample_attrs ON derived_sample_attrs.attr_id =
                               attrs.id
                               WHERE attr_type = %s AND attr_value = %s AND
                               attr_source = %s''',
                               (ident.attr_type, ident.attr_value,
                                ident.attr_source))
                if cursor.fetchone():
                    raise DuplicateKeyException("Error inserting derived_sample attr {} {}"
                                                .format(ident.attr_type, derived_sample))

                cursor.execute('''SELECT * FROM attrs
                               JOIN derived_sample_attrs ON derived_sample_attrs.attr_id =
                               attrs.id
                               WHERE attr_type = %s AND attr_value = %s AND
                               derived_sample_id != %s''',
                               (ident.attr_type, ident.attr_value,
                                uuid_val))
                if cursor.fetchone():
                    raise DuplicateKeyException("Error inserting derived_sample attr {} {}"
                                                .format(ident.attr_type, derived_sample))

                attr_id = uuid.uuid4()
                stmt = '''INSERT INTO attrs
                    (id, attr_type, attr_value, attr_source)
                    VALUES (%s, %s, %s, %s)'''
                cursor.execute(stmt, (attr_id, ident.attr_type, ident.attr_value,
                                      ident.attr_source))

                stmt = '''INSERT INTO derived_sample_attrs
                    (derived_sample_id, attr_id)
                    VALUES (%s, %s)'''
                cursor.execute(stmt, (uuid_val, attr_id))

