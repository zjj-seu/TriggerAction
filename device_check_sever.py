# 用于高频查询设备状态
# TODO 多线程服务器查询有问题,使用了有等待限制的队列读取方法，但是这样会增加时间，建议改多线程暴力并行
from queue import Queue
from threading import Thread
from threading import Lock,Event
import time
import sched

from micloudconnector import MiCloudConnector
from midevicemanager import MiDeviceManager
from settings import Settings
from device_data_xmlreader import AllBrandDeviceDataReader
from mymihome import MyMiHome
from mybroadlink import MyBroadLink
from devicecontroller import DeviceController
from contactqueue import ContactQueue
from eventfetch import EventDictAccess

"""_summary_
想搞多线程，每个查询信道都分配一个线程，就需要管理好线程
线程管理需要注意一下几个问题
1、信道的创建、持续、结束
2、避免重复创建、避免空闲占用
"""


class DeviceCheckServer:
    def __init__(self, contact_queue_access:ContactQueue, event_dict_access:EventDictAccess, xmlreader:AllBrandDeviceDataReader) -> None:
        self.contact_queue_accessor = contact_queue_access
        self.event_dict_accessor = event_dict_access

        self.connector = MiCloudConnector(Settings.username,Settings.password)
        self.connector.connect_to_micloud()
        self.manager = MiDeviceManager(self.connector)

        self.s = sched.scheduler(time.time,time.sleep)
        self.update_mess_queue = sched.scheduler(time.time,time.sleep)
        self.update_mess_queue_interval = Settings.device_server_queue_check_interval_sec
        self.local_queue_dict = dict()
        self.lock_for_local_queue_list = Lock()
        
        self.xml_reader = xmlreader
        self.thread_table = dict()

    def check_current_event(self):
        with self.lock_for_local_queue_list:
            with self.contact_queue_accessor.lock:
                self.local_queue_dict.clear()
                for id, queue in self.contact_queue_accessor.eventlist.items():
                    if id.startswith("status"):
                        self.local_queue_dict[id] = queue
        
        self.update_mess_queue.enter(self.update_mess_queue_interval, 1, self.check_current_event, ())
        self.update_mess_queue.run()
        
    def thread_cell(self, id, queue:Queue, event:Event):
        print(f"[DeviceCheckServer.thread_cell:{id}] sever checking activated!!!")
        while not event.is_set():
            local_device_list = self.xml_reader.get_local_device_list()   
            did = queue.get()
            print(f"[DeviceCheckServer.thread_cell:{id}] id:{id}queue mess got")
            queue.queue.clear()
            device_details = local_device_list[did]
            deviceclass:str = device_details["class"]
            device_controller:DeviceController = None

            if deviceclass.startswith("miio"):
                print(f"[DeviceCheckServer.thread_cell:{id}] checking mihome did:{did} status")
                device_controller = MyMiHome(devicedetails=device_details)
            elif deviceclass.startswith("broadlink"):
                print(f"[DeviceCheckServer.thread_cell:{id}] checking broadlink did:{did} status")
                device_controller = MyBroadLink(devicedetails=device_details)
                
            queue.put(device_controller.get_status())
            queue.put(device_controller.get_status())
            
            time.sleep(0.5)
            
            
    def thread_manager(self):
        """_summary_
        周期性检查通信队列集合的队列情况，管理线程的增加和结束
        """
        with self.contact_queue_accessor.lock:
            for queue_id, queue in self.contact_queue_accessor.queue.items():
                if queue_id not in self.thread_table:
                    event = Event()
                    Thread(target=self.thread_cell, args=(queue_id, queue, event)).start()
                    self.thread_table[queue_id] = event
                    
        
        
        print("[DeviceCheckServer.thread_manager] thread management performed one times\"thread table:\n")
        # print(self.thread_table)
        
        self.s.enter(Settings.device_server_queue_check_interval_sec,1,self.thread_manager,())
        self.s.run()
            
        
                
    def server(self):
        print(f"[DeviceCheckServer] getting online device list ")

        local_device_list = self.xml_reader.get_local_device_list()

        """
        {'317934913_cn': {'name': '台灯', 'did': '317934913', 'ip': '192.168.3.54', 'token': '9490458620e6604d712ccad862bc32b6'}, 
        '108412119_cn': {'name': '小爱音箱 万能遥控版', 'did': '108412119', 'ip': '192.168.3.64', 'token': '704e665a31787076614f354950436c6f'}, 
        'ir.1543249323641991168_cn': {'name': '空调', 'did': 'ir.1543249323641991168', 'ip': None, 'token': None}}
        """
        with self.lock_for_local_queue_list:
            print(f"[DeviceCheckServer] checking device status")
            for id, queue in self.local_queue_dict.items():
                print(f"[DeviceCheckServer] id:{id}queue mess getting")

                try:
                    did = queue.get(timeout= 0.01)
                except:
                    continue
                
                queue.queue.clear()
                device_details = local_device_list[did]
                deviceclass:str = device_details["class"]
                device_controller:DeviceController = None

                if deviceclass.startswith("miio"):
                    print(f"[DeviceCheckServer] checking mihome did:{did} status")
                    device_controller = MyMiHome(devicedetails=device_details)
                elif deviceclass.startswith("broadlink"):
                    print(f"[DeviceCheckServer] checking broadlink did:{did} status")
                    device_controller = MyBroadLink(devicedetails=device_details)
                    
                queue.put(device_controller.get_status())
                queue.put(device_controller.get_status())
            
        print("[DeviceCheckServer] plan next check")

        self.s.enter(Settings.device_data_check_interval_sec,1,self.server,())
        self.s.run()

    def run(self):
        print("[DeviceCheckServer] initiating device check server!!!")

        # Thread(target=self.check_current_event,args=()).start()
        # Thread(target=self.server,args=()).start()
        Thread(target=self.thread_manager, args=()).start()
         