#!/bin/bash

ENVIRON=$1

if [ -z ${ENVIRON} ]
then
    ENVIRON=dev
fi
test -f environment && source environment
test -f ${INPUT1_STAGING_DIR}/import/environment && source ${INPUT1_STAGING_DIR}/import/environment

OUTFILE=${OUTPUT1_STAGING_DIR}/import_$(date +%Y-%m-%d-%H%M%S).log
# Redirect stdout ( > ) into a named pipe ( >() ) running "tee"
exec &> >(tee -i ${OUTFILE})

ARCHIVE_DIR=${OUTPUT1_STAGING_DIR}/archive

shopt -s nullglob
for i in import/oxford_11JAN2018.csv
do
    if [ -f $i.csv ]
    then
        INSTANCE=$(basename ${i} | awk -F_ '{print $1}')
        UPLOAD_LOG=${OUTPUT1_STAGING_DIR}/${INSTANCE}_$(date +%Y-%m-%d-%H%M%S).log
        python3 uploader.py $i.csv ${INSTANCE}.json ${IMPORT_CONFIG} 2>&1 | tee -i ${UPLOAD_LOG}
        if [ -s ${UPLOAD_LOG} ]
        then
            python3 upload_log.py ${CMIS_CONFIG} ${ENVIRON} ${UPLOAD_LOG}
        fi
        #INPUT_STAGING_DIR is a copy so changes aren't synced
        aws s3 mv "s3://malariagen-sims-import-${ENVIRON}/import/$(basename ${i})" "s3://malariagen-sims-import-${ENVIRON}/output/archive/"
    fi
done
SSR=2017_06_07_report_sample_status.xls
if [ -f import/${SSR} ]
then
    python3 upload_ssr.py ${IMPORT_CONFIG} import/${SSR}
    aws s3 mv "s3://malariagen-sims-import-${ENVIRON}/import/${SSR}" "s3://malariagen-sims-import-${ENVIRON}/output/archive/"
fi
for i in ${INPUT1_STAGING_DIR}/import/roma/*
do
    if [ $i != "_dummy" ]
    then
        test -d ${ARCHIVE_DIR}/roma || mkdir -p ${ARCHIVE_DIR}/roma
        INSTANCE=$(basename ${i} | awk -F_ '{print $1}')
        ROMA_LOG=${OUTPUT1_STAGING_DIR}/${INSTANCE}_$(date +%Y-%m-%d-%H%M%S).log
        python3 upload_roma.py ${IMPORT_CONFIG} $i 2>&1 | tee -i ${ROMA_LOG}
        if [ -s ${ROMA_LOG} ]
        then
            python3 upload_log.py ${CMIS_CONFIG} ${ENVIRON} ${ROMA_LOG}
        fi
        #INPUT_STAGING_DIR is a copy so changes aren't synced
        aws s3 mv "s3://malariagen-sims-import-${ENVIRON}/import/roma/$(basename ${i})" "s3://malariagen-sims-import-${ENVIRON}/output/archive/roma/$(basename ${i})"
    fi
done
for i in ${INPUT1_STAGING_DIR}/import/access/*.accdb
do
    if [ ${i} != "_dummy" ]
    then
        test -d ${ARCHIVE_DIR}/access || mkdir -p ${ARCHIVE_DIR}/access
        INSTANCE=$(basename ${i})
        ACCESS_LOG=${OUTPUT1_STAGING_DIR}/${INSTANCE}_$(date +%Y-%m-%d-%H%M%S).log
        JAR="lims-sims/target/lims-transform-1.0-SNAPSHOT.jar"
        if [ ! -f ${JAR} ]
        then
            (cd $(dirname ${JAR})/..;
            mvn package)
        fi
        java -jar ${JAR} net.malariagen.sims.lims.Transform ${i} ${i}.csv
        python3 uploader.py ${i}.csv access.json ${IMPORT_CONFIG} 2>&1 | tee -i ${ACCESS_LOG}
        # if [ -s ${ACCESS_LOG} ]
        # then
        #     python3 upload_log.py ${CMIS_CONFIG} ${ENVIRON} ${ACCESS_LOG}
        # fi
        test -d ${ARCHIVE_DIR}/access && mkdir ${ARCHIVE_DIR}/access
        aws s3 mv
        "s3://malariagen-sims-import-${ENVIRON}/import/access/$(basename ${i})" "s3://malariagen-sims-import-${ENVIRON}/output/archive/access/"
        mv $i ${ARCHIVE_DIR}/access/$(basename ${i})
    fi
done
for i in import/mlwh
do
    if [ -f $i.csv ]
    then
        INSTANCE=$(basename ${i} | awk -F_ '{print $1}')
        UPLOAD_LOG=${OUTPUT1_STAGING_DIR}/${INSTANCE}_$(date +%Y-%m-%d-%H%M%S).log
        python3 uploader.py $i.csv ${INSTANCE}.json ${IMPORT_CONFIG} 2>&1 | tee -i ${UPLOAD_LOG}
        if [ -s ${UPLOAD_LOG} ]
        then
            python3 upload_log.py ${CMIS_CONFIG} ${ENVIRON} ${UPLOAD_LOG}
        fi
        #INPUT_STAGING_DIR is a copy so changes aren't synced
        aws s3 mv "s3://malariagen-sims-import-${ENVIRON}/import/$(basename ${i})" "s3://malariagen-sims-import-${ENVIRON}/output/archive/"
    fi
done
METADATA_LOG=${OUTPUT1_STAGING_DIR}/metadata_$(date +%Y-%m-%d-%H%M%S).log
python3 set_taxa.py ${IMPORT_CONFIG} | tee -i ${METADATA_LOG}
python3 set_studies.py ${IMPORT_CONFIG} ${CMIS_CONFIG} | tee -i ${METADATA_LOG}
if [ -s ${METADATA_LOG} ]
then
    python3 upload_log.py ${CMIS_CONFIG} ${ENVIRON} ${METADATA_LOG}
fi
#Could upload the overall log but just keeping in S3 and uploading individual logs instead
#Not uploading set_taxa and set_studies
#python3 upload_log.py ${CMIS_CONFIG} ${ENVIRON} ${OUTFILE}
