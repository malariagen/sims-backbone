
ENVIRON=$1
shift

if [ -z ${ENVIRON} ]
then
    echo "e.g. $0 dev"
    exit 1
fi

if [ ${ENVIRON} = "prod" ]
then
    echo "Configuring prod"
    DIR=production
    NAME=sims
elif [ ${ENVIRON} = "test" ]
then
    echo "Configuring test"
    DIR=test
    NAME=sims-test
elif [ ${ENVIRON} = "dev" ]
then
    echo "Configuring dev"
    DIR=dev
    NAME=sims-dev
elif [ ${ENVIRON} = "local" ]
then
    echo "Configuring local"
    DIR=local
    NAME=sims-local
    ANGULAR_ENV=microk8s
else
    echo "Environ must be one of prod, test, dev, local"
    exit 1
fi

# The production nginx build has the endpoints built in and therefore needs
# to be rebuilt for each environment
diff -q ../../client/sims-backbone/src/environments/environment.prod.ts ../../client/sims-backbone/src/environments/environment.prod.ts.${ANGULAR_ENV}
if [ $? -eq 1 ]
then
    cp ../../client/sims-backbone/src/environments/environment.prod.ts.${ANGULAR_ENV} ../../client/sims-backbone/src/environments/environment.prod.ts
    (cd ../..;docker-compose -f production.yml build)
    ./local_images.sh
fi

HELM=linux-amd64/helm
## prod deployments
if [ "$1" = "install" ]
then
    shift
${HELM} secrets install  --debug  --namespace sims-${ENVIRON}  ./sims -f sims/${DIR}/secrets.yaml -f sims/${DIR}/values.yaml --name ${NAME} $*
elif [ "$1" = "upgrade" ]
then
    shift
${HELM} secrets upgrade --namespace sims-${ENVIRON} ${NAME} ./sims -f sims/${DIR}/secrets.yaml -f sims/${DIR}/values.yaml $*
else
    echo "Must install or upgrade"
fi
