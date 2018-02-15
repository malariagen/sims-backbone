DB_NAME=backbone_service
if [ "${1}" = "test" ]
then
    DB_NAME=backbone_test
fi
if [ "${1}" = "" ]
then
    echo "Must use an arg e.g. test"
    exit
fi
echo ${DB_NAME}
#Rebuilding an existing db as empty - not changing the structure
pg_dump ${DB_NAME} -s > /tmp/${DB_NAME}.psql
sudo -u postgres psql << +++EOF
DROP database ${DB_NAME};
CREATE DATABASE ${DB_NAME};
Alter DATABASE ${DB_NAME} OWNER TO ${USER};
ALTER DATABASE ${DB_NAME} SET search_path=public, ${DB_NAME}, contrib;
\connect ${DB_NAME};
\i /tmp/${DB_NAME}.psql;
\connect ${DB_NAME};
SELECT postgis_full_version();
\copy countries (English, French, alpha2, alpha3, numeric_code) FROM './country_codes.tsv' DELIMITER E'\t'  HEADER CSV;
\copy taxonomies (id, rank, name) FROM './taxa.tsv' DELIMITER E'\t'  HEADER CSV;
+++EOF
rm /tmp/${DB_NAME}.psql
