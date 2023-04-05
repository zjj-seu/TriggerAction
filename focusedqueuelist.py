# 线程间通信队列组的类，后期可添加更多的信道
# 2023.5.4 天气阴
# believe yourself
from queue import Queue

class FocusedQueueList:
    def __init__(self) -> None:
        self.devicestatus_queue = Queue()
        self.time_queue = Queue()

