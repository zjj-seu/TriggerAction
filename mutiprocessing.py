# 根据从文件中获取到的事件字典创建对应的线程合作监听触发用户事件
# 2023.4.4 天气阴 心情一般 
# good luck
from threading import Thread
from threading import Lock

from settings import Settings
from device_check_sever import DeviceCheckServer
from validtriggermanager import ValidTriggerManager
from eventfetch import EventFetcher
from device_data_xmlreader import AllBrandDeviceDataReader
from eventfetch import EventAccessController, EventDictAccess
from contactqueue import ContactQueue




class manager:
    def __init__(self, total_event_dict_Access:EventDictAccess) -> None:
        self._total_event_dict_Access = total_event_dict_Access
        self._contact_queue = ContactQueue()
        self._xmlreader = AllBrandDeviceDataReader()

    def run_threads(self):
        
        valid_trigger_listen_thread = Thread(target=self.valid_trigger_manager, 
                                             args=())

        device_check_thread = Thread(target=self.device_listen, args=())

        valid_trigger_listen_thread.start()
        device_check_thread.start()


    def device_listen(self):
        device_check = DeviceCheckServer(self._contact_queue, self._total_event_dict_Access,self._xmlreader)
        device_check.run()

    def valid_trigger_manager(self):
        valid_trigger_manager = ValidTriggerManager(self._contact_queue, self._total_event_dict_Access,self._xmlreader)
        valid_trigger_manager.run()

if __name__ == "__main__":
    eventAccess = EventAccessController(Settings.test_event_path,Settings.eventraw_path, Settings.eventclassraw_path)
    total_event = eventAccess.get_event_list()
    eventDictAccess = EventDictAccess(total_event)
    m = manager(eventDictAccess)
    m.run_threads()

    
