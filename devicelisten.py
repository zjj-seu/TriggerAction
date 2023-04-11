# 统筹设备状态更新的类，调用各个品类的IoT设备的状态更新接口,并选择性线程通信。
# 2023.5.4
# 心情好
from queue import Queue
from threading import Semaphore
from settings import Settings
from device_data_xmlreader import miio_DeviceDataXmlReader
from myYeelight import MyYeelight

import time
import sched

class DeviceTrigger:
    def __init__(self, devicestatus_queue:Queue, semaphore:Semaphore, trigger:dict) -> None:
        self._devicestatus_queue = devicestatus_queue
        self._semaphore = semaphore
        self._trigger = trigger

        self.device_id = trigger["targetdevicedid"]
        self.target_status = trigger["targetstatus"]
        self.device_name = trigger["targetdevicename"]
        self.current_status = None

        self.raise_count = 0
        self.s = sched.scheduler(time.time, time.sleep)
        self.trigger_listening_interval = Settings.trigger_listening_interval_sec

    def run(self):
        print("trigger listening activated!!! ")
        print(f"This trigger has been raised {self.raise_count} times")

        print(f"trying to get status whose did:{self.device_id}")
        self._devicestatus_queue.put(self.device_id)


        while self._devicestatus_queue.qsize() < 2:
            pass
            

        self.current_status = self._devicestatus_queue.get()
        self._devicestatus_queue.queue.clear()

        print(f"got needed status did:{self.device_id}, current_status:{self.current_status}, target_status:{self.target_status}")


        if self.current_status == self.target_status:
            self._semaphore.release()
            self.raise_count += 1
        
        self.s.enter(self.trigger_listening_interval, 1, self.run, ())
        self.s.run()

class DeviceCondition:
    def __init__(self, devicestatus_queue:Queue, semaphore_satisfied:Semaphore,semaphore_checked:Semaphore, condition:dict) -> None:
        self._devicestatus_queue = devicestatus_queue
        self._semaphore_satisfied = semaphore_satisfied
        self._semaphore_checked = semaphore_checked
        self._condition = condition

    def run(self):
        # TODO
        pass

class DeviceAction:
    def __init__(self, action:dict) -> None:
        self.action = action
    
    def run(self):
        id = self.action["id"]
        did = self.action["targetdevicedid"]
        print(f"action id: {id} running!!!")

        reader = miio_DeviceDataXmlReader("data_files/device_data.xml")
        local_device_list = reader.get_device_list()

        target_device = local_device_list[did + "_cn"]
        ip = target_device["ip"]
        token = target_device["token"]

        myyeelight = MyYeelight(ip, token)
        myyeelight.status_command(self.action["targetstatus"])

