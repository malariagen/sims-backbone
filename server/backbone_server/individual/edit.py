from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from openapi_server.models.individual import Individual
from openapi_server.models.attr import Attr

from backbone_server.individual.fetch import IndividualFetch
from backbone_server.sampling_event.edit import SamplingEventEdit

import psycopg2

import logging
import uuid

class IndividualEdit():

    _insert_ident_stmt = '''INSERT INTO individual_attrs
                    (individual_id, study_id, attr_type, attr_value, attr_source)
                    VALUES (%s, %s, %s, %s, %s)'''


    @staticmethod
    def get_or_create_individual_attr_id(cursor, ident, create=True):

        study_id = None
        if ident.study_name:
            study_id = SamplingEventEdit.fetch_study_id(cursor, ident.study_name, True)
        stmt = '''SELECT id FROM attrs
                JOIN individual_attrs la ON la.attr_id = attrs.id
                WHERE attr_type=%s AND attr_value=%s AND attr_source=%s'''
        args = (ident.attr_type, ident.attr_value, ident.attr_source)

        if study_id:
            stmt += ' AND study_id = %s'
            args = args + (study_id,)

        cursor.execute(stmt, args)

        res = cursor.fetchone()

        if res:
            return res[0], study_id

        if not create:
            return None, study_id

        uuid_val = uuid.uuid4()

        insert_stmt = '''INSERT INTO attrs
                    (id, study_id, attr_type, attr_value, attr_source)
                    VALUES (%s, %s, %s, %s, %s)'''

        cursor.execute(insert_stmt, (uuid_val, study_id, ident.attr_type, ident.attr_value, ident.attr_source))

        return uuid_val,study_id



    @staticmethod
    def delete_attrs(cursor, individual_id):

        cursor.execute('''SELECT attr_id FROM individual_attrs WHERE
                       individual_id = %s''', (individual_id,))

        attr_ids = []
        for (attr_id,) in cursor:
           attr_ids.append(attr_id)

        stmt = '''DELETE FROM individual_attrs WHERE individual_id = %s'''

        cursor.execute( stmt, (individual_id,))

        for attr_id in attr_ids:
            cursor.execute('''DELETE FROM attrs WHERE id = %s''', (attr_id,))


    @staticmethod
    def add_attrs(cursor, uuid_val, individual):

        studies = []
        study_attrs = {}

        try:
            if individual.attrs:
                for ident in individual.attrs:
                    attr_id, study_id = IndividualEdit.get_or_create_individual_attr_id(cursor, ident)

                    cursor.execute('INSERT INTO individual_attrs(individual_id, attr_id) VALUES (%s, %s)',
                                   (uuid_val, attr_id))

        except psycopg2.IntegrityError as err:
            raise DuplicateKeyException("Error inserting individual {}".format(individual)) from err


    @staticmethod
    def update_attr_study(cursor, individual_id, old_study_id, new_study_id):

        old_attrs = []

        stmt = '''SELECT DISTINCT attr_type, attr_value, attr_source, study_name FROM individual_attrs
        JOIN attrs a ON a.id = individual_attrs.attr_id
                    JOIN studies s ON s.id = a.study_id
                    WHERE individual_id = %s AND study_id = %s'''

        cursor.execute(stmt, (individual_id, old_study_id))

        for (attr_type, attr_value, attr_source, study_name) in cursor:
            old_attrs.append(Attr(attr_type=attr_type,
                                          attr_value=attr_value,
                                          attr_source=attr_source,
                                             study_name=study_name))

        new_attrs = []

        cursor.execute(stmt, (individual_id, new_study_id))

        for (attr_type, attr_value, attr_source, study_name) in cursor:
            new_attrs.append(Attr(attr_type=attr_type,
                                          attr_value=attr_value,
                                          attr_source=attr_source,
                                             study_name=study_name))

        for old_attr in old_attrs:
            attr_id, study_id = IndividualEdit.get_or_create_individual_attr_id(cursor, old_attr)
            cursor.execute('INSERT INTO individual_attrs(individual_id, attr_id) VALUES (%s, %s)',
                               (individual_id, attr_id))
            cursor.execute('UPDATE attrs SET study_id=%s WHERE id=%s',(new_study_id, attr_id))

    @staticmethod
    def check_for_duplicate(cursor, individual, individual_id):

        for ident in individual.attrs:
            (match, study) = IndividualEdit.get_or_create_individual_attr_id(cursor, ident,
                                                            create=False)
            if match:
                raise DuplicateKeyException("Error updating individual - duplicate with {}".format(ident))

        for ident in individual.attrs:
            count = 0
            for ident1 in individual.attrs:
                if ident == ident1:
                    count = count + 1
            if count > 1:
                raise DuplicateKeyException("Error updating individual - duplicate attrs {}".format(ident))

