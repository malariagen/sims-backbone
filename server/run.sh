#TOKENINFO_URL=
VIRTUAL_ENV_HOME=.
if [ "$1" = "build" ]
then
    virtualenv server-env -p /usr/bin/python3
    (cd ..;./generate.sh server $2)
fi
if [ -f ${VIRTUAL_ENV_HOME}/server-env/bin/activate ]
then
    source ${VIRTUAL_ENV_HOME}/server-env/bin/activate
    if [ "$1" = "build" ]
    then
        pip3 install -r bb_server/requirements.txt
        pip3 install -r backbone_server/REQUIREMENTS
        shift
    fi
    cp -pr overlay/* bb_server
    export PYTHONPATH=$(pwd):$(pwd)/bb_server:${PYTHONPATH}
    if [ "$1" = "test" ]
    then
        POSTGRES_DB=backbone_test
        export POSTGRES_DB
        if [ "$2" = "rebuild" ]
        then
            (cd ../database;./rebuild.sh test)
        fi
    fi
    set -o allexport
    source ../.envs/.local/.postgres
    set +o allexport
    export POSTGRES_HOST=localhost
    cd bb_server
    grep security: ./openapi_server/openapi/openapi.yaml
    if [ $? -eq 1 ]
    then
        export BB_NOAUTH=1
    fi
    echo "http://localhost:8080/v1/ui/"
    python3 -m openapi_server
else
    echo "You need to run build first"
fi
