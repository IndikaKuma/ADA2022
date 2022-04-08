import logging
import os

from message_puller import MessagePuller
from pub_sub_util import create_topic, create_subscription
from resources.order import Order, Orders

logging.basicConfig(level=logging.INFO)
orders = Orders()
order = Order()
project_id = os.environ['project_id']
create_topic(project=project_id, topic="inventory_status")
create_subscription(project=project_id, topic="inventory_status",
                    subscription="inventory_status_orderrecord_sub")
create_topic(project=project_id, topic="order_status")
MessagePuller(project=project_id, subscription="inventory_status_orderrecord_sub", orders=orders)
