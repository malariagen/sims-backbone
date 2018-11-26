test -f environment && source environment
for i in ${INPUT1_STAGING_DIR}/import/roma/*
do
    python3 upload_roma.py ${IMPORT_CONFIG} $1 $2
    mv ${i} ${INPUT1_STAGING_DIR}/archive/roma/$(basename ${i}).$(date +%Y-%m-%d:%H:%M:%S)
done
OUTPUT1_STAGING_DIR=/data/output
