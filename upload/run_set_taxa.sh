#!/bin/bash
export PYTHONPATH=$(pwd)/../python_client
if [ ! -d upload-env ]
then
    virtualenv upload-env -p /usr/bin/python3
    source upload-env/bin/activate
    pip3 install -r ../python_client/requirements.txt
    pip3 install -r requirements.txt
fi
source upload-env/bin/activate
export TOKEN_URL=https://sso-dev.cggh.org/sso/oauth2.0/accessToken
python3 set_taxa.py config_dev.json
