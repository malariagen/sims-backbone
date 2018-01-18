from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from swagger_server.models.location import Location
from swagger_server.models.identifier import Identifier

from backbone_server.sampling_event.edit import SamplingEventEdit

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
                        study_id = SamplingEventEdit.fetch_study_id(cursor, ident.study_name, True)
                    stmt = '''INSERT INTO location_identifiers 
                    (location_id, study_id, identifier_type, identifier_value, identifier_source)
                    VALUES (%s, %s, %s, %s, %s)'''
                    cursor.execute(stmt, (uuid_val, study_id, ident.identifier_type,
                                          ident.identifier_value, ident.identifier_source))

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DUP_ENTRY:
                raise DuplicateKeyException("Error inserting location {}".format(location)) from err
            else:
                self._logger.fatal(repr(error))
        except psycopg2.IntegrityError as err:
            print(err.pgcode)
            print(err.pgerror)
            raise DuplicateKeyException("Error inserting location {}".format(location)) from err


