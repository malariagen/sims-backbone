test -f environment && source environment
test -f ${INPUT1_STAGING_DIR}/import/environment && source ${INPUT1_STAGING_DIR}/import/environment

# Redirect stdout ( > ) into a named pipe ( >() ) running "tee"
OUTFILE=${OUTPUT1_STAGING_DIR}/import_$(date +%Y-%m-%d:%H:%M:%S).log
exec > >(tee -i ${OUTFILE})
exec 2>&1

shopt -s nullglob
for i in ${INPUT1_STAGING_DIR}/import/roma/*
do
    python3 upload_roma.py ${IMPORT_CONFIG} $i && \
        mv ${i} ${INPUT1_STAGING_DIR}/archive/roma/$(basename ${i}).$(date +%Y-%m-%d:%H:%M:%S)
done
python3 set_taxa.py ${IMPORT_CONFIG}
python3 set_studies.py ${IMPORT_CONFIG} ${CMIS_CONFIG}
