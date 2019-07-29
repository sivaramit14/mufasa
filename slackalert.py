import json
import logging
import os
from urllib2 import Request, urlopen, URLError, HTTPError
# Read environment variables
SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']
SLACK_USER = os.environ['SLACK_USER']
logger = logging.getLogger()
logger.setLevel(logging.INFO)
def lambda_handler(event, context):
    logger.info("Event: " + str(event))
    # Read message posted on SNS Topic
    raw_message = event['Records'][0]['Sns']['Message']
    jsonObj = json.loads(raw_message)
    pipelineName = jsonObj["approval"]["pipelineName"]
    reviewURL = jsonObj["approval"]["approvalReviewLink"]
    expiryTime = jsonObj["approval"]["expires"]
    custom_message = "Codepipeline " + pipelineName + " is awaiting your approval. \r\n Pipeline review URL: "+ reviewURL +" \r\n Expiry Time : " + expiryTime
    #message = json.loads(event['Records'][0]['Sns']['Message'])
    logger.info("Message: " + str(custom_message))
# Construct a slack message
    slack_message = {
        'channel': SLACK_CHANNEL,
        'username': SLACK_USER,
        'text': "%s" % (custom_message)
    }
# Post message on SLACK_WEBHOOK_URL
    req = Request(SLACK_WEBHOOK_URL, json.dumps(slack_message))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)
