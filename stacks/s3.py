from xml.dom.minidom import Document
from aws_cdk import (
    Stack,
    aws_sqs,
    aws_iam,
    aws_s3
)
from constructs import Construct

class S3(Stack):
    def __init__(self, scope: Construct, construct_id: str,s3_bucket_name, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        bucket_name = aws_s3.Bucket(self,id="Hephaestus-S3",bucket_name=s3_bucket_name)
        
        
        self.bucket_name = bucket_name

        
