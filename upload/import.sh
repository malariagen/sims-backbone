#!/bin/bash

test -f environment && source environment
test -f ${INPUT1_STAGING_DIR}/import/environment && source ${INPUT1_STAGING_DIR}/import/environment

# Redirect stdout ( > ) into a named pipe ( >() ) running "tee"
OUTFILE=${OUTPUT1_STAGING_DIR}/import_$(date +%Y-%m-%d:%H:%M:%S).log
#Doesn't seem to work when run as part of data pipeline so do more simply for each action
#exec &> >(tee -i ${OUTFILE})

ARCHIVE_DIR=${OUTPUT1_STAGING_DIR}/archive

shopt -s nullglob
for i in ${INPUT1_STAGING_DIR}/import/roma/*
do
    test -d ${ARCHIVE_DIR}/roma || mkdir -p ${ARCHIVE_DIR}/roma
    python3 upload_roma.py ${IMPORT_CONFIG} $i 2>&1 | tee -a ${OUTFILE}
    mv ${i} ${ARCHIVE_DIR}/roma/$(basename ${i}).$(date +%Y-%m-%d:%H:%M:%S)
done
python3 set_taxa.py ${IMPORT_CONFIG} 2>&1 | tee -a ${OUTFILE}
python3 set_studies.py ${IMPORT_CONFIG} ${CMIS_CONFIG} 2>&1 | tee -a ${OUTFILE}
