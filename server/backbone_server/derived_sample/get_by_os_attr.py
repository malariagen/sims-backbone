from swagger_server.models.derived_sample import DerivedSample
from swagger_server.models.derived_samples import DerivedSamples

from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.derived_sample.fetch import DerivedSampleFetch

import logging

class DerivedSampleGetByOsAttr():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    def get(self, attr_type, attr_value):

        with self._connection:
            with self._connection.cursor() as cursor:

                locations = {}

                stmt = '''SELECT DISTINCT ds.id FROM derived_samples ds
                JOIN original_sample_attrs osa ON osa.original_sample_id=ds.original_sample_id
                JOIN attrs ON attrs.id = osa.attr_id
                WHERE attr_type = %s AND attr_value = %s'''
                args = (attr_type, attr_value)

                cursor.execute(stmt, args)

                derived_samples = DerivedSamples(derived_samples=[], count=0)
                event_ids = []

                for derived_sample_id in cursor:
                    event_ids.append(derived_sample_id)

                for derived_sample_id in event_ids:
                    derived_sample = DerivedSampleFetch.fetch(cursor, derived_sample_id, locations)
                    derived_samples.derived_samples.append(derived_sample)
                    derived_samples.count = derived_samples.count + 1


                derived_samples.attr_types = [attr_type]

        #partner_name has a unique key
        if derived_samples.count == 0:
            raise MissingKeyException("DerivedSample not found {} {}".format(attr_type,
                                                                      attr_value))
#Allow for when partner ident is used in different studies
#        if derived_samples.count > 1:
#            raise MissingKeyException("Too many derived_samples not found {} {}".format(attr_type,
#                                                                      attr_value))

        return derived_samples
