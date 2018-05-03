from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from swagger_server.models.location import Location
from swagger_server.models.identifier import Identifier

from backbone_server.location.fetch import LocationFetch
from backbone_server.sampling_event.edit import SamplingEventEdit

import psycopg2

import logging
import uuid

class LocationEdit():

    _insert_ident_stmt = '''INSERT INTO location_identifiers 
                    (location_id, study_id, identifier_type, identifier_value, identifier_source)
                    VALUES (%s, %s, %s, %s, %s)'''


    @staticmethod
    def clean_up_identifiers(cursor, location_id, old_study_id):

        if not location_id:
            return

        if not old_study_id:
            return

        stmt = '''select li.study_id, li.location_id FROM location_identifiers li
        LEFT JOIN sampling_events se ON
            (se.location_id = li.location_id OR se.proxy_location_id = li.location_id)
                AND se.study_id = li.study_id
        WHERE se.id IS NULL AND li.location_id = %s group by li.study_id, li.location_id;'''

        cursor.execute(stmt, (location_id,))

        obsolete_idents = []
        for (study_id, location_id) in cursor:
            obsolete_idents.append(study_id)

        delete_stmt = 'DELETE FROM location_identifiers WHERE location_id = %s AND study_id = %s'

        for obsolete_ident in obsolete_idents:
            if obsolete_ident == old_study_id:
                cursor.execute(delete_stmt, (location_id, obsolete_ident))

    @staticmethod
    def add_identifiers(cursor, uuid_val, location):

        studies = []

        try:
            if location.identifiers:
                for ident in location.identifiers:
                    study_id = None
                    if ident.study_name:
                        study_id = SamplingEventEdit.fetch_study_id(cursor, ident.study_name, True)
                        if study_id in studies:
                            raise DuplicateKeyException("Error inserting location {}".format(location))
                        studies.append(study_id)

                    cursor.execute(LocationEdit._insert_ident_stmt, (uuid_val, study_id, ident.identifier_type,
                                          ident.identifier_value, ident.identifier_source))

        except psycopg2.IntegrityError as err:
            print(err.pgcode)
            print(err.pgerror)
            raise DuplicateKeyException("Error inserting location {}".format(location)) from err


    @staticmethod
    def update_identifier_study(cursor, location_id, old_study_id, new_study_id):

        if not location_id:
            return

        old_identifiers = []

        stmt = '''SELECT identifier_type, identifier_value, identifier_source, study_name FROM location_identifiers
                    JOIN studies s ON s.id = location_identifiers.study_id
                    WHERE location_id = %s AND study_id = %s'''

        cursor.execute(stmt, (location_id, old_study_id))

        for (identifier_type, identifier_value, identifier_source, study_name) in cursor:
            old_identifiers.append(Identifier(identifier_type=identifier_type,
                                          identifier_value=identifier_value,
                                          identifier_source=identifier_source,
                                             study_name=study_name))

        new_identifiers = []

        cursor.execute(stmt, (location_id, new_study_id))

        for (identifier_type, identifier_value, identifier_source, study_name) in cursor:
            new_identifiers.append(Identifier(identifier_type=identifier_type,
                                          identifier_value=identifier_value,
                                          identifier_source=identifier_source,
                                             study_name=study_name))

        if len(new_identifiers) == 0:
            if len(old_identifiers) == 1:
                cursor.execute(LocationEdit._insert_ident_stmt, (location_id, new_study_id,
                                                             old_identifiers[0].identifier_type,
                                                             old_identifiers[0].identifier_value,
                                                             old_identifiers[0].identifier_source))

    @staticmethod
    def check_for_duplicate(cursor, location, location_id):

        stmt = '''SELECT id, ST_X(location) as latitude, ST_Y(location) as longitude,
        accuracy, curated_name, curation_method, country
                       FROM locations WHERE  location = ST_SetSRID(ST_MakePoint(%s, %s), 4326)'''
        cursor.execute( stmt, (location.latitude, location.longitude,))

        existing_locations = []

        for (loc_id, latitude, longitude, accuracy, curated_name,
             curation_method, country) in cursor:
            if location_id is None or loc_id != location_id:
                existing_locations.append(loc_id)


        for existing_id in existing_locations:
            existing_location = LocationFetch.fetch(cursor, existing_id)

            if existing_location.identifiers:

                for existing_ident in existing_location.identifiers:
                    for ident in location.identifiers:
                        if ident.identifier_type == existing_ident.identifier_type and\
                            ident.identifier_value == existing_ident.identifier_value and\
                            ident.study_name == existing_ident.study_name:
                            raise DuplicateKeyException("Error updating location - duplicate with {}".format(existing_location))

