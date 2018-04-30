#!/bin/bash
set -e
if [ "${TRAVIS}" != "true" ]
then
  export TOKEN_URL=https://sso-dev.cggh.org/sso/oauth2.0/accessToken
fi
export PYTHONPATH=$(pwd)/..:$(pwd)/../../python_client:$(pwd)/../../server:$(pwd)/../../server/bb_server
if [ ! -d client-env ]
then
    #Already in a virtualenv
    if [ "${TRAVIS}" != "true" ]
    then
        virtualenv client-env -p /usr/bin/python
        source client-env/bin/activate
    fi
    pip3 install -r ../requirements.txt
    pip3 install -r ../../python_client/requirements.txt
    pip3 install -r $(pwd)/../../server/backbone_server/REQUIREMENTS
fi
if [ "${TRAVIS}" != "true" ]
then
    source client-env/bin/activate
fi
if [ "$1" = "one" ]
then
    python3 -m pytest -s -x -k $2
else
    python3 -m pytest -s -x
fi
