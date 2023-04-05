# 时间操作的监听类，用于响应时间操作的各种反馈
from queue import Queue
from threading import Semaphore
import time

class TimeTrigger:
    def __init__(self, time_queue:Queue, semaphore:Semaphore, trigger:dict):
        self._time_queue = time_queue
        self._semaphore = semaphore
        self._trigger = trigger

    def run(self):
        pass

class TimeCondition:
    def __init__(self, time_queue:Queue, semaphore_satisfied:Semaphore,semaphore_checked:Semaphore, condition:dict) -> None:
        self._time_queue = time_queue
        self._semaphore_satisfied = semaphore_satisfied
        self._semaphore_checked = semaphore_checked
        self._condition = condition

    def run(self):
        
        print("time condition checking")
        print("wait for 3 sec to run")
        time.sleep(3)
        print("condition satisfied")
        self._semaphore_satisfied.release()
        self._semaphore_checked.release()