#!/bin/bash
set -f
if [ ! -d ../python_client ]
then
    echo "Please run (cd ..;./generate.sh) first"
    exit 1
fi
export PYTHONPATH=$(pwd)/../python_client
if [ ! -d example-env ]
then
    virtualenv example-env -p /usr/bin/python3
    if [ ! -d example-env ]
    then
        echo "Failed to create virtualenv based on /usr/bin/python3"
        exit 1
    fi
    source example-env/bin/activate
    pip3 install -r ../python_client/requirements.txt
    pip3 install -r requirements.txt
    pip3 install -r $(pwd)/../server/backbone_server/REQUIREMENTS
fi
source example-env/bin/activate
python3 fetch.py config.json "$@"
