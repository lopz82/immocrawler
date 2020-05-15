from messaging import AzureStorageQueueClient
from search import ImmobilienScoutSearch
from utils import get_logger

log = get_logger(__name__)


class Publisher:

    def __init__(self, **kwargs):
        self.search = ImmobilienScoutSearch(**kwargs)
        self.queue = AzureStorageQueueClient()
        self.urls = None

    def search_results(self):
        log.info("Generating result urls...")
        self.urls = self.search.run()

    def publish_tasks(self):
        log.info(f"Sending {len(self.urls)} results to the queue...")
        for url in self.urls:
            self.queue.send_message(url)
        log.info(f"{len(self.urls)} sent successfully to the queue.")

    def publish(self):
        self.search_results()
        self.publish_tasks()

