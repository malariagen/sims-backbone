import os

MANIFEST_DB_COL_NOTE = "note"
MANIFEST_DB_COL_COLLECT_DATE = "collection_date"
MANIFEST_DB_COL_EXT_ID = "external_id"
MANIFEST_DB_COL_LOC_ID = "location_id"

DB_HEADER_TAGS = "tags"


#                 if 'file' in request.FILES:
#                     filetoupload = request.FILES['file']
#                     Document.objects.create_document(filetoupload, manifest, 'manifest')
#                     #newdoc = Document(manifest_id=manifest.id, type='manifest')
#                     #newdoc.docfile.save(filetoupload.name, filetoupload)
#                 if 'csv_file' in request.FILES:
#                     filetoupload = request.FILES['csv_file']
#                     Document.objects.create_document(filetoupload, manifest, 'csv_sample')
#


DIR_PATH = os.path.dirname(os.path.realpath(__file__))

DEFAULT_MANIFEST_CONFIG_INI = os.path.join(DIR_PATH, 'config', 'manifests',
                                           os.getenv("NAME_INSTANCE", "genre")+'_manifest_config.ini')

# CSV or Excel documents containing list of samples to upload
MANIFEST_DOC_TYPE_BULK_UPLOAD_SAMPLES = "csv_sample"
# Any useful documentation associated with the manifest, such as ethics agreements, etc.
MANIFEST_DOC_TYPE_INFO = "manifest"
