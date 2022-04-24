import json
import boto3



def handler(event, context):
    # TODO implement
    
    sqs_client = boto3.client("sqs", region_name="us-east-1")
    print(event)
    
    
    response = sqs_client.send_message(
        QueueUrl="https://sqs.us-east-1.amazonaws.com/139988404192/hephaestus-sqs",
        MessageBody=json.dumps(event)
    )
    print(response) 
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
