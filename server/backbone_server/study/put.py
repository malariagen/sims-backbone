import uuid
import logging

import psycopg2

from openapi_server.models.study import Study
from openapi_server.models.partner_species import PartnerSpecies

from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.integrity_exception import IntegrityException

from backbone_server.study.fetch import StudyFetch
from backbone_server.study.edit import StudyEdit

class StudyPut():

    def __init__(self, conn, cursor=None):
        self._logger = logging.getLogger(__name__)
        self._connection = conn
        self._cursor = cursor


    def put(self, study_id, study):

        if not study_id:
            raise MissingKeyException("No study {}".format(study_id))

        with self._connection:
            with self._connection.cursor() as cursor:

                return self.run_command(cursor, study_id, study)


    def run_command(self, cursor, study_id, study):

        cursor.execute('''SELECT id, study_name, study_code FROM studies WHERE study_code = %s''', (study_id[:4],))

        result = cursor.fetchone()

        study_uuid = None
        if result:
            study_uuid = result[0]
        else:
            raise MissingKeyException("No study {}".format(study_id))

        stmt = '''UPDATE studies
                    SET study_name = %s, ethics_expiry = %s
                    WHERE id = %s'''
        args = (study.name, study.ethics_expiry, study_uuid)
        try:
            cursor.execute(stmt, args)

            stmt = '''SELECT id, study_id, partner_species FROM partner_species_identifiers WHERE
            study_id = %s'''
            cursor.execute( stmt, (study_uuid,))

            ps_ids = []

            for (psid, stud_id, partner_species) in cursor:
                ps = PartnerSpecies([], partner_species=partner_species)
                ps_ids.append(psid)

            for psid in ps_ids:
                cursor.execute('''DELETE FROM taxonomy_identifiers WHERE
                               partner_species_id = %s''',
                               (psid,))

        #The partner_species really relates to the sampling event not the study
        #so can't just blow away and rebuild
            for species in study.partner_species:
                species_id = StudyEdit.fetch_partner_species(cursor, species, study_uuid)
                StudyEdit.update_species_identifiers(cursor, species_id, species.taxa)

            for shipment in study.expected_samples:
                if shipment.expected_samples_id:
                    shipment_id = shipment.expected_samples_id
                else:
                    shipment_id = uuid.uuid4()
                    cursor.execute('INSERT INTO expected_samples (id, study_id) VALUES (%s, %s)',
                                   (shipment_id, study_uuid))

                expected_species = StudyEdit.fetch_expected_partner_species(cursor, shipment, study_uuid)

                cursor.execute('''UPDATE expected_samples SET date_of_arrival=%s,
                               sample_count=%s, partner_species_id=%s  WHERE
                               id=%s''',
                               (shipment.date_of_arrival,
                                shipment.sample_count,
                                expected_species,
                                shipment_id))

                StudyEdit.update_species_identifiers(cursor, expected_species,
                                                shipment.expected_taxonomies)

        except psycopg2.IntegrityError as err:
            raise IntegrityException("Error updating study {}".format(study)) from err


        updated_study = StudyFetch.fetch(cursor, study_id)

        return updated_study
