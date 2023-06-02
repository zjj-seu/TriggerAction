# 根据从文件中获取到的事件字典创建对应的线程合作监听触发用户事件
# 2023.4.4 天气阴 心情一般 
# good luck
from threading import Thread
from threading import Lock
import time
from queue import Queue

from settings import Settings
from device_check_sever import DeviceCheckServer
from validtriggermanager import ValidTriggerManager
from eventfetch import EventFetcher
from device_data_xmlreader import AllBrandDeviceDataReader
from eventfetch import EventAccessController, EventDictAccess
from contactqueue import ContactQueue
from eventcreate import EventCreater




class manager:
    def __init__(self, total_event_dict_Access:EventDictAccess, event_access_controller:EventAccessController, xmlreader:AllBrandDeviceDataReader, new_event_queue:ContactQueue) -> None:
        self._total_event_dict_Access = total_event_dict_Access
        self._contact_queue = ContactQueue()
        self._xmlreader = xmlreader
        self._new_event_queue = new_event_queue
        self.event_Access = event_access_controller

    def run_threads(self):
        
        valid_trigger_listen_thread = Thread(target=self.valid_trigger_manager, 
                                             args=())

        device_check_thread = Thread(target=self.device_listen, args=())
        
        event_add_event = Thread(target=self.event_adder)
        
        event_add_event.start()
        valid_trigger_listen_thread.start()
        device_check_thread.start()
        
    def event_adder(self):
        event_add = EventCreater(self.event_Access, self._new_event_queue)
        event_add.run()


    def device_listen(self):
        device_check = DeviceCheckServer(self._contact_queue, self._total_event_dict_Access,self._xmlreader)
        device_check.run()

    def valid_trigger_manager(self):
        valid_trigger_manager = ValidTriggerManager(self._contact_queue, self._total_event_dict_Access,self._xmlreader)
        valid_trigger_manager.run()

def neweventtest(ContactQueue:ContactQueue):
    time.sleep(10)
    new_event = {'id': '0', 'name': 'save energy', 'status': 'on', 
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
    
    queue:Queue = ContactQueue.queue["update"]
    queue.put(new_event)

    
    

if __name__ == "__main__":
    eventAccess = EventAccessController(Settings.event_path,Settings.eventraw_path, Settings.eventclassraw_path)
    eventDictAccess = EventDictAccess(eventAccess)
    new_event_queue = ContactQueue()
    eventCreate = EventCreater(eventAccess, new_event_queue)
    filepathlist = {"mihome": Settings.mihome_devicefile_path, "broadlink": Settings.broadlink_devicefile_path}
    xmlreader = AllBrandDeviceDataReader(filepathlist)

    m = manager(eventDictAccess, eventAccess, xmlreader,new_event_queue)
    # Thread(target=neweventtest, args=(new_event_queue,)).start()
    
    m.run_threads()
    
    
    
    
