from swagger_server.models.study import Study
from swagger_server.models.taxonomy import Taxonomy
from swagger_server.models.partner_species import PartnerSpecies
from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

class StudyFetch():


    @staticmethod
    def fetch(cursor, study_id):

        if not study_id:
            return None

        cursor.execute('''SELECT id, study_name, study_code FROM studies WHERE study_code = %s''',
                       (study_id[:4],))
        result = cursor.fetchone()

        study_uuid = None
        if result:
            study_uuid = result[0]
        else:
            raise MissingKeyException("No study {}".format(study_id))


        study = Study(name = result[1], code = result[2])

        stmt = '''SELECT id, study_id, partner_species FROM partner_species_identifiers WHERE
        study_id = %s'''
        cursor.execute( stmt, (study_uuid,))

        study.partner_species = []
        ps_id_map = {}

        for (psid, study_id, partner_species) in cursor:
            ps = PartnerSpecies([], partner_species = partner_species)
            ps_id_map[partner_species] = psid
            study.partner_species.append(ps)

        for ps in study.partner_species:
            psid = ps_id_map[ps.partner_species]
            stmt = '''SELECT taxonomies.id, taxonomies.rank, taxonomies.name FROM
            taxonomy_identifiers JOIN taxonomies ON taxonomies.id =
            taxonomy_identifiers.taxonomy_id WHERE partner_species_id = %s'''
            cursor.execute(stmt, (psid,))

            for (tid, rank, name) in cursor:
                taxa = Taxonomy(tid, name = name, rank = rank)
                ps.taxa.append(taxa)

        return study
