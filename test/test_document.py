


import uuid
import base64

import openapi_client
from openapi_client.rest import ApiException

from test_base import TestBase
from datetime import date
import urllib

import pytest

class TestDocument(TestBase):


    """
    """
    def test_doc_create(self, api_factory):

        api_instance = api_factory.DocumentApi()

        try:

            data = open("run.sh", "rb").read()
            encoded = base64.b64encode(data)
            doc = openapi_client.Document(None,
                                          doc_name='doc1',
                                          doc_type='misc',
                                          study_name='1100-MD-UP',
                                          content=encoded)
            created = api_instance.create_document(doc.study_name, doc)
            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to create_document succeeded')

            fetched = api_instance.download_document(created.document_id)
            assert created == fetched, "create response != download response"
            fetched.document_id = None
            fetched.created_by = None
            fetched.version = None
            doc.content = None
            assert doc == fetched, "upload != download response"

            content = api_instance.download_document_content(created.document_id)
            assert content == encoded
            api_instance.delete_document(created.document_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DocumentApi->create_document", error)


    """
    """
    def test_doc_delete(self, api_factory):

        api_instance = api_factory.DocumentApi()

        try:

            doc = openapi_client.Document(None,
                                          doc_name='doc1',
                                          doc_type='misc',
                                          study_name='1101-MD-UP')
            created = api_instance.create_document(doc.study_name, doc)
            api_instance.delete_document(created.document_id)
            with pytest.raises(ApiException, status=114):
                fetched = api_instance.download_document(created.document_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DocumentApi->create_document", error)


    """
    """
    def test_doc_delete_missing(self, api_factory):

        api_instance = api_factory.DocumentApi()

        try:

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=114):
                    api_instance.delete_document(str(uuid.uuid4()))
            else:
                with pytest.raises(ApiException, status=113):
                    api_instance.delete_document(str(uuid.uuid4()))

        except ApiException as error:
            self.check_api_exception(api_factory, "DocumentApi->delete_document", error)

    """
    """
    def test_doc_duplicate_key(self, api_factory):

        api_instance = api_factory.DocumentApi()

        try:

            doc = openapi_client.Document(None, doc_name='Test dup doc',
                                          doc_type='manifest', study_name='1102-MD-UP')
            created = api_instance.create_document(doc.study_name, doc)

            with pytest.raises(ApiException, status=422):
                created = api_instance.create_document(doc.study_name, doc)

            api_instance.delete_document(created.document_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DocumentApi->create_document", error)


    """
    """
    def test_doc_update(self, api_factory):

        api_instance = api_factory.DocumentApi()

        try:

            doc = openapi_client.Document(None, doc_name='My Test Doc',
                                          doc_type='misc',
                                          doc_version="1", study_name='1105-MD-UP',)
            created = api_instance.create_document(doc.study_name, doc)
            created.doc_version = "2"
            updated = api_instance.update_document(created.document_id,
                                                   created)
            updated.updated_by = None
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
                                          doc_name='test_doc_update_duplicate',
                                          doc_type='misc',
                                          study_name='1106-MD-UP')
            created = api_instance.create_document(doc.study_name, doc)
            looked_up = api_instance.download_document(created.document_id)
            new_doc = openapi_client.Document(None,
                                              doc_name='doc1',
                                              doc_type='misc',
                                              study_name='0001-MD-UP')
            new_created = api_instance.create_document(doc.study_name, new_doc)
            new_doc.document_id = looked_up.document_id
            with pytest.raises(ApiException, status=422):
                updated = api_instance.update_document(looked_up.document_id,
                                                       new_doc)

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
                                              doc_name='doc1',
                                              doc_type='misc',
                                              study_name='1107-MD-UP')
            fake_id = uuid.uuid4()
            new_doc.document_id = str(fake_id)


            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=114):
                    updated = api_instance.update_document(new_doc.document_id,
                                                           new_doc)
            else:
                with pytest.raises(ApiException, status=113):
                    updated = api_instance.update_document(new_doc.document_id,
                                                           new_doc)

        except ApiException as error:
            self.check_api_exception(api_factory, "DocumentApi->update_document", error)


    """
    """
    def test_doc_study_lookup(self, api_factory):

        api_instance = api_factory.DocumentApi()

        try:
            study_code = '1120-MD-UP'

            doc = openapi_client.Document(None,
                                          doc_name='doc1',
                                          doc_type='misc',
                                          study_name=study_code)

            created = api_instance.create_document(doc.study_name, doc)

            fetched = api_instance.download_documents_by_study(study_code)

            assert fetched.count == 1, "Study not found"

            assert created == fetched.documents[0], "create response != download response"

            # ffetched = api_instance.download_documents(search_filter='studyId:' + study_code)

            # assert ffetched.count == 1, "Study not found"

            # assert ffetched == fetched

            api_instance.delete_document(created.document_id)

            with pytest.raises(ApiException, status=114):
                fetched = api_instance.download_documents_by_study('asdfhjik')
        except ApiException as error:
            self.check_api_exception(api_factory, "DocumentApi->create_document", error)


    """
    """
    def test_doc_download_document_permission(self, api_factory):

        api_instance = api_factory.DocumentApi()

        try:
            if not api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=113):
                    api_instance.download_document(str(uuid.uuid4()))
        except ApiException as error:
            self.check_api_exception(api_factory, "DocumentApi->download_document", error)


    """
    """
    def test_doc_update_study(self, api_factory):

        api_instance = api_factory.DocumentApi()

        try:

            old_study = '1137-MD-UP'
            new_study = '1138-MD-UP'

            doc = openapi_client.Document(None,
                                          doc_name='doc1',
                                          doc_type='misc',
                                          study_name=old_study)

            created = api_instance.create_document(doc.study_name, doc)
            looked_up = api_instance.download_document(created.document_id)
            looked_up.study_name = new_study
            updated = api_instance.update_document(looked_up.document_id, looked_up)
            fetched = api_instance.download_document(looked_up.document_id)

            api_instance.delete_document(looked_up.document_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DocumentApi->create_document", error)

    """
    """
    def test_doc_gets(self, api_factory):

        api_instance = api_factory.DocumentApi()

        try:

            old_study = '1139-MD-UP'
            new_study = '1140-MD-UP'

            doc = openapi_client.Document(None,
                                          doc_name='doc1',
                                          doc_type='misc',
                                          study_name=old_study)
            doc1 = openapi_client.Document(None,
                                           doc_name='doc2',
                                           doc_type='misc',
                                           study_name=new_study)

            created = api_instance.create_document(doc.study_name, doc)
            created1 = api_instance.create_document(doc1.study_name, doc1)
            looked_up = api_instance.download_documents_by_study(old_study)

            assert looked_up.count == 1

            api_instance.delete_document(created.document_id)
            api_instance.delete_document(created1.document_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "DocumentApi->create_document", error)
