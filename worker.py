from time import sleep
from typing import Tuple

from db import MongoDB
from messaging import AzureStorageQueueClient
from tasks import SearchTaskFactory
from utils import get_logger, random_time

log = get_logger(__name__)


class Worker:

    @classmethod
    def get_azure_worker(cls):
        return cls(MongoDB(), AzureStorageQueueClient())

    def __init__(self, db, queue_client, wait: Tuple[int, int] = None):
        self.db = db
        self.queue = queue_client
        self.wait = (5, 10) or tuple(wait)
        self.task = None
        self.last_retrieved_message = None
        self.result = None
        self.get_task()

    def get_task(self) -> None:
        log.info("Retrieving message from the queue...")
        message = self.queue.receive_message()
        if message:
            self.last_retrieved_message = message
            log.info(f"Message {message.id} retrieved.")
            log.debug(f"Message details {message}")
            log.info("Creating new task...")
            self.task = SearchTaskFactory.new_task(message.content)
            log.info(f"{self.task} created")
        else:
            log.info("Empty queue. No new task will be created.")
            self.task = None

    def task_competed(self) -> None:
        log.info(f"{self.task} completed.")
        log.info(f"Task completed. Deleting last retrieved message from the queue.")
        self.queue.delete_message(self.last_retrieved_message)
        self.last_retrieved_message = None

    def perform_task(self) -> None:
        try:
            if self.task:
                sleep(random_time(self.wait))
                self.result = self.task.run()
                self.save_result()
        except:
            pass
        else:
            self.task_competed()

    def save_result(self) -> None:
        log.info("Saving results to the database...")
        log.debug(f"Saving: {self.result}")
        self.db.save(self.result)
        log.info("Results saved successfully.")

    def run(self) -> None:
        log.info("Starting worker...")
        while self.task:
            self.get_task()
            self.perform_task()
        log.info("No more tasks in the queue, stopping...")


if __name__ == '__main__':
    worker = Worker.get_azure_worker()
    worker.run()
