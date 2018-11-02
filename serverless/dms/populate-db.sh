#https://aws.amazon.com/blogs/database/how-to-script-a-database-migration/
#sudo apt install jq
STAGE=dev
SRC_USERNAME=$(jq -r '.db_user' config.source.json)
SRC_PASSWORD=$(jq -r '.db_password' config.source.json)
SRC_SERVER=$(jq -r '.db_host' config.source.json)
SRC_PORT=5432
SRC_DB=$(jq -r '.database' config.source.json)
TGT_USERNAME=$(jq -r '.db_user' ../config.${STAGE}.json)
TGT_PASSWORD=$(jq -r '.db_password' ../config.${STAGE}.json)
TGT_SERVER=$(aws cloudformation list-exports | jq '.Exports[] | select(.Name == "sims-backbone-service:DbHost-dev") | .Value '| sed -e 's/"//g')
TGT_VPC=$(aws cloudformation list-exports | jq '.Exports[] | select(.Name == "sims-backbone-service:ServerlessVPC-dev") | .Value '| sed -e 's/"//g')
TGT_SG=$(aws cloudformation list-exports | jq '.Exports[] | select(.Name == "sims-backbone-service:ServerlessSecurityGroup-dev") | .Value '| sed -e 's/"//g')
TGT_SUBNETA=$(aws cloudformation list-exports | jq '.Exports[] | select(.Name == "sims-backbone-service:PublicSubnetA-dev") | .Value '| sed -e 's/"//g')
TGT_SUBNETB=$(aws cloudformation list-exports | jq '.Exports[] | select(.Name == "sims-backbone-service:PublicSubnetB-dev") | .Value '| sed -e 's/"//g')
TGT_SUBNETC=$(aws cloudformation list-exports | jq '.Exports[] | select(.Name == "sims-backbone-service:PublicSubnetC-dev") | .Value '| sed -e 's/"//g')
TGT_PORT=5432
TGT_DB=$(jq -r '.database' ../config.${STAGE}.json)


function get_endpoints {
    #For more advanced options for endpoint creation, see create-endpoint in the AWS CLI Command Reference.
    #Run the following commands to save the endpoint ARNs for use in later steps.
    source_endpoint_arn=$(aws dms describe-endpoints --filter="Name=endpoint-id,Values=source-endpoint " --query="Endpoints[0].EndpointArn")
    target_endpoint_arn=$(aws dms describe-endpoints --filter="Name=endpoint-id,Values=target-endpoint" --query="Endpoints[0].EndpointArn")
}

function get_rep_instance {
    #Run the following command to save the ReplicationInstanceArn for use in later steps.
    rep_instance_arn=$(aws dms describe-replication-instances --filter=Name=replication-instance-id,Values=dms-instance --query 'ReplicationInstances[0].ReplicationInstanceArn')
}

function setup {
    #Create a replication instance.
    #Use the following command to create a replication instance with the name dms-instance.
    aws dms create-replication-subnet-group --replication-subnet-group-identifier dms-subnet-group --replication-subnet-group-description "test" --subnet-ids ${TGT_SUBNETA} ${TGT_SUBNETB} ${TGT_SUBNETC}
    aws dms create-replication-instance --replication-instance-identifier dms-instance --replication-instance-class dms.t2.medium --allocated-storage 50 --vpc ${TGT_VPC} --vpc-security-group-ids ${TGT_SG} --replication-subnet-group-identifier dms-subnet-group
    #This command creates the replication instance on a t2.medium instance with 50 GB of allotted storage. It uses default values for other parameters. For more configuration options to use when creating a replication instance, see create-replication-instance in the AWS CLI Command Reference.
    #Describe the replication instance.
    #Run the following command to describe the replication instance. The response of this command will include the status of create-replication-instance. This will help you understand the status of the instance creation.
    aws dms describe-replication-instances --filter=Name=replication-instance-id,Values=dms-instance

    get_rep_instance
    #It will take a few minutes to create the replication instance. While that’s in progress, create the source and target endpoint objects.
    #Create the source and target endpoints.
    #Run the following command to create the source and target endpoints. Provide source and target database details like the engine-name, the hostname and port and the username and password.
    aws dms create-endpoint --endpoint-identifier source-endpoint --endpoint-type source --engine-name postgres --username ${SRC_USERNAME} --password ${SRC_PASSWORD} --server-name ${SRC_SERVER} --port ${SRC_PORT} --database-name=${SRC_DB}
    aws dms create-endpoint --endpoint-identifier target-endpoint --endpoint-type target --engine-name postgres --username ${TGT_USERNAME} --password ${TGT_PASSWORD} --server-name ${TGT_SERVER} --port ${TGT_PORT} --database-name=${TGT_DB}

    get_endpoints

    #Test source and target endpoints from the replication instance.
    #After the replication instance is active and the endpoints have been successfully created, test connectivity from the replication instance to these endpoints. The following commands will invoke connectivity tests from the replication instance to the database endpoints:
    aws dms test-connection --replication-instance-arn $rep_instance_arn --endpoint-arn $source_endpoint_arn
    aws dms test-connection --replication-instance-arn $rep_instance_arn --endpoint-arn $target_endpoint_arn
    #Describe connections to the source and target endpoints.

    #The describe-connections response will contain the status of the test connection and, in the case of a failed connection, the failure message. After invoking the connectivity test, describe the connections to ensure the tests are successful. If the test connection #fails for any reason, it must be fixed and retested.
    aws dms describe-connections --filter "Name=endpoint-arn,Values=$source_endpoint_arn,$target_endpoint_arn"
}

