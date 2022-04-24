import json
import boto3

def handler(event, context):
    # TODO implement
    
    client = boto3.client('s3')
    s3 = client.resource('s3')
    my_bucket = s3.Bucket('test-bucket-lambda-trigger-1')
   

    for my_bucket_object in my_bucket.objects.all():
        print(my_bucket_object.key)
    
    return {
        'statusCode': 200,
        'body': json.dumps("worked")
    }
