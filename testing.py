import json
import boto3

# TODO implement

client = boto3.client('s3')

my_bucket = client.list_objects(Bucket='test-bucket-lambda-trigger-1')
print(my_bucket['Contents'])