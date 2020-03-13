

import logging

from backbone_server.controllers.base_controller import BaseController

from backbone_server.model.document import BaseDocument
from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.permission_exception import PermissionException

from backbone_server.controllers.decorators import apply_decorators


@apply_decorators
class DocumentController(BaseController):

    def create_document(self, document, studies=None, user=None, auths=None):  # noqa: E501
        """create_document

        Create a Document # noqa: E501

        :param document:
        :type document: dict | bytes

        :rtype: Document
        """
        retcode = 201
        doc = None

        try:
            post = BaseDocument(self.get_engine(), self.get_session())

            doc = post.post(document, document.study_name, studies, user)
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

        retcode = 200
        doc = None

        try:
            doc = get.get_content(document_id, studies)
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


    def update_document(self, document_id, document, studies=None, user=None, auths=None):  # noqa: E501
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

            doc = put.put(document_id, document, document.study_name, studies,
                          user)
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

    def update_document_content(self, document_id, document, studies=None, user=None, auths=None):  # noqa: E501
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

            doc = put.put_content(document_id, document, studies)
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
