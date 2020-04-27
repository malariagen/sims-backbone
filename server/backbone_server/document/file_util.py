import os
import io
import shutil
import logging

from pathlib import Path
from flask import send_file

from backbone_server.errors.validation_only import ValidateOnlyPassException
# from werkzeug import FileWrapper

class FileUtil(object):

    def get_document_path(self, document):

        version = document.version
        if version:
            version = str(document.version + 1)
        else:
            version = str(1)
        doc_root = ''
        if not os.getenv('S3_DOCUMENT_BUCKET'):
            doc_root = os.getenv('FILE_STORAGE_ROOT', '.')
        path = os.path.join(doc_root, document.study.code, document.doc_type,
                            document.doc_name, version, document.doc_name)

        return path

    def validate_file(self, document, temp_file):
        print(f'Validating {temp_file} {document}')

    def save_file(self, document, file_storage, doc_content, validate_only):
        doc_file = self.get_document_path(document)
        # jif document.content:
        # j    decoded_string = base64.b64decode(document.content)
        # print(f'Saving to {doc_file}')
        # Also ensures that a new version of the document record is created
        # even if the attributes haven't changed
        document.file_reference = doc_file
        temp_file = os.path.join('/tmp', doc_file)
        path = Path(os.path.dirname(temp_file))
        path.mkdir(parents=True, exist_ok=True)
        if file_storage:
            file_storage.save(temp_file)
        elif doc_content:
            with open(temp_file, 'wb') as tf:
                tf.write(doc_content)
        else:
            bucket = os.getenv('S3_TEMP_BUCKET')
            if bucket:
                import boto3
                s3_client = boto3.client('s3')
                # Will need to be checked and processed by a lambda
                return s3_client.generate_presigned_post(bucket, doc_file)


        self.validate_file(document, temp_file)
        if validate_only:
            #By using an exception the document record won't be saved
            raise ValidateOnlyPassException('Validation passed')

        bucket = os.getenv('S3_DOCUMENT_BUCKET')
        # See also
        # For larger files it may be necessary to return a presigned_post
        if bucket:
            import boto3
            s3_client = boto3.client('s3')
            s3_client.upload_file(temp_file, bucket, doc_file)
            os.remove(temp_file)
        else:
            path = Path(os.path.dirname(doc_file))
            path.mkdir(parents=True, exist_ok=True)
            shutil.move(temp_file, doc_file)



    def get_content(self, document):

        #doc_file = self.get_document_path(document)
        doc_file = document.file_reference

        bucket = os.getenv('S3_DOCUMENT_BUCKET')
        headers = {
            'Content_Type': document.content_type
        }
        if bucket:
            import boto3
            from botocore.exceptions import ClientError

            s3_client = boto3.client('s3')
            try:
                response = s3_client.generate_presigned_url('get_object',
                                                            Params={
                                                                'Bucket': bucket,
                                                                'Key': doc_file
                                                            })
            except ClientError as e:
                logging.error(e)
                return None

            headers['Location'] = response
            return '', 302, headers
        else:
            data = send_file(io.BytesIO(open(doc_file, 'rb').read()),
                             as_attachment=True,
                             mimetype=document.mimetype,
                             attachment_filename=document.doc_name)
            # send_from_directory(os.path.dirname(doc_file), os.path.basename(doc_file))
            # wrapper = FileWrapper(open(doc_file, 'rb'))
            # data = Response(wrapper, mimetype=document.mimetype, direct_passthrough=True)
            # print(f'Getting from {doc_file}')
            return data, 200, headers

    def delete_file(self, document):

        #doc_file = self.get_document_path(document)
        doc_file = document.file_reference

        bucket = os.getenv('S3_DOCUMENT_BUCKET')
        if bucket:
            import boto3
            s3_client = boto3.client('s3')
            s3_client.delete_object(bucket, doc_file)
        else:
            if os.path.exists(doc_file):
                os.remove(doc_file)
