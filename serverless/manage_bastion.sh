KEYPAIR=ec2-keypair
IMAGE_ID=$(aws ec2 describe-images --owners 099720109477 --filters Name=root-device-type,Values=ebs Name=architecture,Values=x86_64 Name=name,Values='*ubuntu-bionic-18.04*' Name=virtualization-type,Values=hvm --query 'sort_by(Images, &Name)[-1].ImageId' | sed -e 's/"//g')

NAME_TAG="Backbone Bastion Dev"
VPC=$(aws cloudformation list-exports | jq '.Exports[] | select(.Name == "sims-backbone-service:ServerlessVPC-dev") | .Value '| sed -e 's/"//g')
SUBNETA=$(aws cloudformation list-exports | jq '.Exports[] | select(.Name == "sims-backbone-service:PublicSubnetA-dev") | .Value '| sed -e 's/"//g')
SUBNETB=$(aws cloudformation list-exports | jq '.Exports[] | select(.Name == "sims-backbone-service:PublicSubnetB-dev") | .Value '| sed -e 's/"//g')
SUBNETC=$(aws cloudformation list-exports | jq '.Exports[] | select(.Name == "sims-backbone-service:PublicSubnetC-dev") | .Value '| sed -e 's/"//g')
SG_NAME="BastionSecurityGroup"

function create_host {

    aws ec2 create-security-group --group-name ${SG_NAME} --description "${NAME_TAG} SG" --vpc-id ${VPC}
    get_params
    aws ec2 authorize-security-group-ingress --group-id ${SG_ID} --protocol tcp --port 22 --cidr 0.0.0.0/0
aws ec2 run-instances --image-id $IMAGE_ID \
    --count 1 --instance-type t2.nano \
    --key-name $KEYPAIR \
    --subnet-id ${SUBNETA} \
    --security-group-ids $SG_ID \
    --user-data file://./init.sh \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=${NAME_TAG}}]"

}

function get_params {

    SG_ID=$( aws ec2 describe-security-groups --query 'SecurityGroups[*].GroupId' --filter "Name=group-name,Values=${SG_NAME} " --output text)
INSTANCE_DETAIL=$(aws ec2 describe-instances --query 'Reservations[*].Instances[*].[Placement.AvailabilityZone, Tags[0].Value ,State.Name, InstanceId, PublicIpAddress]' --region eu-west-1 --filter "Name=tag:Name,Values=${NAME_TAG}" --output=json)
INSTANCE_ID=$(aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId]' --region eu-west-1 --filter "Name=tag:Name,Values=${NAME_TAG}" 'Name=instance-state-name,Values=running' --output=text)
INSTANCE_IP=$(aws ec2 describe-instances --query 'Reservations[*].Instances[*].[PublicIpAddress]' --region eu-west-1 --filter "Name=tag:Name,Values=${NAME_TAG}" --output=text)
}
function destroy_host {
get_params
set -x
echo "Commands not run"
aws ec2 terminate-instances --instance-ids $INSTANCE_ID --dry-run
echo "Need to wait for instance to terminate"
aws ec2 delete-security-group --group-id  ${SG_ID} --dry-run
}

function info {
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[Placement.AvailabilityZone, Tags[0].Value ,State.Name, InstanceId, PublicIpAddress]' --region eu-west-1 --filter "Name=tag:Name,Values=${NAME_TAG}" --output=json
}
if [ $1 = "start" ]
then
    create_host
elif [ $1 = "stop" ]
then
    destroy_host
elif [ $1 = "ssh" ]
then
    get_params
    ssh -i ~/.ssh/id_ec2  ubuntu@${INSTANCE_IP}
elif [ $1 = "tunnel" ]
then
    get_params
    DB_HOST=$(aws cloudformation list-exports | jq '.Exports[] | select(.Name == "sims-backbone-service:DbHost-dev") | .Value '| sed -e 's/"//g')
    STAGE="dev"
    TGT_USERNAME=$(jq -r '.db_user' config.${STAGE}.json)
    TGT_PASSWORD=$(jq -r '.db_password' config.${STAGE}.json)
    TGT_DB=$(jq -r '.database' config.${STAGE}.json)
    set -x
    ssh -i ~/.ssh/id_ec2 -L 3333:${DB_HOST}:5432 -N ubuntu@${INSTANCE_IP} &
    echo "psql -h localhost -p 3333 ${TGT_DB} ${TGT_USERNAME}"
    echo ${TGT_PASSWORD}
elif [ $1 = "info" ]
then
    info
fi
