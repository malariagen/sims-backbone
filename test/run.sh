#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

set -o allexport
source ${DIR}/../.envs/.local/.postgres
set +o allexport
export POSTGRES_HOST=localhost
export POSTGRES_DB=backbone_test
export TOKEN_URL=https://www.malariagen.net/sso/oauth2.0/accessToken
export PYTHONPATH=${DIR}/../python_client:${DIR}/../server:${DIR}/../server/bb_server
if [ ! -d client-env ]
then
    virtualenv client-env -p /usr/bin/python3
    source client-env/bin/activate
    pip3 install -r ${DIR}/../python_client/requirements.txt
    pip3 install -r ${DIR}/../upload/requirements.txt
    pip3 install -r ${DIR}/../server/backbone_server/REQUIREMENTS
    pip3 install -r ${DIR}/requirements.txt
fi
source client-env/bin/activate
grep security: ${DIR}/../server/bb_server/openapi_server/openapi/openapi.yaml
if [ $? -eq 1 ]
then
    export LOCAL_TEST=1
    echo "Server security not enabled therefore forcing local test"
fi
if [ "$1" = "one" ]
then
    python3 -m pytest --cov=backbone_server --cov-report html -v -s -x -k $2
    #Or -k to run a specific test instead of just failing fast
else
    python3 -m pytest -s -x --cov=backbone_server --cov-report html -v -v -v
fi
export PGPASSWORD="${PGPASSWORD:-$POSTGRES_PASSWORD}"
psql=( psql -v ON_ERROR_STOP=1 -h ${POSTGRES_HOST} --username "$POSTGRES_USER" --no-password )
psql+=( --dbname "$POSTGRES_DB" )
#Rebuilding an existing db as empty - not changing the structure
"${psql[@]}" << +++EOF
DELETE FROM taxonomies WHERE id=7227;
+++EOF
