# Sqs
from .sqs import sqs

# Utils
from botocore.exceptions import ClientError
from datetime import datetime


def send_message(queue, message_body, message_attributes):
    """
    Send a message to an Amazon SQS queue.

    :param queue: The queue that receives the message.
    :param message_body: The body text of the message.
    :param message_attributes: Custom attributes of the message. These are key-value
                               pairs that can be whatever you want.
    :return: The response from SQS that contains the assigned message ID.
    """

    try:
        response = queue.send_message(
            MessageBody=message_body,
            MessageAttributes=message_attributes
        )
        print(f"[{datetime.now()}] message Send: {message_body}")
        return response
    except ClientError as error:
        print(f"[{datetime.now()}] Send message failed: {message_body}")


if __name__ == '__main__':
    send_message(
        queue=sqs.get_queue_by_name(QueueName="conversiones"),
        message_body="Hola",
        message_attributes={
            "key1": {'StringValue': "value1", 'DataType': 'String'}
        }
    )