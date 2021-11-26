# Celery
from worker_celery.tasks import convert

# Sqs
from sqs import sqs
from delete_messages import delete_messages

# Utils
from botocore.exceptions import ClientError
from datetime import datetime


def pull_tasks():
    """
    Pull messages from sqs and invoke celery task.
    :return:
    """
    print(f"[{datetime.now()}] Listening for messages...")
    queue = sqs.get_queue_by_name(QueueName="conversiones")
    received_messages = receive_messages(queue=queue, max_number=10, wait_time=2)
    if received_messages:
        for msg in received_messages:
            convert(*unpack_message(msg))
            print(f'[{datetime.now()}] Body: {msg.body}, Attributes: {msg.message_attributes}')
        delete_messages(queue, received_messages)


def receive_messages(queue, max_number, wait_time):
    """
    Receive a batch of messages in a single request from an SQS queue.

    :param queue: The queue from which to receive messages.
    :param max_number: The maximum number of messages to receive. The actual number
                       of messages received might be less.
    :param wait_time: The maximum time to wait (in seconds) before returning. When
                      this number is greater than zero, long polling is used. This
                      can result in reduced costs and fewer false empty responses.
    :return: The list of Message objects received. These each contain the body
             of the message and metadata and custom attributes.
    """
    try:
        messages = queue.receive_messages(
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=max_number,
            WaitTimeSeconds=wait_time
        )
        for msg in messages:
            print(f"[{datetime.now()}] Received message {msg.message_id}, {msg.body}")
        return messages
    except ClientError as error:
        print(f"[{datetime.now()}] could not receive messages{error}")


def unpack_message(msg):
    try:
        return (
            msg.message_attributes.get("user_id", {}).get("StringValue", "unknown"),
            msg.message_attributes.get("original_filename", {}).get("StringValue", "unknown"),
            msg.message_attributes.get("new_format", {}).get("StringValue", "unknown"),
            msg.message_attributes.get("created_at", {}).get("StringValue", "unknown"),
            msg.message_attributes.get("filename_to_delete", {}).get("StringValue", "unknown"),
            msg.message_attributes.get("s3_path", {}).get("StringValue", "unknown"),
        )
    except:
        return "", msg.body, 0


if __name__ == '__main__':
    while True:
        pull_tasks()
