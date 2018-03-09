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
echo $*
python3 uploader.py $1 $2 $3 config_dev.json
