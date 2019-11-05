DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

set -o allexport
source ${DIR}/../.envs/.local/.postgres
set +o allexport
export POSTGRES_HOST=localhost
if [ "${TRAVIS}" == "true" ]
then
    export POSTGRES_USER=postgres
fi
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
# Argueably should be running everything using docker exec but not doing
# that
REBUILD_PREFIX=/docker-entrypoint-initdb.d/
REBUILD_PREFIX=${DIR}/../compose/production/postgres/initdb/
if [ "${2}" = "clean" ]
then
    TMP_REBUILD=0
    REBUILD_FILE=${REBUILD_PREFIX}/02_backbone_service.sql
else
    TMP_REBUILD=1
    REBUILD_FILE=/tmp/backbone_service.psql
    pg_dump ${POSTGRES_NAME} -s > ${REBUILD_FILE}
#    docker cp ${REBUILD_FILE} sims-backbone_backbone_server_1:${REBUILD_FILE}
fi
echo ${POSTGRES_NAME}
# From https://github.com/docker-library/postgres/blob/master/10/docker-entrypoint.sh
export PGPASSWORD="${PGPASSWORD:-$POSTGRES_PASSWORD}"
dropdb -h ${POSTGRES_HOST} --username "$POSTGRES_USER" ${POSTGRES_NAME}
createdb -h ${POSTGRES_HOST} --username "$POSTGRES_USER" ${POSTGRES_NAME}
psql=( psql -v ON_ERROR_STOP=1 -h ${POSTGRES_HOST} --username "$POSTGRES_USER" --no-password )
psql+=( --dbname "$POSTGRES_NAME" )
#Rebuilding an existing db as empty - not changing the structure
"${psql[@]}" << +++EOF
ALTER DATABASE ${POSTGRES_NAME} SET search_path=${POSTGRES_NAME}, public, contrib;
create extension postgis;
+++EOF
"${psql[@]}" << +++EOF
\i ${REBUILD_FILE};
\connect ${POSTGRES_NAME};
SELECT postgis_full_version();
\copy countries (English, French, alpha2, alpha3, numeric_code) FROM '${REBUILD_PREFIX}/country_codes.tsv' DELIMITER E'\t'  HEADER CSV;
\copy taxonomies (id, rank, name) FROM '${REBUILD_PREFIX}/taxa.tsv' DELIMITER E'\t'  HEADER CSV;
+++EOF
if [ ${TMP_REBUILD} -eq 1 ]
then
    rm ${REBUILD_FILE}
fi
unset PGPASSWORD
