import uuid

class StudyEdit():

    @staticmethod
    def update_species_identifiers(cursor, psid, taxonomies):

        if taxonomies:
            for taxa in taxonomies:
                cursor.execute('''INSERT INTO taxonomy_identifiers (taxonomy_id,
                               partner_species_id) VALUES (%s, %s)''', (taxa.taxonomy_id, psid))

    @staticmethod
    def fetch_partner_species(cursor, species, study_id):
        partner_species = None

        if not species.partner_species:
            return partner_species

        cursor.execute('''SELECT id FROM partner_species_identifiers WHERE study_id = %s AND
                       partner_species = %s''',
                       (study_id, species.partner_species))
        result = cursor.fetchone()

        if result:
            partner_species = result[0]
        else:
            partner_species = uuid.uuid4()
            cursor.execute('''INSERT INTO partner_species_identifiers (id, study_id,
                           partner_species) VALUES (%s, %s, %s)''',
                           (partner_species, study_id, species.partner_species))
        return partner_species

    @staticmethod
    def fetch_expected_partner_species(cursor, shipment, study_id):
        partner_species = None

        if not shipment.expected_species:
            return partner_species

        cursor.execute('''SELECT id FROM partner_species_identifiers WHERE study_id = %s AND
                       partner_species = %s''',
                       (study_id, shipment.expected_species))
        result = cursor.fetchone()

        if result:
            partner_species = result[0]
        else:
            partner_species = uuid.uuid4()
            cursor.execute('''INSERT INTO partner_species_identifiers (id, study_id,
                           partner_species) VALUES (%s, %s, %s)''',
                           (partner_species, study_id, shipment.expected_species))
        return partner_species

    @staticmethod
    def clean_up_taxonomies(cursor):

        unused_species = '''(select DISTINCT partner_species_identifiers.id from partner_species_identifiers LEFT JOIN studies ON studies.id = study_id
        LEFT JOIN original_samples ON original_samples.study_id = studies.id
        LEFT JOIN expected_samples ON expected_samples.study_id = studies.id
        WHERE original_samples.id IS NULL AND expected_samples.id IS NULL)'''
        unused_idents = 'DELETE FROM taxonomy_identifiers WHERE partner_species_id IN ' + unused_species
        unused_species_idents = 'DELETE FROM partner_species_identifiers WHERE id IN ' + unused_species

        cursor.execute(unused_idents)
        cursor.execute(unused_species_idents)
