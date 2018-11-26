#!/bin/bash
export TOKEN_URL=https://sso3.malariagen.net/sso/oauth2.0/accessToken
export PYTHONPATH=$(pwd)/../python_client:$(pwd)/../server:$(pwd)/../server/bb_server
if [ ! -d client-env ]
then
    virtualenv client-env -p /usr/bin/python3
    source client-env/bin/activate
    pip3 install -r ../python_client/requirements.txt
    pip3 install -r ../upload/requirements.txt
    pip3 install -r $(pwd)/../server/backbone_server/REQUIREMENTS
    pip3 install -r requirements.txt
fi
source client-env/bin/activate
export POSTGRES_DB=backbone_test
grep security: ../server/bb_server/swagger_server/swagger/swagger.yaml
if [ $? -eq 1 ]
then
    export LOCAL_TEST=1
    echo "Server security not enabled therefore forcing local test"
fi
if [ "$1" = "one" ]
then
    python3 -m pytest --cov=backbone_server --cov-report html -v -s -x -k $2
    #Or -k to run a specific test instead of just failing fast
else
    python3 -m pytest -s -x --cov=backbone_server --cov-report html -v
fi
psql -c "DELETE FROM taxonomies WHERE id=7227;" backbone_test
