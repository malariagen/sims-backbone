from swagger_server.models.sample import Sample
from swagger_server.models.location import Location
from swagger_server.models.identifier import Identifier
from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

class SampleGetById():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def __del__(self):
        if self._connection:
            self._connection.close()

    def get(self, sample_id):

        cursor = self._connection.cursor()

        stmt = '''SELECT samples.id, study_id, doc,
        locations.id as location_id, locations.partner_name, 
        ST_X(locations.location) as latitude, ST_Y(locations.location) as longitude, 
        locations.precision, locations.curated_name, locations.curation_method, locations.country,
        proxy_location.id as proxy_location_id, proxy_location.partner_name as proxy_partner_name,
        ST_X(proxy_location.location) as proxy_latitude,
        ST_Y(proxy_location.location) as proxy_longitude, 
        proxy_location.precision as proxy_precision, proxy_location.curated_name as proxy_curated_name, proxy_location.curation_method as proxy_curation_method, proxy_location.country
        FROM samples
        LEFT JOIN locations ON locations.id = samples.location_id
        LEFT JOIN locations as proxy_location ON proxy_location.id = samples.proxy_location_id
        WHERE samples.id = %s'''
        cursor.execute( stmt, (sample_id,))

        sample = None

        for (sample_id, study_id, doc,
             location_id, partner_name, latitude, longitude, precision, curated_name, curation_method, country,
             proxy_location_id, proxy_partner_name, proxy_latitude, proxy_longitude, proxy_precision, proxy_curated_name, proxy_curation_method, proxy_country
            ) in cursor:
            location = Location(location_id, partner_name, latitude, longitude, precision, curated_name, curation_method, country)
            proxy_location = Location(proxy_location_id, proxy_partner_name, proxy_latitude, proxy_longitude, proxy_precision, proxy_curated_name, proxy_curation_method, proxy_country)
            sample = Sample(sample_id, study_id, doc)
            sample.location_id = location_id
            sample.proxy_location_id = proxy_location_id
            sample.location = location
            sample.proxy_location = proxy_location

        if not sample:
            cursor.close()
            raise MissingKeyException("No sample {}".format(sample_id))

        stmt = '''SELECT identifier_type, identifier_value FROM identifiers WHERE sample_id = %s'''

        cursor.execute(stmt, (sample_id,))

        sample.identifiers = []
        for (name, value) in cursor:
            ident = Identifier(name, value)
            sample.identifiers.append(ident)

        if len(sample.identifiers) == 0:
            sample.identifiers = None

        cursor.close()

        return sample
