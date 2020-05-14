from typing import Iterable

from azure.storage.queue import QueueClient

from config import CONFIG

CONNECTION_STRING = CONFIG["azure_queue"]["connection_string"]
QUEUE_NAME = "frankfurt"


class QueueClient:

    def __init__(self):
        self.client = QueueClient.from_connection_string(CONNECTION_STRING, QUEUE_NAME)

    def send_meesage(self, message: str) -> None:
        self.client.send_message(message)

    def receive_messages_content(self) -> Iterable[str]:
        messages = self.client.receive_messages()
        for msg in messages:
            return msg.content
