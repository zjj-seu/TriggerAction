# 用于创建事件，调用设备目录，调用类功能元数据，调用功能参数元数据

import os
from threading import Thread, Event
from queue import Queue

from xml_reader import XmlReader
from settings import Settings
from eventfetch import EventAccessController
from contactqueue import ContactQueue


class EventCreater:
    def __init__(self, event_access_controller:EventAccessController, event_create_queue:ContactQueue) -> None:
        self._event_access_controller = event_access_controller
        self._event_create_queue = event_create_queue
        self.current_event_id = str(len(self._event_access_controller.get_event_list()))
        self.close_event = Event()
        
        
    def AddEventToFiles(self, new_event:dict):
        new_event["id"]= self.current_event_id
        
        for key, value in new_event["eventdetails"].items():
            if key == "trigger":
                value["id"] = self.current_event_id + value["id"]
            if key == "conditions":
                for condition_key, condition_val in value.items():
                    condition_key = self.current_event_id + condition_key
                    condition_val["id"] = self.current_event_id + condition_val["id"]
            if key == "actions":
                for action_key, action_val in value.items():
                    action_key = self.current_event_id + action_key
                    action_val["id"] = self.current_event_id + action_val["id"]
        
        self._event_access_controller.update_event(new_event)
        
    def run(self):
        with self._event_create_queue.lock:
            self._event_create_queue.queue["create"] = Queue() # 先做增加
            self._event_create_queue.queue["update"] = Queue()
        
        while not self.close_event.is_set():
            new_event_queue:Queue = self._event_create_queue.queue["create"]
            raw_event = new_event_queue.get()
            self.AddEventToFiles(raw_event)
        
        
        
        
if __name__ == "__main__":
    new_event = {'id': '#', 'name': 'save energy', 'status': 'on', 
        'eventdetails': {'trigger': {'type': 'status', 
                                    'id': '101', 
                                    'targetdevicedid': '317934913_cn', 
                                    'targetstatus': 'off', 
                                    'targetdevicename': '台灯'}, 
                        'conditions': {'201': {'type': 'status', 
                                                'id': '201', 
                                                'targetdevicedid': '127049371880428', 
                                                'targetstatus': 'on', 
                                                'targetdevicename': '博联智能插座'}}, 
                        'actions': {'301': {'type': 'status', 
                                                'id': '301', 
                                                'targetdevicedid': '127049371880428', 
                                                'targetstatus': 'off', 
                                                'targetdevicename': '博联智能插座'}}}}
    
    
        
    