function do_replication {
    get_rep_instance
    get_endpoints

    #Note: A failure message in the describe response will provide details for the test connection failure.
    #Create a replication task.
    #If the test connections are successful, use the following command to create the task:
    aws dms create-replication-task --task-identifier replication-task-1 --source-endpoint-arn $source_endpoint_arn --target-endpoint-arn $target_endpoint_arn --replication-instance-arn $rep_instance_arn --migration-type full-load --table-mappings file:///./table-mappings --task-settings file:///./task-settings
    #Task creation will take a few minutes. After the task is created, describe the task and make sure it is ready to be executed.
    aws dms describe-replication-tasks --filters "Name=replication-task-id,Values=replication-task-1"
    #Run the following command to save the replication task ARN for use in later steps:
    replication_task_arn=$(aws dms describe-replication-tasks --filters "Name= replication-task-id,Values=replication-task-1" --query "ReplicationTasks[0].ReplicationTaskArn")
    #Run the following command if you want to just retrieve the status of the task:
    aws dms describe-replication-tasks --filters "Name=replication-task-arn,Values=$replication_task_arn" --query "ReplicationTasks[0].Status"
    #Start the replication task.
    #Run the following command to start the task after it is ready to be executed:
    aws dms start-replication-task --replication-task-arn $replication_task_arn --start-replication-task-type start-replication
    #For all available options for the start-replication-task command, see start-replication-task in the AWS CLI Command Reference.
    #Monitor the progress of the replication task.
    #After you start the task, it’s very important to monitor its progress. Run the following commands to keep track of the task progress.
    #To monitor the overall task-level statistics, run the following command:
    aws dms describe-replication-tasks --filters "Name=replication-task-arn,Values=$replication_task_arn" --query "ReplicationTasks[0].ReplicationTaskStats"
    #To monitor the table-level statistics, run the following command:
    aws dms describe-table-statistics --replication-task-arn $replication_task_arn
    #To monitor the task status itself, run the following command:
    aws dms describe-replication-tasks --filters "Name=replication-task-arn,Values=$replication_task_arn" --query "ReplicationTasks[0].{Status:Status,StopReason:StopReason}"
    #Stop the replication task.
    #You can stop the migration after data is completely migrated from source to target. Run the following command to stop the migration task:
    aws dms stop-replication-task --replication-task-arn $replication_task_arn
    #Delete the replication task.
    #If you don’t want to keep the task, run the following command to delete it:
    aws dms delete-replication-task --replication-task-arn $replication_task_arn
}

function clean_up {
    get_rep_instance
    get_endpoints

    #Delete the source and target endpoints.
    #If you no longer need the endpoints, run the following commands to delete them:
    aws dms delete-endpoint --endpoint-arn $source_endpoint_arn
    aws dms delete-endpoint --endpoint-arn $target_endpoint_arn
    #Delete the replication instance.
    #After your migration is complete, run the following command to delete the replication instance:
    aws dms delete-replication-instance --replication-instance-arn $rep_instance_arn
    aws dms delete-replication-subnet-group --replication-subnet-group-identifier dms-subnet-group
}

do_replication
