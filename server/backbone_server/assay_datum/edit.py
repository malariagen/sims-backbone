from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

import uuid

class AssayDatumEdit():


    @staticmethod
    def add_attrs(cursor, uuid_val, assay_datum):
        if assay_datum.attrs:
            for ident in assay_datum.attrs:
                cursor.execute('''SELECT * FROM attrs
                               JOIN assay_datum_attrs ON assay_datum_attrs.attr_id =
                               attrs.id
                               WHERE attr_type = %s AND attr_value = %s AND
                               attr_source = %s''',
                               (ident.attr_type, ident.attr_value,
                                ident.attr_source))
                if cursor.fetchone():
                    raise DuplicateKeyException("Error inserting assay_datum attr {} {}"
                                                .format(ident.attr_type, assay_datum))

                cursor.execute('''SELECT * FROM attrs
                               JOIN assay_datum_attrs ON assay_datum_attrs.attr_id =
                               attrs.id
                               WHERE attr_type = %s AND attr_value = %s AND
                               assay_datum_id != %s''',
                               (ident.attr_type, ident.attr_value,
                                uuid_val))
                if cursor.fetchone():
                    raise DuplicateKeyException("Error inserting assay_datum attr {} {}"
                                                .format(ident.attr_type, assay_datum))

                attr_id = uuid.uuid4()
                stmt = '''INSERT INTO attrs
                    (id, attr_type, attr_value, attr_source)
                    VALUES (%s, %s, %s, %s)'''
                cursor.execute(stmt, (attr_id, ident.attr_type, ident.attr_value,
                                      ident.attr_source))

                stmt = '''INSERT INTO assay_datum_attrs
                    (assay_datum_id, attr_id)
                    VALUES (%s, %s)'''
                cursor.execute(stmt, (uuid_val, attr_id))

