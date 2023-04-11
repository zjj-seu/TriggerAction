from abc import ABC, abstractmethod
from threading import Lock
from threading import Thread,Event
import threading
import time 
import sched

from devicelisten import DeviceTrigger,DeviceCondition,DeviceAction
from timelisten import TimeCondition,TimeTrigger
from queue import Queue
from restart_thread import MyThread

from focusedqueuelist import FocusedQueueList

class AbstractEventRun(ABC):
    def __init__(self, trigger:dict, condition_dict:dict, action_dict:dict, valid_mess_queue:dict, queue_dict_lock:Lock) -> None:
        super().__init__()
        self.trigger = trigger
        self.condition_dict = condition_dict
        self.action_dict = action_dict
        self.valid_mess_queue = valid_mess_queue
        self.queue_dict_lock = queue_dict_lock

        self.condition_count = len(self.condition_dict)
        self.action_count = len(self.action_dict)

        self.trigger_raised_semaphore = threading.Semaphore(0)
        self.condition_satisfied_semaphore = threading.Semaphore(0)
        self.condition_checked_semaphore = threading.Semaphore(0)


    def trigger_decode(self):    
        id = self.trigger["id"]
        print("id:{id} trigger_decode running!")

        trigger_type = self.trigger["type"]
        if trigger_type == "status":
            mess_queue = Queue()
            with self.queue_dict_lock:
                self.valid_mess_queue["status" + self.trigger["id"]] = mess_queue
            
            device_listenner = DeviceTrigger(mess_queue,
                                             self.trigger_raised_semaphore,
                                             self.trigger)
            Thread(target=device_listenner.run).start()
        elif trigger_type == "time":
            mess_queue = Queue()
            with self.queue_dict_lock:
                self.valid_mess_queue["time" + self.trigger["id"]] = mess_queue

            time_listenner = TimeTrigger(mess_queue,
                                         self.trigger_raised_semaphore,
                                         self.trigger)
            Thread(target=time_listenner.run).start()

    def condition_decode(self):
        
        condition_thread_list = []

        for id, conditon_details in self.condition_dict.items():
            id = conditon_details["id"]
            print("id:{id} condition_decode running!")

            if conditon_details["type"] == "status":
                mess_queue = Queue()
                with self.queue_dict_lock:
                    self.valid_mess_queue["status" + conditon_details["id"]] = mess_queue

                device_condition_check = DeviceCondition(mess_queue,
                                                        self.condition_satisfied_semaphore,
                                                        self.condition_checked_semaphore,
                                                        conditon_details)
                device_condition_check_thread = MyThread(target=device_condition_check.run)
                condition_thread_list.append(device_condition_check_thread)
            elif conditon_details["type"] == "time":
                mess_queue = Queue()
                with self.queue_dict_lock:
                    self.valid_mess_queue["time" + conditon_details["id"]] = mess_queue

                time_condition_check = TimeCondition(mess_queue,
                                                    self.condition_satisfied_semaphore,
                                                    self.condition_checked_semaphore,
                                                    conditon_details)
                time_condition_check_thread = MyThread(target=time_condition_check.run)
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
        
        action_thread_list = []

        for id, action_details in self.action_dict.items():
            if action_details["type"] == "status":
                action_one = DeviceAction(action_details)
                action_thread = MyThread(target=action_one.run)
                action_thread_list.append(action_thread)

        while True:
            self.condition_satisfied_semaphore.acquire(self.condition_count)

            for thread in action_thread_list:
                print(f"=======================\n" + 
                        "action  is running\n" )
                thread.start()
        

    def run(self):
        id = self.trigger["id"]
        print(f"one event has run!!! whose trigger id is {id}")
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

