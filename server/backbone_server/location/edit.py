import logging
import uuid

import psycopg2

from openapi_server.models.location import Location
from openapi_server.models.attr import Attr

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.sampling_event.edit import SamplingEventEdit
from backbone_server.location.fetch import LocationFetch

class LocationEdit():

    _insert_ident_stmt = '''INSERT INTO location_attrs
                    (location_id, study_id, attr_type, attr_value, attr_source)
                    VALUES (%s, %s, %s, %s, %s)'''


    @staticmethod
    def get_or_create_location_attr_id(cursor, ident):

        study_id = None
        if ident.study_name:
            study_id = SamplingEventEdit.fetch_study_id(cursor, ident.study_name, True)
        stmt = '''SELECT id FROM attrs
                JOIN location_attrs la ON la.attr_id = attrs.id
                WHERE attr_type=%s AND attr_value=%s AND attr_source=%s'''
        args = (ident.attr_type, ident.attr_value, ident.attr_source)

        if study_id:
            stmt += ' AND study_id = %s'
            args = args + (study_id,)

        cursor.execute(stmt, args)

        res = cursor.fetchone()

        if res:
            return res[0], study_id

        uuid_val = uuid.uuid4()

        insert_stmt = '''INSERT INTO attrs
                    (id, study_id, attr_type, attr_value, attr_source)
                    VALUES (%s, %s, %s, %s, %s)'''

        cursor.execute(insert_stmt, (uuid_val, study_id, ident.attr_type, ident.attr_value, ident.attr_source))

        return uuid_val,study_id


    @staticmethod
    def add_attrs(cursor, uuid_val, location):

        studies = []
        study_attrs = {}

        try:
            if location.attrs:
                for ident in location.attrs:
                    attr_id, study_id = LocationEdit.get_or_create_location_attr_id(cursor, ident)
                    if ident.study_name:
                        if ident.attr_type in study_attrs:
                            studies = study_attrs[ident.attr_type]
                            if study_id in studies:
                                raise DuplicateKeyException("Error inserting location - duplicate name for study {}".format(location))
                        else:
                            study_attrs[ident.attr_type] = []
                        study_attrs[ident.attr_type].append(study_id)

                    cursor.execute('INSERT INTO location_attrs(location_id, attr_id) VALUES (%s, %s)',
                                   (uuid_val, attr_id))

        except psycopg2.IntegrityError as err:
            raise DuplicateKeyException("Error inserting location {}".format(location)) from err


    @staticmethod
    def update_attr_study(cursor, location_id, old_study_id, new_study_id):

        if not location_id:
            return

        old_attrs = []

        stmt = '''SELECT DISTINCT attr_type, attr_value, attr_source, study_name FROM location_attrs
        JOIN attrs a ON a.id = location_attrs.attr_id
                    JOIN studies s ON s.id = a.study_id
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
                attr_id, study_id = LocationEdit.get_or_create_location_attr_id(cursor, old_attrs[0])
                cursor.execute('INSERT INTO location_attrs(location_id, attr_id) VALUES (%s, %s)',
                                   (location_id, attr_id))
                cursor.execute('UPDATE attrs SET study_id=%s WHERE id=%s',(new_study_id, attr_id))

    @staticmethod
    def check_for_duplicate(cursor, location, location_id, studies):

        stmt = '''SELECT id, ST_X(location) as latitude, ST_Y(location) as longitude,
        accuracy, curated_name, curation_method, country
                       FROM locations WHERE  location = ST_SetSRID(ST_MakePoint(%s, %s), 4326)'''
        cursor.execute(stmt, (location.latitude, location.longitude,))

        existing_locations = []

        for (loc_id, latitude, longitude, accuracy, curated_name,
             curation_method, country) in cursor:
            if str(loc_id) != location_id:
                existing_locations.append(loc_id)

        for existing_id in existing_locations:
            existing_location = LocationFetch.fetch(cursor, existing_id,
                                                    studies)

            if existing_location.attrs:

                for existing_ident in existing_location.attrs:
                    for ident in location.attrs:
                        if ident.attr_type == existing_ident.attr_type and\
                            ident.attr_value == existing_ident.attr_value and\
                            ident.study_name == existing_ident.study_name:
                            raise DuplicateKeyException("Error updating location - {} {} {} duplicate with {}".format(ident.attr_type,
                                                                   ident.attr_value,
                                                                   ident.study_name,existing_location))
