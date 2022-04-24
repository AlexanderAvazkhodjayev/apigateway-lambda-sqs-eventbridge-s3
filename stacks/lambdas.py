from aws_cdk import (
    Stack,
    aws_lambda,
    Duration,
    aws_lambda_destinations
)
from constructs import Construct

class Lambdas(Stack):

    def __init__(self, 
                 scope: Construct, 
                 construct_id: str,
                 lambda_container_name, lambda_container_execution_role,
                 lambda_sqs_checker_creator_name,
                 lambda_sqs_checker_creator_execution_role,
                 lambda_training_name,
                 lambda_training_name_execution_role,
                 actual_sqs, 
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        lambda_container = aws_lambda.Function(self, 
                            id = "lambda_container",
                            code=aws_lambda.Code.from_asset('./lambda/lambda_container'),
                            handler="lambda_container.handler",
                            runtime=aws_lambda.Runtime.PYTHON_3_9,
                            function_name =lambda_container_name,
                            timeout= Duration.seconds(30),
                            role= lambda_container_execution_role,
        )
        
        lambda_sqs_checker_creator_name = aws_lambda.Function(self, 
                            id = "lambda_sqs_checker_creator_name",
                            code=aws_lambda.Code.from_asset('./lambda/lambda_sqs_checker_creator_name'),
                            handler="lambda_sqs_checker.handler",
                            runtime=aws_lambda.Runtime.PYTHON_3_9,
                            function_name = lambda_sqs_checker_creator_name,
                            timeout= Duration.seconds(30),
                            role= lambda_sqs_checker_creator_execution_role,
                            # Destination wasn't working
                            # on_success= aws_lambda_destinations.SqsDestination(actual_sqs)
        )
        lambda_training = aws_lambda.Function(self, 
                            id = "lambda_training",
                            code=aws_lambda.Code.from_asset('./lambda/lambda_trainer'),
                            handler="lambda_trainer.handler",
                            runtime=aws_lambda.Runtime.PYTHON_3_9,
                            function_name = lambda_training_name,
                            timeout= Duration.seconds(30),
                            role= lambda_training_name_execution_role,
                           
        )
        
        
        self.lambda_container = lambda_container
        self.lambda_sqs_checker_creator_name = lambda_sqs_checker_creator_name
        self.lambda_training=lambda_training
