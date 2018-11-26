POSTGRES_NAME=backbone_service
if [ "${1}" = "test" ]
then
    POSTGRES_NAME=backbone_test
fi
if [ "${1}" = "" ]
then
    echo "Must use an arg e.g. test"
    exit
fi
echo ${POSTGRES_NAME}
#Rebuilding an existing db as empty - not changing the structure
pg_dump ${POSTGRES_NAME} -s > /tmp/${POSTGRES_NAME}.psql
sudo -u postgres psql << +++EOF
DROP database ${POSTGRES_NAME};
CREATE DATABASE ${POSTGRES_NAME};
Alter DATABASE ${POSTGRES_NAME} OWNER TO ${USER};
ALTER DATABASE ${POSTGRES_NAME} SET search_path=public, ${POSTGRES_NAME}, contrib;
\connect ${POSTGRES_NAME};
\i /tmp/${POSTGRES_NAME}.psql;
\connect ${POSTGRES_NAME};
SELECT postgis_full_version();
\copy countries (English, French, alpha2, alpha3, numeric_code) FROM './country_codes.tsv' DELIMITER E'\t'  HEADER CSV;
\copy taxonomies (id, rank, name) FROM './taxa.tsv' DELIMITER E'\t'  HEADER CSV;
+++EOF
rm /tmp/${POSTGRES_NAME}.psql
