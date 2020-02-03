import six

from openapi_server.models.document import Document  # noqa: E501
from openapi_server.models.documents import Documents  # noqa: E501
from openapi_server import util

import logging

from backbone_server.controllers.document_controller import DocumentController

from local.base_local_api import BaseLocalApi


class LocalDocumentApi(BaseLocalApi):

    def __init__(self, api_client, user, auths, method):

        super().__init__(api_client, user, auths, method)

        self.document_controller = DocumentController()

    def create_document(self, document, uuid_val=None,
                               studies=None):
        """
        create_document
        Create a document
        :param document:
        :type document: dict | bytes

        :rtype: Document
        """

        (ret, retcode) = self.document_controller.create_document(document,
                                                                  studies=studies,
                                                                  user=self._user,
                                                                  auths=self.document_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'Document')

    def delete_document(self, document_id, studies=None):
        """
        deletes an document_id

        :param document_id: ID of document to fetch
        :type document_id: str

        :rtype: None
        """
        (ret, retcode) = self.document_controller.delete_document(document_id,
                                                                  studies=studies,
                                                                  user=self._user,
                                                                  auths=self.document_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode)

    def download_document(self, document_id, studies=None):
        """
        fetches an document

        :param document_id: ID of document to fetch
        :type document_id: str

        :rtype: Document
        """
        (ret, retcode) = self.document_controller.download_document(document_id,
                                                                    studies=studies,
                                                                    user=self._user,
                                                                    auths=self.document_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'Document')

    def download_document_content(self, document_id, studies=None):
        """
        fetches an document

        :param document_id: ID of document to fetch
        :type document_id: str

        :rtype: Document
        """
        (ret, retcode) = self.document_controller.download_document_content(document_id,
                                                                    studies=studies,
                                                                    user=self._user,
                                                                    auths=self.document_controller.token_info(self.auth_tokens()))

        return ret

    def download_documents(self, search_filter=None, start=None,
                                  count=None, studies=None):
        """
        fetches an document

        :param documentId: ID of document to fetch
        :type documentId: str

        :rtype: Document
        """
        (ret, retcode) = self.document_controller.download_documents(search_filter, start,
                                                                     count,
                                                                     studies=studies,
                                                                     user=self._user,
                                                                     auths=self.document_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'Documents')

    def download_documents_by_study(self, study_name, studies=None):
        """
        fetches documents for a study

        :param study_name: 4 digit study code
        :type study_name: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: Documents
        """
        (ret, retcode) = self.document_controller.download_documents_by_study(study_name,
                                                                              studies=studies,
                                                                              user=self._user,
                                                                              auths=self.document_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'Documents')

    def update_document(self, document_id, document,
                               studies=None):
        """
        updates an document

        :param document_id: ID of document to update
        :type document_id: str
        :param document:
        :type document: dict | bytes

        :rtype: Document
        """
        (ret, retcode) = self.document_controller.update_document(document_id,
                                                                  document,
                                                                  studies=studies,
                                                                  user=self._user,
                                                                  auths=self.document_controller.token_info(self.auth_tokens()))

        return self.create_response(ret, retcode, 'Document')
