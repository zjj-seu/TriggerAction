# 统筹设备状态更新的类，调用各个品类的IoT设备的状态更新接口,并选择性线程通信。
# 2023.5.4
# 心情好
from queue import Queue

class DeviceListen:
    def __init__(self, devicestatus_queue:Queue) -> None:
        self._devicestatus_queue = devicestatus_queue

    def run(self):
        # TODO
        pass