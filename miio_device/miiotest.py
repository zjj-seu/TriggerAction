from settings import Settings
from micloudconnector import MiCloudConnector
from midevicemanager import MiDeviceManager
from threading import Thread
from queue import Queue
from miio.integrations.yeelight.light.yeelight import Yeelight


def connect(q:Queue):
    miConnector = MiCloudConnector(Settings.username,Settings.password)
    miConnector.connect_to_micloud()
    midevicemanager = MiDeviceManager(miConnector)
    q.put(midevicemanager)


def process(q:Queue):
    connected_midevicemanager:MiDeviceManager = q.get()
    print("输入命令：0退出，1查看设备列表，2通过名称控制设备")
    answer_1 = input()
    while answer_1 != '0':
        if answer_1 == '1':
            print("设备列表")
            device_list = connected_midevicemanager.get_devicelist()
            for did, dev in device_list.items():
                print(f"name:{dev.name}\nip:{dev.ip}\ntoken:{dev.token}")
        else:
            print("输入设备名称")
            dev_name = input()
            my_ip, my_token = connected_midevicemanager.get_ip_token_with_name(dev_name)
            if my_ip != None:
                print(f"已找到设备\n名称：{dev_name}\nIp:{my_ip}\nToken:{my_token}")
                light_1s = Yeelight(ip=my_ip, token=my_token)
                print("执行操作：0退出，1开灯，2关灯")
                answer_2 = input()
                while answer_2 != '0':
                    if answer_2 == '1':
                        light_1s.on()
                    else:
                        light_1s.off()
                    
                    print("执行操作：0退出，1开灯，2关灯")
                    answer_2 = input()
            else:
                print("无该设备")
        print("输入命令：0退出，1查看设备列表，2通过名称控制设备")
        answer_1 = input()
        

def main():
    device_queue = Queue()

    thread_server = Thread(target=connect, args=(device_queue,))
    thread_processor = Thread(target=process, args=(device_queue,))

    thread_server.start()
    thread_processor.start()

if __name__ == "__main__":
    main()