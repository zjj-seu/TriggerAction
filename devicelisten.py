# 统筹设备状态更新的类，调用各个品类的IoT设备的状态更新接口,并选择性线程通信。
# 2023.5.4
# 心情好
from queue import Queue
from threading import Semaphore
import time
import sched

from settings import Settings
from device_data_xmlreader import miio_DeviceDataXmlReader
from device_data_xmlreader import AllBrandDeviceDataReader
from mymihome import MyMiHome
from mybroadlink import MyBroadLink
from devicecontroller import DeviceController


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
        print(f"[DeviceTrigger] trigger listening activated!!! This trigger has been raised {self.raise_count} times")
        print(f"[DeviceTrigger] trying to get status whose did:{self.device_id}")
        self._devicestatus_queue.put(self.device_id)

        while self._devicestatus_queue.qsize() < 2:
            pass
            
        print("[DeviceTrigger] return to trigger")
        
        self.current_status = self._devicestatus_queue.get()
        self._devicestatus_queue.queue.clear()

        print(f"[DeviceTrigger] got needed status did:{self.device_id}, current_status:{self.current_status}, target_status:{self.target_status}")


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
        
        self.device_id = condition["targetdevicedid"]
        self.target_status = condition["targetstatus"]
        self.current_status = None

    def run(self):
        print("[DeviceCondition] condition checking activated!!! ")
        
        print(f"[DeviceCondition] trying to get status whose did:{self.device_id}")
        self._devicestatus_queue.put(self.device_id)


        while self._devicestatus_queue.qsize() < 2:
            pass
            
        print("[DeviceCondition] return to condtion checker")
        
        self.current_status = self._devicestatus_queue.get()
        self._devicestatus_queue.queue.clear()

        print(f"[DeviceCondition] got needed status did:{self.device_id}, current_status:{self.current_status}, target_status:{self.target_status}")


        if self.current_status == self.target_status:
            self._semaphore_satisfied.release()
        
        self._semaphore_checked.release()

class DeviceAction:
    def __init__(self, action:dict, xmlreader:AllBrandDeviceDataReader) -> None:
        self.action = action
        self.xmlreader = xmlreader
        
        self.device_controller:DeviceController = None
    
    def run(self):
        id = self.action["id"]
        did = self.action["targetdevicedid"]
        print(f"[DeviceAction] action id: {id} running!!!")

        
        local_device_list = self.xmlreader.get_local_device_list()
        target_device_details = local_device_list[did]
        device_class:str = target_device_details["class"]
        device_controller:DeviceController = None
        cmd = self.action["targetstatus"]
        if device_class.startswith("miio"):
            device_controller = MyMiHome(target_device_details)
        elif device_class.startswith("broadlink"):
            device_controller = MyBroadLink(target_device_details)
        
        device_controller.status_action(cmd)


