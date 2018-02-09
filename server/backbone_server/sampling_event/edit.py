from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

import uuid

class SamplingEventEdit():


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
    def fetch_partner_species(cursor, sample, study_id):
        partner_species = None

        if not sample.partner_species:
            return partner_species

        cursor.execute('''SELECT id FROM partner_species_identifiers WHERE study_id = %s AND
                       partner_species = %s''',
                           (study_id, sample.partner_species))
        result = cursor.fetchone()

        if result:
            partner_species = result[0]
        else:
            partner_species = uuid.uuid4()
            cursor.execute('''INSERT INTO partner_species_identifiers (id, study_id,
                           partner_species) VALUES (%s, %s, %s)''',
                           (partner_species, study_id, sample.partner_species))
        return partner_species

    @staticmethod
    def add_identifiers(cursor, uuid_val, sample):
        if sample.identifiers:
            for ident in sample.identifiers:
                if ident.identifier_type != 'partner_id':
                    cursor.execute('''SELECT * FROM identifiers
                                   WHERE identifier_type = %s AND identifier_value = %s AND
                                   identifier_source = %s''',
                                   (ident.identifier_type, ident.identifier_value,
                                    ident.identifier_source))
                    if cursor.fetchone():
                        raise DuplicateKeyException("Error inserting sample identifier {} {}"
                                                    .format(ident.identifier_type, sample))

                    cursor.execute('''SELECT * FROM identifiers
                                   WHERE identifier_type = %s AND identifier_value = %s AND
                                   sample_id != %s''',
                                   (ident.identifier_type, ident.identifier_value,
                                    uuid_val))
                    if cursor.fetchone():
                        raise DuplicateKeyException("Error inserting sample identifier {} {}"
                                                    .format(ident.identifier_type, sample))

                stmt = '''INSERT INTO identifiers 
                    (sample_id, identifier_type, identifier_value, identifier_source)
                    VALUES (%s, %s, %s, %s)'''
                cursor.execute(stmt, (uuid_val, ident.identifier_type, ident.identifier_value,
                                      ident.identifier_source))



