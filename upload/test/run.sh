#!/bin/bash
set -e
if [ "${TRAVIS}" != "true" ]
then
  export TOKEN_URL=https://sso-dev.cggh.org/sso/oauth2.0/accessToken
fi
export PYTHONPATH=$(pwd)/..:$(pwd)/../../python_client:$(pwd)/../../server:$(pwd)/../../server/bb_server
if [ ! -d client-env ]
then
    virtualenv client-env -p /usr/bin/python3.5
    source client-env/bin/activate
    pip3 install -r ../requirements.txt
    pip3 install -r ../../python_client/requirements.txt
    pip3 install -r $(pwd)/../../server/backbone_server/REQUIREMENTS
fi
source client-env/bin/activate
if [ "$1" = "one" ]
then
    python3 -m unittest test_sampling_event.TestSampling_Event.test_multiple_study
else
    python3 all_tests.py
fi
