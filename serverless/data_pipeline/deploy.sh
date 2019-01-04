
if [ "$2" = "" ]
then
    STAGE=dev
else
    STAGE=$2
fi

BUCKET="s3://malariagen-sims-import-${STAGE}"

POSTGRES_HOST=$(aws cloudformation list-exports | jq ".Exports[] | select(.Name == \"sims-backbone-service:DbHost-${STAGE}\") | .Value "| sed -e 's/"//g')
POSTGRES_USER=$(jq -r '.db_user' ../config.${STAGE}.json)
POSTGRES_PASSWORD=$(jq -r '.db_password' ../config.${STAGE}.json)
POSTGRES_DB=$(jq -r '.database' ../config.${STAGE}.json)

sed -i.bak -r -e "s/^(POSTGRES_HOST=).*/\1${POSTGRES_HOST}/" \
    -e "s/^(POSTGRES_USER=).*/\1${POSTGRES_USER}/"  \
    -e "s/^(POSTGRES_PASSWORD=).*/\1${POSTGRES_PASSWORD}/"  \
    -e "s/^(POSTGRES_DB=).*/\1${POSTGRES_DB}/"  \
import/environment
aws s3 cp import/environment ${BUCKET}/import/
aws s3 cp import/config.json ${BUCKET}/import/
aws s3 cp ../../upload/setup.sh ${BUCKET}/import/
aws s3 cp ../../upload/cmis_config.json ${BUCKET}/import/
touch empty
aws s3 cp empty ${BUCKET}/output/
aws s3 cp empty ${BUCKET}/output/archive/
aws s3 cp empty ${BUCKET}/output/archive/roma/

mv import/environment.bak import/environment

SUBNETA=$(aws cloudformation list-exports | jq ".Exports[] | select(.Name == \"sims-backbone-service:PublicSubnetA-${STAGE}\") | .Value ")
SG_ID=$(aws cloudformation list-exports | jq ".Exports[] | select(.Name == \"sims-backbone-service:ServerlessSecurityGroup-${STAGE}\") | .Value ")
SNS_ARN=$(aws sns list-topics --query 'Topics[*].TopicArn' | grep "sims_import_notification")

#Two different ways of doing the same thing here
jq ".values.myS3InputLoc = \"${BUCKET}/\" | \
        .values.myS3OutputLoc = \"${BUCKET}/output/\" | \
        .objects |= map(if .id==\"Default\" then .pipelineLogUri = \"${BUCKET}/logs/\" else . end) | \
        .objects |= map(if .id==\"EC2ResourceObj\" then .subnetId = ${SUBNETA} else . end) | \
        .objects |= map(if .id==\"EC2ResourceObj\" then .securityGroupIds = ${SG_ID} else . end) | \
        .objects |= map(if .type==\"SnsAlarm\" then .topicArn = ${SNS_ARN} else . end) | \
        (.objects[] | select (.id == \"ShellCommandActivityObj\") | .scriptUri) |= \"${BUCKET}/import/setup.sh\" " definition.json > definition-${STAGE}.json


PIPELINE_NAME=SIMS-IMPORT-${STAGE}
PIPELINE_ID=$(aws datapipeline list-pipelines --query "pipelineIdList[?name=='${PIPELINE_NAME}'].id" --output=text)

#You can't change the schedule of a pipeline once it's been created so really all you can do is to
#delete it and recreated it
#https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-manage-pipeline-modify-console.html
if [ "${PIPELINE_ID}" != "" ]
then
    aws datapipeline get-pipeline-definition --pipeline-id ${PIPELINE_ID} > definition-backup-${STAGE}-$$.json
    diff -w definition-backup-${STAGE}-$$.json definition-${STAGE}.json
    aws datapipeline delete-pipeline --pipeline-id  ${PIPELINE_ID}
fi

PIPELINE_ID=$(aws datapipeline create-pipeline --tags key=Name,value="${PIPELINE_NAME}" --name ${PIPELINE_NAME} --unique-id $(uuidgen) --output=text)
aws datapipeline put-pipeline-definition --pipeline-id ${PIPELINE_ID} --pipeline-definition file://definition-${STAGE}.json

aws datapipeline activate-pipeline --pipeline-id  ${PIPELINE_ID}
