#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

set -o allexport
source ${DIR}/../../.envs/.local/.postgres
set +o allexport
export POSTGRES_HOST=localhost
if [ "${TRAVIS}" != "true" ]
then
  export TOKEN_URL=https://www.malariagen.net/sso/oauth2.0/accessToken
fi
export PYTHONPATH=${DIR}/..:${DIR}/../../python_client:${DIR}/../../server:${DIR}/../../server/bb_server
if [ ! -d client-env ]
then
    #Already in a virtualenv
    if [ "${TRAVIS}" != "true" ]
    then
        virtualenv client-env -p /usr/bin/python
        source client-env/bin/activate
    fi
    pip3 install -r ../../test/requirements.txt
    pip3 install -r ../requirements.txt
    pip3 install -r ../../python_client/requirements.txt
    pip3 install -r $(pwd)/../../server/backbone_server/REQUIREMENTS
fi
if [ "${TRAVIS}" != "true" ]
then
    source client-env/bin/activate
fi
if [ ! -z "${LOCAL_TEST}" ]
then
    if [ "${LOCAL_TEST}" -eq 1 ]
    then
        export BB_NOAUTH=1
    fi
fi
POSTGRES_DB=backbone_test
export POSTGRES_DB
if [ "$1" = "one" ]
then
    python3 -m pytest -s -x -k $2
else
    python3 -m pytest -s -x --cov=.. --cov-report html -v
fi
