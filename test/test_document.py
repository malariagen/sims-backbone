
import uuid
import base64

import openapi_client
from openapi_client.rest import ApiException

from test_base import TestBase
from datetime import date
import urllib

import pytest

class TestDocument(TestBase):


    def create_document(self, api_factory, study_name, doc):

        api_instance = api_factory.DocumentApi()

        created = api_instance.create_document(study_name,
                                               doc_type=doc.doc_type,
                                               document=doc.doc_name,
                                               doc_version='',
                                               note='')
        return created
    """
    """
    def test_doc_create(self, api_factory):

        api_instance = api_factory.DocumentApi()

        try:

            doc = openapi_client.Document(None,
                                          doc_name='test.docx',
                                          doc_type='misc',
                                          study_name='9100-MD-UP')
            created = self.create_document(api_factory, doc.study_name, doc)
            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to create_document succeeded')

            fetched = api_instance.download_document(created.document_id)
            assert created == fetched, "create response != download response"
            fetched.document_id = None
            fetched.created_by = None
            fetched.version = None
            fetched.action_date = None
            if not api_factory.isLocal():
                doc.content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                doc.mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            assert doc == fetched, "upload != download response"

            # https://github.com/OpenAPITools/openapi-generator/issues/4847
            if not api_factory.isLocal():
                preload = False
                content = api_instance.download_document_content(created.document_id, _preload_content=preload)
                if preload:
                    downloaded_content = open(content, "rb").read()
                else:
                    downloaded_content = content.data
                data = open(doc.doc_name, "rb").read()
                assert downloaded_content == data
            api_instance.delete_document(created.document_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DocumentApi->create_document", error)


    """
    """
    def test_doc_delete(self, api_factory):

        api_instance = api_factory.DocumentApi()

        try:

            doc = openapi_client.Document(None,
                                          doc_name='test.docx',
                                          doc_type='misc',
                                          study_name='9101-MD-UP')
            created = self.create_document(api_factory, doc.study_name, doc)
            api_instance.delete_document(created.document_id)
            with pytest.raises(ApiException, status=404):
                fetched = api_instance.download_document(created.document_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DocumentApi->create_document", error)


    """
    """
    def test_doc_delete_missing(self, api_factory):

        api_instance = api_factory.DocumentApi()

        try:

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    api_instance.delete_document(str(uuid.uuid4()))
            else:
                with pytest.raises(ApiException, status=403):
                    api_instance.delete_document(str(uuid.uuid4()))

        except ApiException as error:
            self.check_api_exception(api_factory, "DocumentApi->delete_document", error)

    """
    """
    def test_doc_duplicate_key(self, api_factory):

        api_instance = api_factory.DocumentApi()

        try:

            doc = openapi_client.Document(None, doc_name='test.docx',
                                          doc_type='manifest', study_name='9102-MD-UP')
            created = self.create_document(api_factory, doc.study_name, doc)

            with pytest.raises(ApiException, status=422):
                created = self.create_document(api_factory, doc.study_name, doc)

            api_instance.delete_document(created.document_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DocumentApi->create_document", error)


    """
    """
    def test_doc_update(self, api_factory):

        api_instance = api_factory.DocumentApi()

        try:

            doc = openapi_client.Document(None, doc_name='test.docx',
                                          doc_type='misc',
                                          doc_version="1", study_name='9105-MD-UP',)
            created = self.create_document(api_factory, doc.study_name, doc)
            created.doc_version = "2"
            updated = api_instance.update_document(created.document_id,
                                                   version=created.version,
                                                   document='test1.docx',
                                                   doc_type=doc.doc_type,
                                                   doc_version="2")
            updated.updated_by = None
            assert updated.version > created.version
            created.version = updated.version
            created.doc_name = updated.doc_name
            assert updated.doc_name == 'test1.docx'
            assert updated == created, "update response != download response"
            updated_fetched = api_instance.download_document(created.document_id)
            updated_fetched.updated_by = None
            assert created == updated_fetched, "update != download response"
            # https://github.com/OpenAPITools/openapi-generator/issues/4847
            if not api_factory.isLocal():
                preload = False
                content = api_instance.download_document_content(created.document_id, _preload_content=preload)
                if preload:
                    downloaded_content = open(content, "rb").read()
                else:
                    downloaded_content = content.data
                data = open(updated.doc_name, "rb").read()
                assert downloaded_content == data
            api_instance.delete_document(created.document_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DocumentApi->create_document", error)

    """
    """
    def test_doc_update_metadata(self, api_factory):

        api_instance = api_factory.DocumentApi()

        try:

            doc = openapi_client.Document(None, doc_name='test.docx',
                                          doc_type='misc',
                                          doc_version="1", study_name='9105-MD-UP',)
            created = self.create_document(api_factory, doc.study_name, doc)
            created.doc_version = "2"
            updated = api_instance.update_document(created.document_id,
                                                   version=created.version,
                                                   doc_type=doc.doc_type,
                                                   doc_version="2")
            updated.updated_by = None
            assert updated.version > created.version
            created.version = updated.version
            assert updated == created, "update response != download response"
            updated_fetched = api_instance.download_document(created.document_id)
            updated_fetched.updated_by = None
            assert created == updated_fetched, "update != download response"
            api_instance.delete_document(created.document_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DocumentApi->create_document", error)

    """
    """
    def test_doc_update_duplicate(self, api_factory):

        api_instance = api_factory.DocumentApi()

        try:

            doc = openapi_client.Document(None,
                                          doc_name='test.docx',
                                          doc_type='misc',
                                          study_name='9106-MD-UP')
            created = self.create_document(api_factory, doc.study_name, doc)
            looked_up = api_instance.download_document(created.document_id)
            new_doc = openapi_client.Document(None,
                                              doc_name='test1.docx',
                                              doc_type='misc',
                                              study_name='0001-MD-UP')
            new_created = self.create_document(api_factory, doc.study_name, new_doc)
            new_doc.document_id = looked_up.document_id
            with pytest.raises(ApiException, status=422):
                updated = api_instance.update_document(looked_up.document_id,
                                                       version=looked_up.version,
                                                       doc_type='misc',
                                                       document='test1.docx')

            api_instance.delete_document(looked_up.document_id)
            api_instance.delete_document(new_created.document_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DocumentApi->create_document", error)

    """
    """
    def test_doc_update_missing(self, api_factory):

        api_instance = api_factory.DocumentApi()

        try:

            new_doc = openapi_client.Document(None,
                                              doc_name='test.docx',
                                              doc_type='misc',
                                              study_name='9107-MD-UP')
            fake_id = uuid.uuid4()
            new_doc.document_id = str(fake_id)


            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    updated = api_instance.update_document(new_doc.document_id,
                                                           version=1)
            else:
                with pytest.raises(ApiException, status=403):
                    updated = api_instance.update_document(new_doc.document_id,
                                                           version=1)

        except ApiException as error:
            self.check_api_exception(api_factory, "DocumentApi->update_document", error)


    """
    """
    def test_doc_study_lookup(self, api_factory):

        api_instance = api_factory.DocumentApi()

        try:
            study_code = '9120-MD-UP'

            doc = openapi_client.Document(None,
                                          doc_name='test.docx',
                                          doc_type='misc',
                                          study_name=study_code)

            created = self.create_document(api_factory, doc.study_name, doc)

            fetched = api_instance.download_documents_by_study(study_code)

            assert fetched.count == 1, "Study not found"

            assert created == fetched.documents[0], "create response != download response"

            # ffetched = api_instance.download_documents(search_filter='studyId:' + study_code)

            # assert ffetched.count == 1, "Study not found"

            # assert ffetched == fetched

            api_instance.delete_document(created.document_id)

            with pytest.raises(ApiException, status=404):
                fetched = api_instance.download_documents_by_study('asdfhjik')
        except ApiException as error:
            self.check_api_exception(api_factory, "DocumentApi->create_document", error)


    """
    """
    def test_doc_download_document_permission(self, api_factory):

        api_instance = api_factory.DocumentApi()

        try:
            if not api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=403):
                    api_instance.download_document(str(uuid.uuid4()))
        except ApiException as error:
            self.check_api_exception(api_factory, "DocumentApi->download_document", error)


    """
    """
    def test_doc_gets(self, api_factory):

        api_instance = api_factory.DocumentApi()

        try:

            old_study = '9139-MD-UP'
            new_study = '9140-MD-UP'

            doc = openapi_client.Document(None,
                                          doc_name='test.docx',
                                          doc_type='misc',
                                          study_name=old_study)
            doc1 = openapi_client.Document(None,
                                           doc_name='test1.docx',
                                           doc_type='misc',
                                           study_name=new_study)

            created = self.create_document(api_factory, doc.study_name, doc)
            created1 = self.create_document(api_factory, doc1.study_name, doc1)
            looked_up = api_instance.download_documents_by_study(old_study)

            assert looked_up.count == 1

            api_instance.delete_document(created.document_id)
            api_instance.delete_document(created1.document_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DocumentApi->create_document", error)
