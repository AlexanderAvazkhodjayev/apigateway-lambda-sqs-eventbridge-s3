from aws_cdk import (
    Stack,
    aws_lambda_event_sources,
    aws_lambda_destinations,
    aws_events_targets,
    aws_events

)
from constructs import Construct

class LambdaEventSources(Stack):
    def __init__(self, 
                 scope: Construct, 
                 construct_id: str,
                 actual_sqs,
                 lambda_container,
                 lambda_training, 
                 **kwargs) -> None:
        
        super().__init__(scope, construct_id, **kwargs)
        
        eventSource = aws_lambda_event_sources.SqsEventSource(actual_sqs)
        lambda_container.add_event_source(eventSource)
        
        #Event Bridge
        rule = aws_events.Rule(self, 
                               id="lambda_training_event_bridge",
                                rule_name="lambda_training_event_bridge",
                                schedule=aws_events.Schedule.cron(minute="0",hour="10",day="*",month="*",year="*"))
        
        rule.add_target(aws_events_targets.LambdaFunction(handler=lambda_training))
        
        
        
        
        
        
