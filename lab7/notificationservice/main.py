import base64
import json
import logging
import os

from pub_sub_util import create_topic, publish_message


def receive_order_status(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
      Args:
           event (dict):  The dictionary with data specific to this type of
           event. The `data` field contains the PubsubMessage message. The
           `attributes` field will contain custom attributes if there are any.
           context (google.cloud.functions.Context): The Cloud Functions event
           metadata. The `event_id` field contains the Pub/Sub message ID. The
           `timestamp` field contains the publish time.
      """
    logging.basicConfig(level=logging.INFO)
    logging.info("""This Function was triggered by messageId {} published at {}
        """.format(context.event_id, context.timestamp))
    project_id = os.environ.get('PROJET_ID', 'Specified environment variable is not set.')
    data = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    event_type = event['attributes'].get("event_type")
    create_topic(project=project_id, topic="order_status_user")
    if event_type == "OrderCreated":
        order_id = data["id"]
        data = {
            "message": "The order was accepted. The order id is {}.".format(order_id)
        }
        data = json.dumps(data).encode("utf-8")
        publish_message(project=project_id, topic="order_status_user", message=data, event_type="OrderAccepted")
    else:
        data = {
            "message": "Sorry, we can not meet your order at the moment. Please try later."
        }
        data = json.dumps(data).encode("utf-8")
        publish_message(project=project_id, topic="order_status_user", message=data, event_type="OrderRejected")
