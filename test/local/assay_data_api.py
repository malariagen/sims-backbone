import six

from openapi_server.models.assay_datum import AssayDatum  # noqa: E501
from openapi_server.models.assay_data import AssayData  # noqa: E501
from openapi_server import util

import logging

from backbone_server.controllers.assay_datum_controller  import AssayDatumController

from local.base_local_api import BaseLocalApi

class LocalAssayDataApi(BaseLocalApi):

    def __init__(self, api_client, user, auths, method):

        super().__init__(api_client, user, auths, method)

        self.assay_datum_controller = AssayDatumController()

    def create_assay_datum(self, assayDatum):
        """
        create_assay_datum
        Create a assayDatum
        :param assayDatum: 
        :type assayDatum: dict | bytes

        :rtype: assayDatum
        """

        (ret, retcode) = self.assay_datum_controller.create_assay_datum(assayDatum, self._user,
                                                               self.auth_tokens())

        return self.create_response(ret, retcode, 'AssayDatum')

    def delete_assay_datum(self, assayDatumId):
        """
        deletes an assayDatum
        
        :param assayDatumId: ID of assayDatum to fetch
        :type assayDatumId: str

        :rtype: None
        """
        (ret, retcode) = self.assay_datum_controller.delete_assay_datum(assayDatumId, self._user,
                                                               self.auth_tokens())

        return self.create_response(ret, retcode)


    def download_assay_datum(self, assayDatumId):
        """
        fetches an assayDatum
        
        :param assayDatumId: ID of assayDatum to fetch
        :type assayDatumId: str

        :rtype: AssayDatum
        """
        (ret, retcode) = self.assay_datum_controller.download_assay_datum(assayDatumId, self._user,
                                                                 self.auth_tokens())

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
                                                                                 self.auth_tokens())

        return self.create_response(ret, retcode, 'AssayData')


    def download_assay_data_by_attr(self, propName, propValue, study_name=None):
        """
        fetches a assayDatum by property value
        
        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str

        :rtype: AssayData
        """
        (ret, retcode) = self.assay_datum_controller.download_assay_data_by_attr(propName, propValue,
                                                                                 study_name,
                                                                                 self._user,
                                                                                 self.auth_tokens())

        return self.create_response(ret, retcode, 'AssayData')

    def download_assay_data_by_os_attr(self, propName, propValue, study_name=None):
        """
        fetches a assayDatum by property value
        
        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str

        :rtype: AssayData
        """
        (ret, retcode) = self.assay_datum_controller.download_assay_data_by_os_attr(propName, propValue,
                                                                                    study_name,
                                                                                    self._user,
                                                                                    self.auth_tokens())

        return self.create_response(ret, retcode, 'AssayData')


    def update_assay_datum(self, assayDatumId, assayDatum):
        """
        updates an assayDatum
        
        :param assayDatumId: ID of assayDatum to update
        :type assayDatumId: str
        :param assayDatum: 
        :type assayDatum: dict | bytes

        :rtype: AssayDatum
        """
        (ret, retcode) = self.assay_datum_controller.update_assay_datum(assayDatumId,
                                                                              assayDatum, self._user,
                                                               self.auth_tokens())

        return self.create_response(ret, retcode, 'AssayDatum')

