import logging
import uuid

from openapi_server.models.derivative_sample import DerivativeSample

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException

from backbone_server.controllers.base_controller import BaseController
from backbone_server.derivative_sample.edit import DerivativeSampleEdit
from backbone_server.derivative_sample.fetch import DerivativeSampleFetch


class DerivativeSamplePost():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def post(self, derivative_sample, studies):

        with self._connection:
            with self._connection.cursor() as cursor:

                if studies and derivative_sample.original_sample_id:
                    stmt = '''SELECT study_code FROM original_samples
                    LEFT JOIN studies ON studies.id = original_samples.study_id
                    WHERE original_samples.id = %s'''
                    cursor.execute(stmt, (derivative_sample.original_sample_id,))
                    for (study_code,) in cursor:
                        BaseController.has_study_permission(studies, study_code,
                                                            BaseController.UPDATE_PERMISSION)

                uuid_val = uuid.uuid4()

                stmt = '''INSERT INTO derivative_samples
                            (id, original_sample_id, dna_prep,
                            acc_date,
                            parent_derivative_sample_id)
                            VALUES (%s, %s, %s, %s, %s)'''
                args = (uuid_val, derivative_sample.original_sample_id,
                        derivative_sample.dna_prep,
                        derivative_sample.acc_date,
                        derivative_sample.parent_derivative_sample_id)

                try:
                    cursor.execute(stmt, args)

                    DerivativeSampleEdit.add_attrs(cursor, uuid_val, derivative_sample)

                except DuplicateKeyException as err:
                    raise err

                derivative_sample = DerivativeSampleFetch.fetch(cursor, uuid_val)

        return derivative_sample
