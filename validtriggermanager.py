# 有效触发器监听线程，用于解析事件集合并决定高响应监听受关注设备的状态。
# 2023.5.4 
# 可能再分线程
import sched
import time
from settings import Settings
from threading import Lock
import threading
from threading import Thread

from abstract_event_run import AbstractEventRun
from device_data_xmlreader import AllBrandDeviceDataReader

class ValidTriggerManager:
    def __init__(self, total_event_dict:dict, valid_queue_list:dict, event_dict_lock:Lock, queue_dict_lock:Lock, xmlreader:AllBrandDeviceDataReader) -> None:
        self._total_event_dict = total_event_dict
        self._valid_mess_queue = valid_queue_list
        self._event_dict_lock = event_dict_lock
        self._queue_dict_lock = queue_dict_lock
        self.xmlreader = xmlreader

        self.thread_manage_table = dict()

        self.interval = Settings.event_decode_interval_sec
        self.s = sched.scheduler(time.time, time.sleep)

    def run(self):
        self.decode_event_dict()

    def valid_event_processing(self, event_id, trigger:dict, condition_dict:dict, action_dict:dict):
        # 向事件线程管理表中添加正在执行的合法事件线程和事件id的对应信息
        thread_id = threading.current_thread().ident
        self.thread_manage_table[event_id] = thread_id

        event = AbstractEventRun(trigger, condition_dict, action_dict, self._valid_mess_queue, self._queue_dict_lock, self.xmlreader)
        event.run()

    def decode_event_dict(self):
        with self._event_dict_lock:
            for event_id, event in self._total_event_dict.items():
                # 如果该事件未激活或者已启动响应线程则跳过
                # TODO 事件不激活的处理待定
                if(event["status"] == "off" or event_id in self.thread_manage_table):
                    continue

                trigger = event["eventdetails"]["trigger"]
                condition_dict = event["eventdetails"]["conditions"]
                action_dict = event["eventdetails"]["actions"]


                valid_event_thread = Thread(target=self.valid_event_processing, args=(event_id,trigger,condition_dict,action_dict,))
                valid_event_thread.start()

        self.s.enter(self.interval,1,self.decode_event_dict,())
        self.s.run()