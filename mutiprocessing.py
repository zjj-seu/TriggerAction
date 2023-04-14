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



class manager:
    def __init__(self, total_event_dict:dict) -> None:
        self._total_event_dict = total_event_dict
        self._valid_mess_queue = dict()

        self._event_dict_lock = Lock()
        self._queue_dict_lock = Lock()
        self._local_xml_lock = Lock()

        self._xmlreader = AllBrandDeviceDataReader(self._local_xml_lock)



    def run_threads(self):
        
        valid_trigger_listen_thread = Thread(target=self.valid_trigger_manager, 
                                             args=())

        device_check_thread = Thread(target=self.device_listen, args=())

        valid_trigger_listen_thread.start()
        device_check_thread.start()


    def device_listen(self):
        device_check = DeviceCheckServer(self._valid_mess_queue,self._queue_dict_lock,
                                         self._total_event_dict,self._event_dict_lock,self._xmlreader)
        device_check.run()

    def valid_trigger_manager(self):
        valid_trigger_manager = ValidTriggerManager(self._total_event_dict, self._valid_mess_queue, 
                                                    self._event_dict_lock, self._queue_dict_lock)
        valid_trigger_manager.run()

if __name__ == "__main__":
    eventfecher = EventFetcher(Settings.event_path,Settings.eventraw_path)
    total_event = eventfecher.get_event_list()
    m = manager(total_event)
    m.run_threads()

    
