

import logging

from flask import make_response

from openapi_server.models.document import Document  # noqa: E501
from backbone_server.controllers.base_controller import BaseController

from backbone_server.model.document import BaseDocument
from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.permission_exception import PermissionException

from backbone_server.controllers.decorators import apply_decorators


@apply_decorators
class DocumentController(BaseController):

    def create_document(self, study_code,
                        doc1,
                        document=None,
                        studies=None,
                        user=None, auths=None):  # noqa: E501
        """create_document

        Create a Document # noqa: E501

        :param study_code: 4 digit study code
        :type study_code: str
        :param doc_name:
        :type doc_name: str
        :param doc_type:
        :type doc_type: str
        :param document:
        :type document: werkzeug.FileStorage
        :param doc_version:
        :type doc_version: str
        :param note:
        :type note: str

        :rtype: Document
        """
        retcode = 201
        doc = None

        post = BaseDocument(self.get_engine(), self.get_session())
        doc1.doc_name = document.filename
        doc1.content_type = document.content_type
        doc1.mimetype = document.mimetype
        doc1.study_name = study_code

        try:
            doc = post.post(doc1, study_code, file_storage=document,
                            studies=studies, user=user)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug("create_document: %s", repr(dke))
            retcode = 422
            doc = str(dke)
        except PermissionException as dke:
            logging.getLogger(__name__).debug("create_document: %s", repr(dke))
            retcode = 403
            doc = str(dke)

        return doc, retcode

    def delete_document(self, document_id, studies=None, user=None, auths=None):  # noqa: E501
        """deletes an Document

         # noqa: E501

        :param document_id: ID of Document to fetch
        :type document_id: str

        :rtype: None
        """
        delete = BaseDocument(self.get_engine(), self.get_session())

        retcode = 200

        try:
            delete.delete(document_id, studies)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "delete_document: %s", repr(dme))
            retcode = 404
        except PermissionException as dke:
            logging.getLogger(__name__).debug("delete_document: %s", repr(dke))
            retcode = 403
            doc = str(dke)

        return None, retcode


    def download_document(self, document_id, studies=None, user=None, auths=None):  # noqa: E501
        """fetches an Document

         # noqa: E501

        :param document_id: ID of Document to fetch
        :type document_id: str

        :rtype: Document
        """
        get = BaseDocument(self.get_engine(), self.get_session())

        retcode = 200
        doc = None

        try:
            doc = get.get(document_id, studies)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "download_document: %s", repr(dme))
            retcode = 404
            doc = str(dme)
        except PermissionException as dke:
            logging.getLogger(__name__).debug("download_document: %s", repr(dke))
            retcode = 403
            doc = str(dke)

        return doc, retcode

    def download_document_content(self, document_id, studies=None, user=None, auths=None):  # noqa: E501
        """fetches an Document

         # noqa: E501

        :param document_id: ID of Document to fetch
        :type document_id: str

        :rtype: Document
        """
        get = BaseDocument(self.get_engine(), self.get_session())

        status = 200
        doc = None

        try:
            (doc, status, headers) = get.get_content(document_id, studies)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "download_document: %s", repr(dme))
            retcode = 404
            doc = str(dme)
        except PermissionException as dke:
            logging.getLogger(__name__).debug("download_document: %s", repr(dke))
            retcode = 403
            doc = str(dke)

        resp = doc
#        resp = make_response()
#        resp.data = doc
        resp.headers = headers
#        if 'content_type' in headers:
#            resp.content_type = headers['content_type']
#            del headers['content_type']
#        if 'mimetype' in headers:
#            resp.content_type = headers['mimetype']
#            del headers['mimetype']
#        resp.status = status
#

        return resp

    def download_documents_by_study(self, study_name, studies=None, user=None, auths=None):  # noqa: E501
        """fetches Documents for a study

         # noqa: E501

        :param study_name: 4 digit study code
        :type study_name: str

        :rtype: Documents
        """
        get = BaseDocument(self.get_engine(), self.get_session())

        retcode = 200
        doc = None

        try:
            start = None
            count = None
            doc = get.get_by_study(study_name, start=start,
                                   count=count, studies=studies)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "download_document: %s", repr(dme))
            retcode = 404
            doc = str(dme)
        except PermissionException as dke:
            logging.getLogger(__name__).debug("download_documents_by_study: %s", repr(dke))
            retcode = 403
            doc = str(dke)

        return doc, retcode


    def update_document(self, document_id,
                        doc1=None,
                        document=None,
                        studies=None,
                        user=None, auths=None):  # noqa: E501
        """updates an Document

         # noqa: E501

        :param document_id: ID of Document to update
        :type document_id: str
        :param document:
        :type document: dict | bytes

        :rtype: Document
        """
        retcode = 200
        doc = None

        try:
            put = BaseDocument(self.get_engine(), self.get_session())

            if document:
                doc1.doc_name = document.filename
                doc1.content_type = document.content_type
                doc1.mimetype = document.mimetype

            doc = put.put(document_id, doc1, None, file_storage=document,
                          studies=studies, user=user)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug(
                "update_document: %s", repr(dke))
            retcode = 422
            doc = str(dke)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "update_document: %s", repr(dme))
            retcode = 404
            doc = str(dme)
        except PermissionException as dke:
            logging.getLogger(__name__).debug("update_document: %s", repr(dke))
            retcode = 403
            doc = str(dke)

        return doc, retcode
