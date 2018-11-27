test -f environment && source environment
test -f ${INPUT1_STAGING_DIR}/import/environment && source ${INPUT1_STAGING_DIR}/import/environment
for i in ${INPUT1_STAGING_DIR}/import/roma/*
do
    python3 upload_roma.py ${IMPORT_CONFIG} $i && \
        mv ${i} ${INPUT1_STAGING_DIR}/archive/roma/$(basename ${i}).$(date +%Y-%m-%d:%H:%M:%S)
done
OUTPUT1_STAGING_DIR=/data/output
