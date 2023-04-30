# 有效触发器监听线程，用于解析事件集合并决定高响应监听受关注设备的状态。
# 2023.5.4 
# 可能再分线程
import sched
import time
from threading import Lock,Thread
import threading

from settings import Settings
from abstract_event_run import AbstractEventRun
from device_data_xmlreader import AllBrandDeviceDataReader
from contactqueue import ContactQueue
from eventfetch import EventDictAccess

class ValidTriggerManager:
    def __init__(self, contact_queue_access:ContactQueue, event_dict_access:EventDictAccess, xmlreader:AllBrandDeviceDataReader) -> None:
        
        self.contact_queue_accessor = contact_queue_access
        self.event_dict_accessor = event_dict_access
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

        # TODO 
        event = AbstractEventRun(trigger, condition_dict, action_dict, self.contact_queue_accessor, self.xmlreader)
        event.run()

    def decode_event_dict(self):
        with self.event_dict_accessor.lock:
            for event_id, event in self.event_dict_accessor.eventlist.items():
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