import os
import sys
import base64
import tempfile

from pathlib import Path
# from flask import send_from_directory

class FileUtil(object):


    def get_document_path(self, document):

        path = os.path.join(document.study_name[:4], document.doc_type,
                            document.doc_name)

        return path

    def save_file(self, document):
        doc_file = self.get_document_path(document)
        if document.content:
            decoded_string = base64.b64decode(document.content)
            path = Path(os.path.dirname(doc_file))
            path.mkdir(parents=True, exist_ok=True)
            with open(doc_file, mode="wb") as doc_file_handle:
                doc_file_handle.write(decoded_string)


    def update_file(self, document):
        doc_file = self.get_document_path(document)
        if document.content:
            decoded_string = base64.b64decode(document.content)
            with open(doc_file, mode="wb") as doc_file_handle:
                doc_file_handle.write(decoded_string)

    def get_content(self, document):

        doc_file = self.get_document_path(document)

        # send_from_directory(os.path.dirname(doc_file), os.path.basename(doc_file))
        with open(doc_file, mode="rb") as doc_file_handle:
            data = doc_file_handle.read()
            return base64.b64encode(data)

    def delete_file(self, document):

        doc_file = self.get_document_path(document)


        if document.content:
            decoded_string = base64.b64decode(document.content)
            with tempfile.TemporaryFile(mode="wb") as tmp_file:
                tmp_file.write(decoded_string)
