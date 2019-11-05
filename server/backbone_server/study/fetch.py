import logging

from openapi_server.models.study import Study
from openapi_server.models.taxonomy import Taxonomy
from openapi_server.models.partner_species import PartnerSpecies
from openapi_server.models.expected_samples import ExpectedSamples

from backbone_server.location.gets import LocationsGet
from backbone_server.errors.missing_key_exception import MissingKeyException


class StudyFetch():


    @staticmethod
    def get_taxonomies(cursor, psid):

        taxas = []
        stmt = '''SELECT taxonomies.id, taxonomies.rank, taxonomies.name
        FROM taxonomy_identifiers
        JOIN taxonomies ON taxonomies.id = taxonomy_identifiers.taxonomy_id
        WHERE partner_species_id = %s'''
        cursor.execute(stmt, (psid,))

        for (tid, rank, name) in cursor:
            taxa = Taxonomy(tid, name=name, rank=rank)
            taxas.append(taxa)

        return taxas

    @staticmethod
    def fetch(cursor, study_id):

        if not study_id:
            return None

        cursor.execute('''SELECT id, study_name, study_code, ethics_expiry FROM studies WHERE study_code = %s''',
                       (study_id[:4],))
        result = cursor.fetchone()

        study_uuid = None
        if result:
            study_uuid = result[0]
        else:
            raise MissingKeyException("No study {}".format(study_id))


        study = Study(name=result[1], code=result[2], ethics_expiry=result[3])

        stmt = '''SELECT id, study_id, partner_species FROM partner_species_identifiers WHERE
        study_id = %s'''
        cursor.execute(stmt, (study_uuid,))

        arr_partner_species = []
        ps_id_map = {}

        for (psid, study_uuid, partner_species) in cursor:
            ps = PartnerSpecies([], partner_species=partner_species)
            ps_id_map[partner_species] = psid
            arr_partner_species.append(ps)

        for ps in arr_partner_species:
            psid = ps_id_map[ps.partner_species]
            ps.taxa = StudyFetch.get_taxonomies(cursor, psid)

        study.partner_species = arr_partner_species

        get = LocationsGet(cursor.connection)

        locs = get.get(study_id)

        study.locations = locs

        stmt = '''SELECT id, study_id, date_of_arrival, sample_count,
        partner_species_id FROM expected_samples WHERE study_id = %s'''
        cursor.execute(stmt, (study_uuid,))

        expected_samples = []

        e_species = {}
        for (psid, study_uuid, doa, samp_count, partner_species) in cursor:
            es = ExpectedSamples(str(psid), date_of_arrival=doa,
                                 sample_count=samp_count)
            e_species[str(psid)] = partner_species
            expected_samples.append(es)

        for es in expected_samples:
            stmt = '''SELECT id, study_id, partner_species FROM partner_species_identifiers WHERE
            id = %s'''
            cursor.execute(stmt, (e_species[es.expected_samples_id], ))

            for (psid, study_uuid, partner_species) in cursor:
                ps_id_map[partner_species] = psid
                es.expected_species = partner_species

            if es.expected_species and es.expected_species in ps_id_map:
                es.expected_taxonomies = StudyFetch.get_taxonomies(cursor,
                                                                   ps_id_map[es.expected_species])
        study.expected_samples = expected_samples

        return study
