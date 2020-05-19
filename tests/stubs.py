import datetime


class QueueMessage:
    def __init__(self, msg):
        self.msg = msg

    @property
    def content(self):
        return self.msg

    @property
    def id(self):
        return 1


class DB:
    def save(self):
        pass


class Queue:
    def receive_message(self):
        pass

    def delete_message(self):
        pass


class Result:
    def __init__(self, content=None):
        self.content = content

    @property
    def data(self):
        return self.content


class Task:
    def __init__(self, result=None):
        self.result = result

    def run(self):
        return self.result


class Date(datetime.datetime):
    @classmethod
    def now(cls):
        return cls(1982, 7, 16, 18, 0, 0)
