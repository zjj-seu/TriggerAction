# 根据从文件中获取到的事件字典创建对应的线程合作监听触发用户事件
# 2023.4.4 天气阴 心情一般 
# good luck
from threading import Thread
from threading import Lock

from focusedqueuelist import FocusedQueueList

from devicelisten import DeviceListen
from timelisten import TimeListen
from validtriggermanager import ValidTriggerManager


class manager:
    def __init__(self, total_event_dict:dict) -> None:
        self._total_event_dict = total_event_dict
        self._focused_queue_list = FocusedQueueList()

        self._event_dict_lock = Lock()

    def run_threads(self):
        device_listen_thread = Thread(target=self.device_listen, 
                                      args=(self,self._focused_queue_list.devicestatus_queue))
        time_listen_thread = Thread(target=self.time_listen, 
                                    args=(self,self._focused_queue_list.time_queue))
        
        valid_trigger_listen_thread = Thread(target=self.device_listen, 
                                             args=(self,self._total_event_dict,
                                                   self._focused_queue_list,self._event_dict_lock))

        device_listen_thread.run()
        valid_trigger_listen_thread.run()

    def time_listen(self, time_queue):
        time_listener =  TimeListen(time_queue)
        time_listener.run()

    def device_listen(self, devicestatus_queue):
        device_listener = DeviceListen(devicestatus_queue)
        device_listener.run()

    def valid_trigger_manager(self, total_event_dict:dict, focused_queue_list, event_dict_lock):
        valid_trigger_manager = ValidTriggerManager(total_event_dict, focused_queue_list, event_dict_lock)
        valid_trigger_manager.run()

    
