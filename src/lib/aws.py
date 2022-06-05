import os
import logging
import boto3

log = logging.getLogger(__name__)


def send_message(content, **kwargs):
    """Queue up website restore into SQS"""
    messageAttributes = {}
    for key, value in kwargs.items():
        messageAttributes.update({key: {"DataType": "String", "StringValue": str(value)}})
    try:
        sqs = boto3.client("sqs", region_name=os.environ.get("SQS_REGION"))
        response = sqs.send_message(
            QueueUrl="https://sqs.%s.amazonaws.com/827114851303/%s" % (os.environ.get("SQS_REGION"), os.environ.get("SQS_NAME")),
            MessageAttributes=messageAttributes,
            MessageBody=content
        )
        return response
    except Exception as exception:
        log.error("Unable to queue message on: %s", exception)
        return None
