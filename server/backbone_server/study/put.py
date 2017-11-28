from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.integrity_exception import IntegrityException

from backbone_server.study.fetch import StudyFetch

import uuid

from swagger_server.models.study import Study
from swagger_server.models.partner_species import PartnerSpecies

import mysql.connector
from mysql.connector import errorcode
import psycopg2

import logging

class StudyPut():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def put(self, study_id, study):

        if not study_id:
            raise MissingKeyException("No study {}".format(study_id))

        with self._connection:
            with self._connection.cursor() as cursor:

                cursor.execute('''SELECT id, study_name, study_code FROM studies WHERE study_code = %s''', (study_id[:4],))
                result = cursor.fetchone()

                study_uuid = None
                if result:
                    study_uuid = result[0]
                else:
                    raise MissingKeyException("No study {}".format(study_id))

                stmt = '''UPDATE studies 
                            SET study_name = %s
                            WHERE id = %s''' 
                args = (study.name, study_uuid)
                try:
                    cursor.execute(stmt, args)

                    stmt = '''SELECT id, study_id, partner_species FROM partner_species_identifiers WHERE
                    study_id = %s'''
                    cursor.execute( stmt, (study_uuid,))

                    ps_ids = []

                    for (psid, stud_id, partner_species) in cursor:
                        ps = PartnerSpecies([], partner_species = partner_species)
                        ps_ids.append(psid)

                    for psid in ps_ids:
                        cursor.execute('''DELETE FROM taxonomy_identifiers WHERE
                                       partner_species_id = %s''',
                                       (psid,))

                    #The partner_species really relates to the sampling event not the study
                    #so can't just blow away and rebuild
                    for species in study.partner_species:
                        stmt = '''SELECT id, study_id, partner_species FROM partner_species_identifiers WHERE
                        study_id = %s AND partner_species = %s'''
                        cursor.execute( stmt, (study_uuid, species.partner_species,))
                        result = cursor.fetchone()
                        psid = None
                        if result:
                            psid = result[0]
                        else:
                            psid = uuid.uuid4()
                            cursor.execute('''INSERT INTO partner_species_identifiers (id, study_id,
                                           partner_species) VALUES (%s, %s, %s)''', (psid, study_uuid,
                                                                                     species.partner_species))
                        for taxa in species.taxa:
                            cursor.execute('''INSERT INTO taxonomy_identifiers (taxonomy_id,
                                           partner_species_id) VALUES (%s, %s)''', (taxa.taxonomy_id, psid))

                except mysql.connector.Error as err:
                    raise IntegrityException("Error updating study {}".format(study)) from err
                except psycopg2.IntegrityError as err:
                    raise IntegrityException("Error updating study {}".format(study)) from err


                updated_study = StudyFetch.fetch(cursor, study_id)

        return updated_study
