import http
from aws_cdk import (
    # Duration,
    CfnOutput,
    Stack,
    aws_apigateway,
    aws_iam
    # aws_sqs as sqs,
)
from constructs import Construct

class ApiGateway(Stack):

    def __init__(self, scope: Construct, construct_id: str,iam_cloud_watch_role,lambda_sqs_checker_creator_name, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # API Gateway Resource
        api_gateway = aws_apigateway.RestApi(
            self,
            id="sdsds", 
            rest_api_name="hephaestus-apigateway",
            description="REST Api for Hephaestus Backend",
            default_cors_preflight_options=aws_apigateway.CorsOptions(
                allow_origins=aws_apigateway.Cors.ALL_ORIGINS,
                allow_methods=aws_apigateway.Cors.ALL_METHODS,
            ),
            cloud_watch_role=False
           
            )
        
        # Attach Cloud Watch Role
        aws_apigateway.CfnAccount(self, 
                                  "Set-Cloud-Watch-Role",
                                  cloud_watch_role_arn=iam_cloud_watch_role
                                  )
        
        
        api_gateway.root.add_resource("lambda_sqs").add_method(http_method="POST",integration=aws_apigateway.LambdaIntegration(lambda_sqs_checker_creator_name))
