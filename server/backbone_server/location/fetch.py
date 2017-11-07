from swagger_server.models.location import Location
from swagger_server.models.identifier import Identifier
from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

class LocationFetch():


    @staticmethod
    def fetch(cursor, location_id):

        if not location_id:
            return None

        stmt = '''SELECT id, ST_X(location) as latitude, ST_Y(location) as longitude,
        precision, curated_name, curation_method, country, notes
                       FROM locations WHERE id = %s'''
        cursor.execute( stmt, (location_id,))

        location = None

        for (location_id, latitude, longitude, accuracy, curated_name,
             curation_method, country, notes) in cursor:
            location = Location(location_id, latitude, longitude, accuracy,
                                curated_name, curation_method, country, notes)

        stmt = '''SELECT DISTINCT identifier_type, identifier_value, studies.study_name 
                FROM location_identifiers 
                LEFT JOIN studies ON location_identifiers.study_id = studies.id
                WHERE location_id = %s AND location_identifiers.identifier_type = %s'''

        cursor.execute(stmt, (location_id, 'partner_name'))

        if not location:
            raise MissingKeyException("No location {}".format(location_id))

        location.identifiers = []
        for (name, value, study) in cursor:
            ident = Identifier(name, value, study)
            location.identifiers.append(ident)

        if len(location.identifiers) == 0:
            location.identifiers = None

        return location
