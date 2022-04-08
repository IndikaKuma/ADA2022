import logging
import os

from message_puller import MessagePuller
from pub_sub_util import create_subscription, create_topic
from resources.product import Product, Products

logging.basicConfig(level=logging.INFO)
product = Product()
products = Products()
project_id = os.environ['project_id']
create_topic(project=project_id, topic="order_req")
create_subscription(project=project_id, topic="order_req", subscription="order_req_sub")
create_topic(project=project_id, topic="inventory_status")
MessagePuller(project=project_id, subscription="order_req_sub", product=product)
