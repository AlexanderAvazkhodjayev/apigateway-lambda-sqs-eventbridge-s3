from xml.dom.minidom import Document
from aws_cdk import (
    Stack,
    aws_sqs,
    aws_iam
)
from constructs import Construct

class SQS(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        queue_name="hephaestus-sqs"
        
        actual_sqs = aws_sqs.Queue(self,id="hephaestus-sqs",queue_name=queue_name)
     
        actual_sqs.add_to_resource_policy(
                                        aws_iam.PolicyStatement(
                                            principals=[aws_iam.AccountPrincipal(account_id="139988404192")],
                                            actions=["SQS:*"],
                                            resources=["arn:aws:sqs:us-east-1:139988404192:"+queue_name]
                                        )   
                                    )
        
        self.actual_sqs = actual_sqs

        
