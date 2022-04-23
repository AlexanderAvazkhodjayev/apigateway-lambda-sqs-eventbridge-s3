import aws_cdk as core
import aws_cdk.assertions as assertions

from apigateway_lambda_sqs_athena_cronjob_s3.apigateway_lambda_sqs_athena_cronjob_s3_stack import ApigatewayLambdaSqsAthenaCronjobS3Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in apigateway_lambda_sqs_athena_cronjob_s3/apigateway_lambda_sqs_athena_cronjob_s3_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ApigatewayLambdaSqsAthenaCronjobS3Stack(app, "apigateway-lambda-sqs-athena-cronjob-s3")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
