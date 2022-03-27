import logging

from google.cloud import pubsub_v1


# Code is based on the following examples from Google. Please check them for more information.
# https://github.com/googleapis/python-pubsub/blob/master/samples/snippets/publisher.py
# https://github.com/googleapis/python-pubsub/blob/master/samples/snippets/subscriber.py

def create_topic(project, topic):
    try:
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project, topic)
        topic = publisher.create_topic(request={"name": topic_path})
        print("Created topic: {}".format(topic.name))  # instead, can check if there is a topic already, and only if not create a new one
    except Exception as ex:
        logging.info(ex)


def publish_message(project, topic, message, event_type):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic)
    future = publisher.publish(topic_path, message, event_type=event_type)
    try:
        future.result()
    except Exception as ex:
        logging.info(ex)
        future.cancel()
    logging.info(f"Published event {event_type} to {topic_path}.")


def create_subscription(project, topic, subscription):
    try:
        publisher = pubsub_v1.PublisherClient()
        subscriber = pubsub_v1.SubscriberClient()
        topic_path = publisher.topic_path(project, topic)
        subscription_path = subscriber.subscription_path(project, subscription)
        with subscriber:
            subscription_en = subscriber.create_subscription(
                request={"name": subscription_path, "topic": topic_path}
            )
        logging.info(f"Subscription created: {subscription_en}")
    except Exception as ex:
        logging.info(f"Error creating subscription {subscription} , the exception: {ex}.")
