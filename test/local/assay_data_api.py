import six

from openapi_server.models.assay_datum import AssayDatum  # noqa: E501
from openapi_server.models.assay_data import AssayData  # noqa: E501
from openapi_server import util

import logging

from backbone_server.controllers.assay_datum_controller import AssayDatumController

from local.base_local_api import BaseLocalApi


class LocalAssayDataApi(BaseLocalApi):

    def __init__(self, api_client, user, auths, method):

        super().__init__(api_client, user, auths, method)

        self.assay_datum_controller = AssayDatumController()

    def create_assay_datum(self, assay_datum):
        """
        create_assay_datum
        Create a assayDatum
        :param assay_datum:
        :type assay_datum: dict | bytes

        :rtype: assayDatum
        """

        (ret, retcode) = self.assay_datum_controller.create_assay_datum(assay_datum, self._user,
                                                                        self.assay_datum_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'AssayDatum')

    def delete_assay_datum(self, assay_datum_id):
        """
        deletes an assayDatum

        :param assay_datum_id: ID of assayDatum to fetch
        :type assay_datum_id: str

        :rtype: None
        """
        (ret, retcode) = self.assay_datum_controller.delete_assay_datum(assay_datum_id, user=self._user,
                                                                        auths=self.assay_datum_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode)

    def download_assay_datum(self, assay_datum_id):
        """
        fetches an assayDatum

        :param assay_datum_id: ID of assayDatum to fetch
        :type assay_datum_id: str

        :rtype: AssayDatum
        """
        (ret, retcode) = self.assay_datum_controller.download_assay_datum(assay_datum_id, self._user,
                                                                          self.assay_datum_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'AssayDatum')

    def download_assay_data(self, filter=None, start=None, count=None):
        """
        fetches an assayDatum

        :param assayDatumId: ID of assayDatum to fetch
        :type assayDatumId: str

        :rtype: AssayDatum
        """
        (ret, retcode) = self.assay_datum_controller.download_assay_data(filter, start,
                                                                         count, self._user,
                                                                         self.assay_datum_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'AssayData')

    def download_assay_data_by_attr(self, prop_name, prop_value, study_name=None):
        """
        fetches a assayDatum by property value

        :param prop_name: name of property to search
        :type prop_name: str
        :param prop_value: matching value of property to search
        :type prop_value: str

        :rtype: AssayData
        """
        (ret, retcode) = self.assay_datum_controller.download_assay_data_by_attr(prop_name, prop_value,
                                                                                 study_name,
                                                                                 self._user,
                                                                                 self.assay_datum_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'AssayData')

    def download_assay_data_by_os_attr(self, prop_name, prop_value, study_name=None):
        """
        fetches a assayDatum by property value

        :param prop_name: name of property to search
        :type prop_name: str
        :param prop_value: matching value of property to search
        :type prop_value: str

        :rtype: AssayData
        """
        (ret, retcode) = self.assay_datum_controller.download_assay_data_by_os_attr(prop_name, prop_value,
                                                                                    study_name,
                                                                                    self._user,
                                                                                    self.assay_datum_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'AssayData')

    def update_assay_datum(self, assay_datum_id, assay_datum):
        """
        updates an assayDatum

        :param assay_datum_id: ID of assayDatum to update
        :type assay_datum_id: str
        :param assay_datum:
        :type assay_datum: dict | bytes

        :rtype: AssayDatum
        """
        (ret, retcode) = self.assay_datum_controller.update_assay_datum(assay_datum_id,
                                                                        assay_datum, self._user,
                                                                        self.assay_datum_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'AssayDatum')
