from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from swagger_server.models.location import Location
from swagger_server.models.identifier import Identifier

import mysql.connector
from mysql.connector import errorcode
import psycopg2

import logging
import uuid

class LocationEdit():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    @staticmethod
    def add_identifiers(cursor, uuid_val, location):

        try:
            if location.identifiers:
                for ident in location.identifiers:
                    study_id = None
                    if ident.study_name:
                        cursor.execute('''SELECT id FROM studies WHERE study_name = %s''',
                                       (ident.study_name,))
                        study = cursor.fetchone()
                        if study:
                            study_id = study[0]
                        else:
                            suuid = uuid.uuid4()
                            cursor.execute('''INSERT INTO studies (id, study_name) 
                                            VALUES (%s, %s)''', (suuid, ident.study_name))
                            study_id = suuid
                    stmt = '''INSERT INTO location_identifiers (location_id, study_id, identifier_type, identifier_value)
                    VALUES (%s, %s, %s, %s)'''
                    cursor.execute(stmt, (uuid_val, study_id, ident.identifier_type, ident.identifier_value))

        except mysql.connector.Error as err:
            cursor.close()
            if err.errno == errorcode.ER_DUP_ENTRY:
                raise DuplicateKeyException("Error inserting location {}".format(location)) from err
            else:
                self._logger.fatal(repr(error))
        except psycopg2.IntegrityError as err:
            cursor.close()
            raise DuplicateKeyException("Error inserting location {}".format(location)) from err


