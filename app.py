#!/usr/bin/env python3
import os
from dotenv import dotenv_values

import aws_cdk as cdk
from stacks.apigateway import ApiGateway
from stacks.iam import IAMRoles
from stacks.lambdas import Lambdas
from stacks.sqs import SQS
from stacks.s3 import S3
from stacks.lambda_event_sources import LambdaEventSources

props = dotenv_values(".env")

app = cdk.App()

s3_bucket_name = "test-bucket-lambda-trigger-1"
lambda_container_name = "lambda_container"
lambda_sqs_checker_creator_name = "lambda_sqs_checker_creator"
lambda_training_name = "lambda_training"

IAM = IAMRoles(
        app,
        construct_id="Hephaestus-IAM-Roles",
        env={'account':props["ACCOUNT_ID"], "region": props["REGION"]},
        stack_name="hephaestus-IAM-Roles",
        lambda_container_name=lambda_container_name,
        lambda_sqs_checker_creator_name=lambda_sqs_checker_creator_name,
        lambda_training_name=lambda_training_name,
        s3_bucket_name=s3_bucket_name
    )

S3_Bucket = S3(
        app,
        construct_id="Hephaestus-S3",
        env={'account':props["ACCOUNT_ID"], "region": props["REGION"]},
        stack_name="Hephaestus-S3",
        s3_bucket_name=s3_bucket_name
    )

sqs_data = SQS(
        app,
        construct_id="Hephaestus-SQS",
        env={'account':props["ACCOUNT_ID"], "region": props["REGION"]},
        stack_name="Hephaestus-SQS"
    )

actual_lambda = Lambdas(
        app,
        construct_id="Hephaestus-Lambda",
        env={'account':props["ACCOUNT_ID"], "region": props["REGION"]},
        stack_name="Hephaestus-Lambda",
        
        # IAM Execution Roles
        lambda_container_execution_role=IAM.lambda_container_execution_role,
        lambda_sqs_checker_creator_execution_role = IAM.lambda_sqs_checker_creator_execution_role,
        lambda_training_name_execution_role=IAM.lambda_training_name_execution_role,
        
        # Lambda Container Name
        lambda_container_name=lambda_container_name,
        lambda_sqs_checker_creator_name=lambda_sqs_checker_creator_name,
        lambda_training_name=lambda_training_name,
        #SQS Data
        actual_sqs=sqs_data.actual_sqs
    )

LambdaEventSources = LambdaEventSources(
        app,
        construct_id="LambdaEventSources",
        env={'account':props["ACCOUNT_ID"], "region": props["REGION"]},
        stack_name="LambdaEventSources",
        actual_sqs=sqs_data.actual_sqs,
        lambda_container=actual_lambda.lambda_container,
        lambda_training=actual_lambda.lambda_training
        
        
)

ApiGateway(
        app,
        construct_id="Hephaestus-ApiGateway",
        env={'account':props["ACCOUNT_ID"], "region": props["REGION"]},
        stack_name="hephaestus-apigateway",
        iam_cloud_watch_role=IAM.cloud_watch_role,
        lambda_sqs_checker_creator_name=actual_lambda.lambda_sqs_checker_creator_name
    )

app.synth()
