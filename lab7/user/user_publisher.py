import json
import logging

from google.cloud import pubsub_v1


def create_topic(project_id, topic_id):
    try:
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic_id)
        topic = publisher.create_topic(request={"name": topic_path})
        logging.info("Created topic: {}".format(topic.name))
    except Exception as ex:
        logging.info(ex)


def publish_message(project_id, topic_id, message):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    future = publisher.publish(topic_path, message)
    try:
        future.result()
    except Exception as ex:
        logging.info(ex)
    logging.info(f"Published messages to {topic_path}.")


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    create_topic("ada2020-305519", "order_req")
    data = {
        "product_type": "Phone",
        "quantity": 10,
        "unit_price": 232.00
    }
    data = json.dumps(data).encode("utf-8")
    publish_message("ada2020-305519", "order_req", data)
