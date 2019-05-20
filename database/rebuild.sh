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
if [ "${2}" = "clean" ]
then
    TMP_REBUILD=0
    REBUILD_FILE=$(pwd)/backbone_service.psql
else
    TMP_REBUILD=1
    REBUILD_FILE=/tmp/backbone_service.psql
    pg_dump ${POSTGRES_NAME} -s > ${REBUILD_FILE}
fi
echo ${POSTGRES_NAME}
#Rebuilding an existing db as empty - not changing the structure
(cd /tmp;
sudo -u postgres psql << +++EOF
DROP database ${POSTGRES_NAME};
CREATE DATABASE ${POSTGRES_NAME};
Alter DATABASE ${POSTGRES_NAME} OWNER TO ${USER};
ALTER DATABASE ${POSTGRES_NAME} SET search_path=${POSTGRES_NAME}, public, contrib;
\c ${POSTGRES_NAME}
create extension postgis;
+++EOF
)
psql ${POSTGRES_NAME} << +++EOF
\i ${REBUILD_FILE};
\connect ${POSTGRES_NAME};
SELECT postgis_full_version();
\copy countries (English, French, alpha2, alpha3, numeric_code) FROM '../compose/local/postgres/initdb/country_codes.tsv' DELIMITER E'\t'  HEADER CSV;
\copy taxonomies (id, rank, name) FROM '../compose/local/postgres/initdb/taxa.tsv' DELIMITER E'\t'  HEADER CSV;
+++EOF
if [ ${TMP_REBUILD} -eq 1 ]
then
    rm ${REBUILD_FILE}
fi
