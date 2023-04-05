# 统筹设备状态更新的类，调用各个品类的IoT设备的状态更新接口,并选择性线程通信。
# 2023.5.4
# 心情好
from queue import Queue
from threading import Semaphore
import time

class DeviceTrigger:
    def __init__(self, devicestatus_queue:Queue, semaphore:Semaphore, trigger:dict) -> None:
        self._devicestatus_queue = devicestatus_queue
        self._semaphore = semaphore
        self._trigger = trigger

    def run(self):
        
        print("test trigger activated!!!")
        print("count down for 3 sec")
        time.sleep(3)
        print("raise trigger!!!")
        self._semaphore.release()

        pass

class DeviceCondition:
    def __init__(self, devicestatus_queue:Queue, semaphore_satisfied:Semaphore,semaphore_checked:Semaphore, condition:dict) -> None:
        self._devicestatus_queue = devicestatus_queue
        self._semaphore_satisfied = semaphore_satisfied
        self._semaphore_checked = semaphore_checked
        self._condition = condition

    def run(self):
        # TODO
        pass