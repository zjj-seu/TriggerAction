# 用于创建事件，调用设备目录，调用类功能元数据，调用功能参数元数据

import os

from xml_reader import XmlReader
from settings import Settings
from eventfetch import EventAccessController
from contactqueue import ContactQueue


class EventCreater:
    def __init__(self, event_access_controller:EventAccessController, event_create_queue:ContactQueue) -> None:
        self._event_access_controller = event_access_controller
        self._event_create_queue = event_create_queue
        
        
    def AddEventToFiles(self, new_event:dict):
        self._event_access_controller.update_event(new_event)
        
        
        
        
if __name__ == "__main__":
    new_event = {'001': {'id': '001', 'name': 'save energy', 'status': 'on', 
                'eventdetails': {'trigger': {'type': 'status', 
                                            'id': '001101',
                                            'targetdevicedid': '317934913', 
                                            'targetstatus': 'on', 
                                            'targetdevicename': '台灯'}, 
                                'conditions': {'001201': {'type': 'time', 
                                                    'id': '001201', 
                                                    'targettimefrom': '18:00', 
                                                    'targettimeto': '18:10'}}, 
                                'actions': {'001301': {'type': 'status', 
                                                'id': '001301', 
                                                'targetdevicedid': '317934913', 
                                                'targetstatus': 'off', 
                                                'targetdevicename': '台灯'}}}}}
        
    