import logging
import psycopg2

from openapi_server.models.derivative_sample import DerivativeSample

from backbone_server.controllers.base_controller import BaseController
from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.derivative_sample.edit import DerivativeSampleEdit
from backbone_server.derivative_sample.fetch import DerivativeSampleFetch



class DerivativeSamplePut():

    def __init__(self, conn, cursor=None):
        self._logger = logging.getLogger(__name__)
        self._connection = conn
        self._cursor = cursor


    def put(self, derivative_sample_id, derivative_sample, studies):

        with self._connection:
            with self._connection.cursor() as cursor:
                return self.run_command(cursor, derivative_sample_id,
                                        derivative_sample, studies)

    def run_command(self, cursor, derivative_sample_id, derivative_sample,
                    studies):

        stmt = '''SELECT id FROM derivative_samples WHERE id = %s'''
        cursor.execute(stmt, (derivative_sample_id,))

        existing_derivative_sample = None

        for (deriv_sample_id,) in cursor:
            existing_derivative_sample = DerivativeSample(deriv_sample_id)

        if not existing_derivative_sample:
            raise MissingKeyException("Could not find derivative_sample to update {}".format(derivative_sample_id))

        if studies:
            stmt = '''SELECT study_code FROM derivative_samples
            LEFT JOIN original_samples ON derivative_samples.original_sample_id = original_samples.id
            LEFT JOIN studies ON studies.id = original_samples.study_id
            WHERE derivative_samples.id = %s'''
            cursor.execute(stmt, (derivative_sample_id,))
            for (study_code,) in cursor:
                BaseController.has_study_permission(studies, study_code,
                                                    BaseController.UPDATE_PERMISSION)

        stmt = '''UPDATE derivative_samples
                    SET original_sample_id = %s,
                    dna_prep = %s,
                    acc_date = %s,
                    parent_derivative_sample_id = %s
                    WHERE id = %s'''
        args = (derivative_sample.original_sample_id,
                derivative_sample.dna_prep,
                derivative_sample.acc_date,
                derivative_sample.parent_derivative_sample_id,
                derivative_sample_id)

        try:
            cursor.execute(stmt, args)
            rc = cursor.rowcount

            cursor.execute('DELETE FROM derivative_sample_attrs WHERE derivative_sample_id = %s',
                           (derivative_sample_id,))

            DerivativeSampleEdit.add_attrs(cursor, derivative_sample_id, derivative_sample)

        except psycopg2.IntegrityError as err:
            raise DuplicateKeyException("Error updating derivative_sample {}".format(derivative_sample)) from err
        except DuplicateKeyException as err:
            raise err

        derivative_sample = DerivativeSampleFetch.fetch(cursor, derivative_sample_id)

        if rc != 1:
            raise MissingKeyException("Error updating derivative_sample {}".format(derivative_sample_id))


        return derivative_sample
