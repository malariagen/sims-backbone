#!/bin/bash
export TOKEN_URL=https://sso-dev.cggh.org/sso/oauth2.0/accessToken
export PYTHONPATH=$(pwd)/..:$(pwd)/../../python_client
if [ ! -d client-env ]
then
    virtualenv client-env -p /usr/bin/python3
    source client-env/bin/activate
    pip3 install -r ../requirements.txt
    pip3 install -r ../../python_client/requirements.txt

fi
source client-env/bin/activate
if [ "$1" = "one" ]
then
    python3 -m unittest test_sampling_event.TestSampling_Event.test_multiple_study
else
    python3 all_tests.py
fi
