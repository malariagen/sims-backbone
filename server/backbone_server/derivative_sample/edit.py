from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

import uuid


class DerivativeSampleEdit():

    @staticmethod
    def add_attrs(cursor, uuid_val, derivative_sample):
        if derivative_sample.attrs:

            not_unique = [ 'plate_name', 'plate_location' ]
            for ident in derivative_sample.attrs:

                if ident.attr_type not in not_unique:
                    cursor.execute('''SELECT * FROM attrs
                                   JOIN derivative_sample_attrs ON derivative_sample_attrs.attr_id =
                                   attrs.id
                                   WHERE attr_type = %s AND attr_value = %s AND
                                   attr_source = %s''',
                                   (ident.attr_type, ident.attr_value,
                                    ident.attr_source))
                    if cursor.fetchone():
                        raise DuplicateKeyException("Error inserting derivative_sample attr {} {}"
                                                    .format(ident.attr_type, derivative_sample))

                    cursor.execute('''SELECT * FROM attrs
                                   JOIN derivative_sample_attrs ON derivative_sample_attrs.attr_id =
                                   attrs.id
                                   WHERE attr_type = %s AND attr_value = %s AND
                                   derivative_sample_id != %s''',
                                   (ident.attr_type, ident.attr_value,
                                    uuid_val))
                    if cursor.fetchone():
                        raise DuplicateKeyException("Error inserting derivative_sample attr {} {}"
                                                    .format(ident.attr_type, derivative_sample))

                attr_id = uuid.uuid4()
                stmt = '''INSERT INTO attrs
                    (id, attr_type, attr_value, attr_source)
                    VALUES (%s, %s, %s, %s)'''
                cursor.execute(stmt, (attr_id, ident.attr_type, ident.attr_value,
                                      ident.attr_source))

                stmt = '''INSERT INTO derivative_sample_attrs
                    (derivative_sample_id, attr_id)
                    VALUES (%s, %s)'''
                cursor.execute(stmt, (uuid_val, attr_id))
