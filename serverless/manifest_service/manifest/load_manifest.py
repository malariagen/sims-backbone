# Load-Inventory Lambda function
#
# This function is triggered by an object being created in an Amazon S3 bucket.
# The file is downloaded and each line is inserted into a DynamoDB table.

import json, urllib, boto3, csv
import uuid
import os

# Connect to S3 and DynamoDB
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

# Connect to the DynamoDB tables
inventory_table = dynamodb.Table(os.getenv("DYNAMODB_TABLE"))

# This handler is executed every time the Lambda function is triggered
def load_manifest(event, context):

  # Show the incoming event in the debug log
    print("Event received by Lambda function: " + json.dumps(event, indent=2))

    # Get the bucket and object key from the Event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    # e.g. "key": "media/studies/1175/VMF00001/csv_sample/manifest-1175-S01.csv"
    folders = key.split('/')
    study = folders[2]
    manifest = folders[3]
    manifest_file = folders[5]
    local_filename = '/tmp/inventory.txt'

    # Download the file from S3 to the local filesystem
    try:
        s3.meta.client.download_file(bucket, key, local_filename)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

    print('About to open local file')
    # Read the Manifest CSV file
    with open(local_filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')

        print(' local file opened')
        # Read each row in the file
        for row in reader:

            row["study"] = study
            row["manifest"] = manifest
            row["manifest_file"] = manifest_file
            row["id"] = str(uuid.uuid4())

            # Remove any empty values
            new_item_data = {k:row[k] for k in row if row[k]}
          # Show the row in the debug log
            print(json.dumps(new_item_data))

            # NB assumes file is valid - should be checked before uploading
            # No deduplication if a file is uploaded twice
            # Everything is a string
            # No normalization of tag names
            try:
            # Insert row table
                inventory_table.put_item(Item=new_item_data)

            except Exception as e:
                print(e)
                print("Unable to insert data into DynamoDB table {}".format(e))

    # Finished!
    return "counts inserted"
