# 用于高频查询设备状态
# TODO 多线程服务器查询有问题,使用了有等待限制的队列读取方法，但是这样会增加时间，建议改多线程暴力并行
from queue import Queue
from settings import Settings
from threading import Lock
import time
import sched

from micloudconnector import MiCloudConnector
from midevicemanager import MiDeviceManager


from threading import Thread
from device_data_xmlreader import AllBrandDeviceDataReader
from mymihome import MyMiHome
from mybroadlink import MyBroadLink
from devicecontroller import DeviceController



class DeviceCheckServer:
    def __init__(self, valid_queue_dict:dict, queue_dict_lock:Lock, total_event_dict:dict, event_dict_lock:Lock, xmlreader:AllBrandDeviceDataReader) -> None:
        self.valid_queue_dict = valid_queue_dict
        self.queue_dict_lock = queue_dict_lock
        self.lock_for_event_dict = event_dict_lock
        self.total_event_dict = total_event_dict

        self.connector = MiCloudConnector(Settings.username,Settings.password)
        self.connector.connect_to_micloud()
        self.manager = MiDeviceManager(self.connector)

        self.s = sched.scheduler(time.time,time.sleep)
        self.update_mess_queue = sched.scheduler(time.time,time.sleep)
        self.lock_for_local_queue_list = Lock()
        self.update_mess_queue_interval = Settings.device_server_queue_check_interval_sec
        self.local_queue_dict = dict()
        
        self.xml_reader = xmlreader

    def check_current_event(self):
        with self.lock_for_local_queue_list:
            with self.lock_for_event_dict:
                self.local_queue_dict.clear()
                for id, queue in self.valid_queue_dict.items():
                    if id.startswith("status"):
                        self.local_queue_dict[id] = queue
        
        self.update_mess_queue.enter(self.update_mess_queue_interval, 1, self.check_current_event, ())
        self.update_mess_queue.run()

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

        Thread(target=self.check_current_event,args=()).start()
        Thread(target=self.server,args=()).start()
         