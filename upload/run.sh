#!/bin/bash
export PYTHONPATH=$(pwd)/../python_client
if [ ! -d upload-env ]
then
    virtualenv upload-env -p /usr/bin/python3
    source upload-env/bin/activate
    pip3 install -r ../python_client/requirements.txt
fi
source upload-env/bin/activate
python3 uploader.py $1 $2 $3
