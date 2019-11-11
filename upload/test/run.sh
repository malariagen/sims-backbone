#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

set -o allexport
source ${DIR}/../../.envs/.local/.postgres
set +o allexport
export POSTGRES_HOST=localhost
export POSTGRES_DB=backbone_test
if [ "${TRAVIS}" != "true" ]
then
  export TOKEN_URL=https://www.malariagen.net/sso/oauth2.0/accessToken
else
    POSTGRES_USER=postgres
fi
export PYTHONPATH=${DIR}/..:${DIR}/../../python_client:${DIR}/../../server:${DIR}/../../server/bb_server
if [ ! -d client-env ]
then
    #Already in a virtualenv
    if [ "${TRAVIS}" != "true" ]
    then
        virtualenv client-env -p /usr/bin/python
        source client-env/bin/activate
        pip3 install -r ../../test/requirements.txt
        pip3 install -r ../requirements.txt
        pip3 install -r ../../python_client/requirements.txt
        pip3 install -r $(pwd)/../../server/backbone_server/REQUIREMENTS
    fi
fi
if [ "${TRAVIS}" != "true" ]
then
    source client-env/bin/activate
fi
if [ ! -z "${LOCAL_TEST}" ]
then
    if [ "${LOCAL_TEST}" -eq 1 ]
    then
        echo "export BB_NOAUTH=1"
    fi
fi
if [ "$1" = "one" ]
then
    python3 -m pytest -s -x -k $2
else
    python3 -m pytest -s -x --cov=.. --cov-report html -v
fi
