#!/bin/bash
set -f
export PYTHONPATH=$(pwd)/../python_client
if [ ! -d example-env ]
then
    virtualenv example-env -p /usr/bin/python3
    source example-env/bin/activate
    pip3 install -r ../python_client/requirements.txt
    pip3 install -r requirements.txt
    pip3 install -r $(pwd)/../server/backbone_server/REQUIREMENTS
fi
source example-env/bin/activate
export TOKEN_URL=https://sso3.malariagen.net/sso/oauth2.0/accessToken
export REMOTE_HOST_URL=http://localhost:8080/v1
python3 fetch.py config.json "$@"
