import connexion
import six

from openapi_server.models.document import Document  # noqa: E501
from openapi_server.models.documents import Documents  # noqa: E501
from openapi_server import util

import logging

from backbone_server.controllers.document_controller  import DocumentController

document_controller = DocumentController()

def create_document(study_code,
                    body=None,
                    document=None,
                    user=None, token_info=None):  # noqa: E501
    """create_document

    Create a Document # noqa: E501

    :param study_code: 4 digit study code
    :type study_code: str
    :param body:
    :type body: dict
    :param document:
    :type document: werzeug.FileStorage

    :rtype: Document
    """

    if body:
        doc = Document.from_dict(body)

    return document_controller.create_document(study_code, doc, document,
                                               studies=None,
                                               user=user,
                                               auths=document_controller.token_info(token_info))


def delete_document(document_id, user=None, token_info=None):  # noqa: E501
    """deletes an Document

     # noqa: E501

    :param document_id: ID of Document to fetch
    :type document_id: str

    :rtype: None
    """
    return document_controller.delete_document(document_id, studies=None,
                                               user=user,
                                               auths=document_controller.token_info(token_info))


def download_document(document_id, user=None, token_info=None):  # noqa: E501
    """fetches an Document

     # noqa: E501

    :param document_id: ID of Document to fetch
    :type document_id: str

    :rtype: Document
    """
    return document_controller.download_document(document_id, studies=None,
                                                 user=user,
                                                 auths=document_controller.token_info(token_info))

def download_document_content(document_id, user=None, token_info=None):  # noqa: E501
    """fetches an Document

     # noqa: E501

    :param document_id: ID of Document to fetch
    :type document_id: str

    :rtype: Document
    """
    return document_controller.download_document_content(document_id, studies=None,
                                                         user=user,
                                                         auths=document_controller.token_info(token_info))


def download_documents_by_study(study_name, user=None, token_info=None):  # noqa: E501
    """fetches Documents for a study

     # noqa: E501

    :param study_name: 4 digit study code
    :type study_name: str

    :rtype: Documents
    """
    return document_controller.download_documents_by_study(study_name, studies=None,
                                                           user=user,
                                                           auths=document_controller.token_info(token_info))


def update_document(document_id,
                    body=None,
                    document=None,
                    user=None,
                    token_info=None):  # noqa: E501
    """updates an Document

     # noqa: E501

    :param document_id: ID of Document to update
    :type document_id: str
    :param document:
    :type document: dict | bytes

    :rtype: Document
    """
    if body:
        doc = Document.from_dict(body)

    doc.document_id = document_id
    return document_controller.update_document(document_id, doc,
                                               document, studies=None,
                                               user=user,
                                               auths=document_controller.token_info(token_info))
