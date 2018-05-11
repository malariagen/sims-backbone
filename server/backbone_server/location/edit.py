from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from swagger_server.models.location import Location
from swagger_server.models.attr import Attr

from backbone_server.location.fetch import LocationFetch
from backbone_server.sampling_event.edit import SamplingEventEdit

import psycopg2

import logging
import uuid

class LocationEdit():

    _insert_ident_stmt = '''INSERT INTO location_attrs 
                    (location_id, study_id, attr_type, attr_value, attr_source)
                    VALUES (%s, %s, %s, %s, %s)'''


    @staticmethod
    def clean_up_attrs(cursor, location_id, old_study_id):

        if not location_id:
            return

        if not old_study_id:
            return

        stmt = '''select li.study_id, li.location_id FROM location_attrs li
        LEFT JOIN sampling_events se ON
            (se.location_id = li.location_id OR se.proxy_location_id = li.location_id)
                AND se.study_id = li.study_id
        WHERE se.id IS NULL AND li.location_id = %s group by li.study_id, li.location_id;'''

        cursor.execute(stmt, (location_id,))

        obsolete_idents = []
        for (study_id, location_id) in cursor:
            obsolete_idents.append(study_id)

        delete_stmt = 'DELETE FROM location_attrs WHERE location_id = %s AND study_id = %s'

        for obsolete_ident in obsolete_idents:
            if obsolete_ident == old_study_id:
                cursor.execute(delete_stmt, (location_id, obsolete_ident))

    @staticmethod
    def add_attrs(cursor, uuid_val, location):

        studies = []

        try:
            if location.attrs:
                for ident in location.attrs:
                    study_id = None
                    if ident.study_name:
                        study_id = SamplingEventEdit.fetch_study_id(cursor, ident.study_name, True)
                        if study_id in studies:
                            raise DuplicateKeyException("Error inserting location {}".format(location))
                        studies.append(study_id)

                    cursor.execute(LocationEdit._insert_ident_stmt, (uuid_val, study_id, ident.attr_type,
                                          ident.attr_value, ident.attr_source))

        except psycopg2.IntegrityError as err:
            print(err.pgcode)
            print(err.pgerror)
            raise DuplicateKeyException("Error inserting location {}".format(location)) from err


    @staticmethod
    def update_attr_study(cursor, location_id, old_study_id, new_study_id):

        if not location_id:
            return

        old_attrs = []

        stmt = '''SELECT attr_type, attr_value, attr_source, study_name FROM location_attrs
                    JOIN studies s ON s.id = location_attrs.study_id
                    WHERE location_id = %s AND study_id = %s'''

        cursor.execute(stmt, (location_id, old_study_id))

        for (attr_type, attr_value, attr_source, study_name) in cursor:
            old_attrs.append(Attr(attr_type=attr_type,
                                          attr_value=attr_value,
                                          attr_source=attr_source,
                                             study_name=study_name))

        new_attrs = []

        cursor.execute(stmt, (location_id, new_study_id))

        for (attr_type, attr_value, attr_source, study_name) in cursor:
            new_attrs.append(Attr(attr_type=attr_type,
                                          attr_value=attr_value,
                                          attr_source=attr_source,
                                             study_name=study_name))

        if len(new_attrs) == 0:
            if len(old_attrs) == 1:
                cursor.execute(LocationEdit._insert_ident_stmt, (location_id, new_study_id,
                                                             old_attrs[0].attr_type,
                                                             old_attrs[0].attr_value,
                                                             old_attrs[0].attr_source))

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

            if existing_location.attrs:

                for existing_ident in existing_location.attrs:
                    for ident in location.attrs:
                        if ident.attr_type == existing_ident.attr_type and\
                            ident.attr_value == existing_ident.attr_value and\
                            ident.study_name == existing_ident.study_name:
                            raise DuplicateKeyException("Error updating location - duplicate with {}".format(existing_location))

