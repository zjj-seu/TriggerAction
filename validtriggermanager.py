# 有效触发器监听线程，用于解析事件集合并决定高响应监听受关注设备的状态。
# 2023.5.4 
# 可能再分线程
import sched
import time
from settings import Settings
from threading import Lock
import threading
from threading import Thread

class ValidTriggerManager:
    def __init__(self, total_event_dict:dict, focused_queue_list, event_dict_lock) -> None:
        self._total_event_dict = total_event_dict
        self._focused_queue_list = focused_queue_list
        self._event_dict_lock = event_dict_lock

        self.thread_manage_table = dict()


        self.interval = Settings.event_decode_interval_sec
        self.s = sched.scheduler(time.time, time.sleep)

    def run(self):
        self.decode_event_dict = self.s.enter(self.interval,1,self.decode_event_dict,argument=(self._total_event_dict,self._event_dict_lock,))
        self.s.run()



    def valid_event_processing(self, event_id, trigger:dict, condition_dict:dict, action_dict:dict):
        # 向事件线程管理表中添加正在执行的合法事件线程和事件id的对应信息
        thread_id = threading.current_thread().ident
        self.thread_manage_table[event_id] = thread_id

        



    def decode_event_dict(self, total_event_dict:dict, event_dict_lock:Lock):
        with event_dict_lock:
            for event_id, event in total_event_dict.items():
                # 如果该事件未激活或者已启动响应线程则跳过
                # TODO 事件不激活的处理待定
                if(event["status"] == "off" or event_id in self.thread_manage_table):
                    continue

                trigger = event["eventdetails"]["trigger"]
                condition_dict = event["eventdetails"]["conditions"]
                action_dict = event["eventdetails"]["actions"]


                valid_event_thread = Thread(target=self.valid_event_processing, args=(event_id,trigger,condition_dict,action_dict))
                valid_event_thread.start()

        self.s.enter(self.interval,1,self.decode_event_dict,argument=(total_event_dict,event_dict_lock,))
        self.s.run()