# 时间操作的监听类，用于响应时间操作的各种反馈
from queue import Queue

class TimeListen:
    def __init__(self, time_queue:Queue) -> None:
        self._time_queue = time_queue

    def run(self):
        pass