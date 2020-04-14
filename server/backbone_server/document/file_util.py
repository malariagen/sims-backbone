import os
import sys
import io
import base64
import tempfile

from pathlib import Path
from flask import send_from_directory, send_file, Response

# from werkzeug import FileWrapper

class FileUtil(object):

    def get_document_path(self, document):

        version = document.version
        if version:
            version = str(document.version + 1)
        else:
            version = str(1)
        doc_root = os.getenv('FILE_STORAGE_ROOT', '.')
        path = os.path.join(doc_root, document.study.code, document.doc_type,
                            document.doc_name, version, document.doc_name)

        return path

    def save_file(self, document, file_storage):
        doc_file = self.get_document_path(document)
        # jif document.content:
        # j    decoded_string = base64.b64decode(document.content)
        path = Path(os.path.dirname(doc_file))
        path.mkdir(parents=True, exist_ok=True)
        # print(f'Saving to {doc_file}')
        # Also ensures that a new version of the document record is created
        # even if the attributes haven't changed
        document.file_reference = doc_file
        file_storage.save(doc_file)

    def get_content(self, document):

        #doc_file = self.get_document_path(document)
        doc_file = document.file_reference

        data = send_file(io.BytesIO(open(doc_file,'rb').read()),
                         as_attachment=True,
                         mimetype=document.mimetype,
                         attachment_filename=document.doc_name)
        # send_from_directory(os.path.dirname(doc_file), os.path.basename(doc_file))
        # wrapper = FileWrapper(open(doc_file, 'rb'))
        # data = Response(wrapper, mimetype=document.mimetype, direct_passthrough=True)
        # print(f'Getting from {doc_file}')
        return data, 200, {
            'content_type': document.content_type
        }

    def delete_file(self, document):

        #doc_file = self.get_document_path(document)
        doc_file = document.file_reference

        if os.path.exists(doc_file):
            os.remove(doc_file)
