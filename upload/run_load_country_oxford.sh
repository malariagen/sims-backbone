#!/bin/bash
export PYTHONPATH=$(pwd)/../python_client:$(pwd)/../server:$(pwd)/../server/bb_server
if [ ! -d upload-env ]
then
    virtualenv upload-env -p /usr/bin/python3
    source upload-env/bin/activate
    pip3 install -r ../python_client/requirements.txt
    pip3 install -r requirements.txt
    pip3 install -r $(pwd)/../server/backbone_server/REQUIREMENTS
fi
source upload-env/bin/activate
export TOKEN_URL=https://sso-dev.cggh.org/sso/oauth2.0/accessToken
python3 set_country.py config_dev.json oxford_id $1 3 10 $2
