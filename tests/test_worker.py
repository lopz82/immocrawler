from unittest.mock import MagicMock, patch

import pytest

from immocrawler.db import MongoDB
from immocrawler.messaging import AzureStorageQueueClient
from immocrawler.tasks import SearchTaskFactory, SearchTask
from immocrawler.worker import Worker
from tests.helpers import AlmostAlwaysTrue
from tests.stubs import DB, Queue, QueueMessage, Result


@pytest.fixture(scope="function")
def worker():
    return Worker(DB(), Queue())


def test_class_method_get_azure_worker():
    w = Worker.get_azure_worker()
    assert isinstance(w, Worker)
    assert isinstance(w.db, MongoDB)
    assert isinstance(w.queue, AzureStorageQueueClient)


def test_worker_init(worker):
    assert isinstance(worker.db, DB)
    assert isinstance(worker.queue, Queue)
    assert worker.wait == (5, 10)
    assert worker.task is None
    assert worker.last_retrieved_message is None
    assert worker.result is None


@patch("immocrawler.tasks.SearchTaskFactory.new_task")
def test_get_taskworker(mock_factory_method, worker):
    # Mocking queue.receive_message response. Returns a message
    msg = QueueMessage("Message")
    worker.queue.receive_message = MagicMock(return_value=msg, autospec=True)
    # Creating response for SearchTaskFactory classmethod
    task = SearchTask("http://fake.url")
    mock_factory_method.return_value = task  # We are mocking directly the method.

    worker.get_task()
    worker.queue.receive_message.assert_called_once()
    SearchTaskFactory.new_task.assert_called_once_with("Message")
    assert worker.task == task
    assert worker.last_retrieved_message == msg

    worker.queue.receive_message = MagicMock(return_value=None, autospec=True)
    worker.get_task()
    assert worker.task is None


def test_task_completed(worker):
    worker.task = SearchTask("http://fake.url")
    last_message = QueueMessage("Last message")
    worker.last_retrieved_message = last_message
    worker.queue.delete_message = MagicMock(autospec=True)

    worker.task_completed()
    assert worker.queue.delete_message.call_args.args == (last_message,)
    assert worker.queue.delete_message.call_count == 1
    assert worker.last_retrieved_message is None


@patch("immocrawler.worker.random_time")
@patch("immocrawler.worker.sleep")
def test_perform_task(mock_sleep, mock_random_time, worker):
    # Checking if self.task
    worker.last_retrieved_message = QueueMessage("Message")
    res = Result()
    search_task = MagicMock()
    search_task.run.return_value = res
    worker.task = search_task
    worker.task_completed = MagicMock(autospec=True)
    worker.save_result = MagicMock(autospec=True)
    mock_random_time.return_value = 8

    worker.perform_task()
    assert worker.task == search_task
    assert worker.result == res
    assert mock_sleep.call_count == 1
    assert mock_sleep.call_args.args == (8,)
    assert mock_random_time.call_count == 1
    assert worker.save_result.call_count == 1
    assert worker.task_completed.call_count == 1


@patch("immocrawler.worker.log.info")
def test_save_result(mock_log_info, worker):
    # if message:
    worker.db.save = MagicMock(autospec=True)
    res = Result()
    worker.result = res

    worker.save_result()
    assert worker.db.save.call_count == 1
    assert worker.db.save.call_args.args == (res,)

    # else
    # Reseting mock_log_info after running first part of the test
    mock_log_info.call_count = 0
    worker.result = None
    worker.save_result()

    assert mock_log_info.call_count == 1

# The key difference to use a stub or a mock is how easy is to access that object/method
# If we need to check if the method was called we need a mock (via MagicMock if we can access
# the object/method or patch for system or imported dependencies).
# If we just need to set a value, a stub should be enough.

def test_run(worker):
    worker.get_task = MagicMock()
    worker.perform_task = MagicMock()
    worker.task = AlmostAlwaysTrue(total_iterations=2)
    worker.run()

    assert worker.get_task.call_count == 2
    assert worker.perform_task.call_count == 1
