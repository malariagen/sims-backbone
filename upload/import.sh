#!/bin/bash

ENVIRON=$1

if [ -z ${ENVIRON} ]
    ENVIRON=dev
fi
test -f environment && source environment
test -f ${INPUT1_STAGING_DIR}/import/environment && source ${INPUT1_STAGING_DIR}/import/environment

OUTFILE=${OUTPUT1_STAGING_DIR}/import_$(date +%Y-%m-%d-%H%M%S).log
# Redirect stdout ( > ) into a named pipe ( >() ) running "tee"
exec &> >(tee -i ${OUTFILE})

ARCHIVE_DIR=${OUTPUT1_STAGING_DIR}/archive

shopt -s nullglob
for i in ${INPUT1_STAGING_DIR}/import/roma/*
do
    test -d ${ARCHIVE_DIR}/roma || mkdir -p ${ARCHIVE_DIR}/roma
    ROMA_LOG=${OUTPUT1_STAGING_DIR}/import_$(date +%Y-%m-%d-%H%M%S).log
    python3 upload_roma.py ${IMPORT_CONFIG} $i 2>&1 | tee -i ${ROMA_LOG}
    python3 upload_log.py ${CMIS_CONFIG} ${ENVIRON} ${ROMA_LOG}
    #INPUT_STAGING_DIR is a copy so changes aren't synced
    cp ${i} ${ARCHIVE_DIR}/roma/$(basename ${i}).$(date +%Y-%m-%d:%H:%M:%S)
    aws s3 rm "s3://malariagen-sims-import-dev/import/roma/$(basename ${i})"
done
python3 set_taxa.py ${IMPORT_CONFIG}
python3 set_studies.py ${IMPORT_CONFIG} ${CMIS_CONFIG}
#Could upload the overall log but just keeping in S3 and uploading individual logs instead
#Not uploading set_taxa and set_studies
#python3 upload_log.py ${CMIS_CONFIG} ${ENVIRON} ${OUTFILE}
