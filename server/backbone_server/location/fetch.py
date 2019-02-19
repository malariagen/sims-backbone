from openapi_server.models.location import Location
from openapi_server.models.attr import Attr
from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

class LocationFetch():


    @staticmethod
    def fetch(cursor, location_id):

        if not location_id:
            return None

        stmt = '''SELECT id, ST_X(location) as latitude, ST_Y(location) as longitude,
        accuracy, curated_name, curation_method, country, notes
                       FROM locations WHERE id = %s'''
        cursor.execute( stmt, (location_id,))

        location = None

        for (location_id, latitude, longitude, accuracy, curated_name,
             curation_method, country, notes) in cursor:
            location = Location(str(location_id), latitude, longitude, accuracy,
                                curated_name, curation_method, country, notes)

        stmt = '''SELECT DISTINCT attr_type, attr_value, attr_source, studies.study_name
                FROM location_attrs
                JOIN attrs a ON a.id = location_attrs.attr_id
                LEFT JOIN studies ON a.study_id = studies.id
                WHERE location_id = %s AND attr_type = %s'''

        cursor.execute(stmt, (location_id, 'partner_name'))

        if not location:
            raise MissingKeyException("No location {}".format(location_id))

        location.attrs = []
        for (name, value, source, study) in cursor:
            ident = Attr(attr_type = name, 
                               attr_value = value,
                               attr_source = source,
                               study_name = study)
            location.attrs.append(ident)

        if len(location.attrs) == 0:
            location.attrs = None

        return location
