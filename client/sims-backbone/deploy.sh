if [ "$1" = "" ]
then
    BUILD_ENV=dev
    STAGE=dev
else
    BUILD_ENV=$1
    STAGE=$1
fi
API=$(aws cloudformation list-exports | jq ".Exports[] | select(.Name == \"sims-backbone-service:ApiGatewayRestApi-${STAGE}\") | .Value "| sed -e 's/"//g')
REGION=$(aws configure get region)
ENDPOINT="https://${API}.execute-api.${REGION}.amazonaws.com/${STAGE}/sims-backbone-service/v1"
echo ${ENDPOINT}
S3_BUCKET="sims-backbone-${STAGE}"
URL="http://${S3_BUCKET}.s3-website-${REGION}.amazonaws.com/"
sed -i -e "s#\(apiLocation: '\)\(.*\)'#\1${ENDPOINT}\'#"  -e "s#\(redirectUri: '\)\(.*\)'#\1${URL}\'#" src/environments/environment.${BUILD_ENV}.ts


echo Build started on `date`
ng build -c ${BUILD_ENV}

if [ $? -ne 0 ]
then
    echo "Build failed"
    exit 1
fi
aws s3 website s3://${S3_BUCKET} --index-document index.html --error-document index.html
aws s3 sync --acl public-read --delete dist s3://${S3_BUCKET}
aws s3api put-bucket-website --bucket ${S3_BUCKET} --website-configuration file://./s3_routes.json
aws s3api put-bucket-policy --bucket 'sims-backbone-dev' --policy file://./policy.sims-backbone-dev.json
echo Build completed on `date`

echo "URL is ${URL}"
