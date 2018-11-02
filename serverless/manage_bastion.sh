KEYPAIR=ec2-keypair
IMAGE_ID=$(aws ec2 describe-images --owners 099720109477 --filters Name=root-device-type,Values=ebs Name=architecture,Values=x86_64 Name=name,Values='*ubuntu-bionic-18.04*' Name=virtualization-type,Values=hvm --query 'sort_by(Images, &Name)[-1].ImageId' | sed -e 's/"//g')

NAME_TAG="Backbone Bastion Dev"
VPC=$(aws cloudformation list-exports | jq '.Exports[] | select(.Name == "sims-backbone-service:ServerlessVPC-dev") | .Value '| sed -e 's/"//g')
SG_ID=$(aws cloudformation list-exports | jq '.Exports[] | select(.Name == "sims-backbone-service:ServerlessSecurityGroup-dev") | .Value '| sed -e 's/"//g')
SUBNETA=$(aws cloudformation list-exports | jq '.Exports[] | select(.Name == "sims-backbone-service:PublicSubnetA-dev") | .Value '| sed -e 's/"//g')
SUBNETB=$(aws cloudformation list-exports | jq '.Exports[] | select(.Name == "sims-backbone-service:PublicSubnetB-dev") | .Value '| sed -e 's/"//g')
SUBNETC=$(aws cloudformation list-exports | jq '.Exports[] | select(.Name == "sims-backbone-service:PublicSubnetC-dev") | .Value '| sed -e 's/"//g')

function create_host {
aws ec2 run-instances --image-id $IMAGE_ID \
    --count 1 --instance-type t2.micro \
    --key-name $KEYPAIR \
    --subnet-id ${SUBNETA} \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=${NAME_TAG}}]"
#    --security-group-ids $SG_ID \
}

function destroy_host {
INSTANCE_DETAIL=$(aws ec2 describe-instances --query 'Reservations[*].Instances[*].[Placement.AvailabilityZone, Tags[0].Value ,State.Name, InstanceId, PublicIpAddress]' --region eu-west-1 --filter "Name=tag:Name,Values=${NAME_TAG}" --output=json)
INSTANCE_ID=$(aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId]' --region eu-west-1 --filter "Name=tag:Name,Values=${NAME_TAG}" --output=text)

aws ec2 terminate-instances --instance-ids $INSTANCE_ID
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
elif [ $1 = "info" ]
then
    info
fi
