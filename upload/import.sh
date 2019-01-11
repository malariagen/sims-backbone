#!/bin/bash

test -f environment && source environment
test -f ${INPUT1_STAGING_DIR}/import/environment && source ${INPUT1_STAGING_DIR}/import/environment

OUTFILE=${OUTPUT1_STAGING_DIR}/import_$(date +%Y-%m-%d:%H:%M:%S).log
# Redirect stdout ( > ) into a named pipe ( >() ) running "tee"
exec &> >(tee -i ${OUTFILE})

ARCHIVE_DIR=${OUTPUT1_STAGING_DIR}/archive

shopt -s nullglob
for i in ${INPUT1_STAGING_DIR}/import/roma/*
do
    test -d ${ARCHIVE_DIR}/roma || mkdir -p ${ARCHIVE_DIR}/roma
    python3 upload_roma.py ${IMPORT_CONFIG} $i
    mv ${i} ${ARCHIVE_DIR}/roma/$(basename ${i}).$(date +%Y-%m-%d:%H:%M:%S)
done
python3 set_taxa.py ${IMPORT_CONFIG}
python3 set_studies.py ${IMPORT_CONFIG} ${CMIS_CONFIG}
if [ ${INPUT1_STAGING_DIR} = "s3://malariagen-sims-import-test/" ]
then
    ENVIRON=test
elif [ ${INPUT1_STAGING_DIR} = "s3://malariagen-sims-import-production/" ]
    ENVIRON=production
else
    ENVIRON=dev
fi
python3 upload_log.py ${CMIS_CONFIG} ${ENVIRON} ${OUTFILE}
