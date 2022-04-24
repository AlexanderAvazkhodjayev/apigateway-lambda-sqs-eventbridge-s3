from aws_cdk import (
    # Duration,
    CfnOutput,
    Stack,
    aws_iam
    # aws_sqs as sqs,
)
from constructs import Construct

class IAMRoles(Stack):

    def __init__(self, 
                 scope: Construct, 
                 construct_id: str,
                 lambda_container_name,
                 lambda_sqs_checker_creator_name, 
                 lambda_training_name,
                 s3_bucket_name,
                 **kwargs) -> None:
        
        super().__init__(scope, construct_id, **kwargs)
        
        cloud_watch_role = aws_iam.Role(
            self, 
            id="Cloud-Watch-Role",
            assumed_by=aws_iam.ServicePrincipal(service="apigateway.amazonaws.com"),
            description="This role will be used by the API_Gateway for Cloud Watch Permissions",
            role_name="hephaestus-cloud-watch-role",
            #permissions_boundary=
            inline_policies={"APIGatewayPushToCloudWatchLogs":
                aws_iam.PolicyDocument(
                    statements=[
                        aws_iam.PolicyStatement(
                            actions=[
                            "logs:CreateLogGroup",
                            "logs:CreateLogStream",
                            "logs:DescribeLogGroups",
                            "logs:DescribeLogStreams",
                            "logs:PutLogEvents",
                            "logs:GetLogEvents",
                            "logs:FilterLogEvents"],
                            resources=["*"]
                        )]
                )}
        )
        
        # Creating IAM role for lambda
        # Important Note: Don't forget to put accurate lambda name for policy statement below under following ID -- AWSBasicExecutionRoles -- !!!!
        lambda_container_execution_role = aws_iam.Role(
            self, 
            id="lambda_container_execution_role",
            assumed_by=aws_iam.ServicePrincipal(service="lambda.amazonaws.com"),
            description="This role will be used by the Lambda_Container for XXXX Permissions (SQS, CloudWatch, ETC...)",
            role_name="lambda_container_execution_role",
            #permissions_boundary=
            inline_policies={
                "AWSBasicExecutionRoles":
                    aws_iam.PolicyDocument(
                        statements=[
                            aws_iam.PolicyStatement(
                                actions=["logs:CreateLogGroup"],
                                resources=["arn:aws:logs:us-east-1:139988404192:*"]
                            ),
                            aws_iam.PolicyStatement(
                                actions=["logs:CreateLogStream","logs:PutLogEvents"],
                                resources=["arn:aws:logs:us-east-1:139988404192:log-group:/aws/lambda/"+lambda_container_name+":*"]
                            )
                        ]
                    ),
                "AWSLambdaSQSPollerExecutionRole":
                    aws_iam.PolicyDocument(
                        statements=[
                            aws_iam.PolicyStatement(
                                actions=["sqs:DeleteMessage","sqs:GetQueueAttributes","sqs:ReceiveMessage"],
                                resources=["arn:aws:sqs:*"]
                            )
                        ]
                    )
            }
        )
        
        lambda_sqs_checker_creator = aws_iam.Role(
            self, 
            id="lambda_sqs_checker_creator",
            assumed_by=aws_iam.ServicePrincipal(service="lambda.amazonaws.com"),
            description="This role will be used by the lambda_sqs_checker_creator for XXXX Permissions (SQS, CloudWatch, ETC...)",
            role_name="lambda_sqs_checker_creator",
            #permissions_boundary=
            inline_policies={
                "AWSBasicExecutionRoles":
                    aws_iam.PolicyDocument(
                        statements=[
                            aws_iam.PolicyStatement(
                                actions=["logs:CreateLogGroup"],
                                resources=["arn:aws:logs:us-east-1:139988404192:*"]
                            ),
                            aws_iam.PolicyStatement(
                                actions=["logs:CreateLogStream","logs:PutLogEvents"],
                                resources=["arn:aws:logs:us-east-1:139988404192:log-group:/aws/lambda/"+lambda_sqs_checker_creator_name+":*"]
                            )
                        ]
                    ),
                "AWSLambdaSQSPollerExecutionRole":
                    aws_iam.PolicyDocument(
                        statements=[
                            aws_iam.PolicyStatement(
                                actions=["sqs:SendMessage","sqs:GetQueueUrl"],
                                resources=["arn:aws:sqs:us-east-1:139988404192:*"]
                            )
                        ]
                    )
            }
        )
        
        lambda_training_name_execution_role = aws_iam.Role(
            self, 
            id="lambda_training_name",
            assumed_by=aws_iam.ServicePrincipal(service="lambda.amazonaws.com"),
            description="This role will be used by the lambda_training_name for XXXX Permissions (S3,CloudWatch, ETC...)",
            role_name="lambda_training_name",
            #permissions_boundary=
            inline_policies={
                "AWSBasicExecutionRoles":
                    aws_iam.PolicyDocument(
                        statements=[
                            aws_iam.PolicyStatement(
                                actions=["logs:CreateLogGroup"],
                                resources=["arn:aws:logs:us-east-1:139988404192:*"]
                            ),
                            aws_iam.PolicyStatement(
                                actions=["logs:CreateLogStream","logs:PutLogEvents"],
                                resources=["arn:aws:logs:us-east-1:139988404192:log-group:/aws/lambda/"+lambda_training_name+":*"]
                            ),
                            
                        ]
                    ),   
                "AWSS3BucketPerms":
                    aws_iam.PolicyDocument(
                        statements=[
                            aws_iam.PolicyStatement(
                                actions=["s3:PutObject","s3:GetObject","s3:DeleteObject","s3:ListObjects","s3:ListBucket"],
                                resources=["arn:aws:s3:::"+s3_bucket_name+"/*","arn:aws:s3:::"+s3_bucket_name]
                            )
                        ]
                    )
            }
        )
        
        self.cloud_watch_role = cloud_watch_role.role_arn
        self.lambda_container_execution_role = lambda_container_execution_role
        self.lambda_sqs_checker_creator_execution_role = lambda_sqs_checker_creator
        self.lambda_training_name_execution_role=lambda_training_name_execution_role
