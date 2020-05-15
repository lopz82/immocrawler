from azure.storage.queue import QueueClient, QueueMessage

from config import CONFIG
from utils import get_logger

CONNECTION_STRING = CONFIG["azure_queue"]["connection_string"]
QUEUE_NAME = "frankfurt"

log = get_logger(__name__)


class AzureStorageQueueClient:

    def __init__(self):
        self.client = QueueClient.from_connection_string(CONNECTION_STRING, QUEUE_NAME)

    def send_message(self, message: str) -> None:
        self.client.send_message(message)

    def receive_message(self) -> QueueMessage:
        messages = self.client.receive_messages()
        for msg in messages:
            return msg

    def delete_message(self, message: QueueMessage):
        self.client.delete_message(message)
