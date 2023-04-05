from abc import ABC, abstractmethod
from threading import Lock
from threading import Thread,Event
import threading
import time 
import sched

from devicelisten import DeviceTrigger,DeviceCondition
from timelisten import TimeCondition,TimeTrigger

from focusedqueuelist import FocusedQueueList

class AbstractEventRun(ABC):
    def __init__(self, trigger:dict, condition_dict:dict, action_dict:dict, focused_queue_dict:FocusedQueueList) -> None:
        super().__init__()
        self.trigger = trigger
        self.condition_dict = condition_dict
        self.action_dict = action_dict
        self.focused_queue_dict = focused_queue_dict

        self.condition_count = len(self.condition_dict)
        self.action_count = len(self.action_dict)

        self.trigger_raised_semaphore = threading.Semaphore(0)
        self.condition_satisfied_semaphore = threading.Semaphore(0)
        self.condition_checked_semaphore = threading.Semaphore(0)


    def trigger_decode(self):    
        trigger_type = self.trigger["type"]
        if trigger_type == "status":
            device_listenner = DeviceTrigger(self.focused_queue_dict.devicestatus_queue,
                                             self.trigger_raised_semaphore,
                                             self.trigger)
            Thread(target=device_listenner.run).start()
        elif trigger_type == "time":
            time_listenner = TimeTrigger(self.focused_queue_dict.time_queue,
                                         self.trigger_raised_semaphore,
                                         self.trigger)
            Thread(target=time_listenner.run).start()

    def condition_decode(self):
        condition_thread_list = []

        for id, conditon_details in self.condition_dict.items():
            if conditon_details["type"] == "status":
                device_condition_check = DeviceCondition(self.focused_queue_dict.devicestatus_queue,
                                                                self.condition_satisfied_semaphore,
                                                                self.condition_checked_semaphore,
                                                                conditon_details)
                device_condition_check_thread = Thread(target=device_condition_check.run)
                condition_thread_list.append(device_condition_check_thread)
            elif conditon_details["type"] == "time":
                time_condition_check = TimeCondition(self.focused_queue_dict.time_queue,
                                                            self.condition_satisfied_semaphore,
                                                            self.condition_checked_semaphore,
                                                            conditon_details)
                time_condition_check_thread = Thread(target=time_condition_check.run)
                condition_thread_list.append(time_condition_check_thread)

        # 等待触发器触发再执行检查
        while True:
            self.trigger_raised_semaphore.acquire(1)
            for thread in condition_thread_list:
                thread.start()

            self.condition_checked_semaphore.acquire(self.condition_count)
            time.sleep(1)
            
            satified_count = self.condition_satisfied_semaphore._value
            print(f"dictlen:{self.condition_count}")
            print(f"checked num:{self.condition_checked_semaphore._value}")
            print(f"satisfied num:{self.condition_satisfied_semaphore._value}")
            if satified_count != self:
                self.condition_satisfied_semaphore.acquire(satified_count)
            
            print("=========================================")
            print(f"checked num:{self.condition_checked_semaphore._value}")
            print(f"satisfied num:{self.condition_satisfied_semaphore._value}")
            continue


    def action_decode(self):
        self.condition_satisfied_semaphore.acquire(self.condition_count)
        print("action_performed")
        

    def run(self):
        Thread(target=self.trigger_decode).start()
        Thread(target=self.condition_decode).start()
        Thread(target=self.action_decode).start()



if __name__ == "__main__":
    trigger = {'type': 'status', 
                'targetdevicedid': '317934913', 
                'targetstatus': 'on', 
                'targetdevicename': '台灯'}
    
    condition_dict = {'1': {'type': 'time', 
                            'id': '1', 
                            'targettimefrom': '18:00', 
                            'targettimeto': '18:10'}}
    
    action_dict = {'1': {'type': 'status', 
                        'id': '1', 
                        'targetdevicedid': '317934913', 
                        'targetstatus': 'off', 
                        'targetdevicename': '台灯'}}
    
    print("run")
    
    mess_queue = FocusedQueueList()
    a = AbstractEventRun(trigger, condition_dict, action_dict, mess_queue)
    a.run()

