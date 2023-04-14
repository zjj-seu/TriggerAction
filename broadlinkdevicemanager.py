import broadlink# 用设备的IP地址、MAC地址和设备类型创建设备对象
import time

"""
raw devicelist:

[broadlink.switch.sp4(('192.168.3.70', 80), 
mac=b'\xec\x0b\xae\xfc\x8cs', devtype=30056, 
timeout=10, name='博联智能插座', model='SP4L-CN', 
manufacturer='Broadlink', is_locked=False)]

processed for:

<device id="broadlink_001">
    <did>broadlink_001</did>
    <name>博联智能插座</name>
    <ip>192.168.3.70</ip>
    <port>80</port>
    <mac>b'\xec\x0b\xae\xfc\x8c\x73'</mac>
    <devtype>30056</devtype>
    <class>broadlink.switch.sp4</class>
</device>
"""

class DeviceInfoProcessor:
    def __init__(self, raw_broadlink_devicelist:list[broadlink.device.Device]) -> None:
        self.raw_broadlink_devicelist = raw_broadlink_devicelist

    def process_raw_devicelist(self):
        my_device_list = dict()

        for device in self.raw_broadlink_devicelist:
            deviceinfo = dict()
            did = str(int.from_bytes(device.mac, byteorder='little'))
            deviceinfo["did"] = did
            deviceinfo["mac"] = did
            deviceinfo["ip"] = device.host[0]
            deviceinfo["port"] = device.host[1]
            deviceinfo["name"] = device.name
            deviceinfo["devtype"] = device.devtype
            deviceinfo["class"] = device.__class__.__module__ + "." + device.__class__.__name__
            my_device_list[did] = deviceinfo
        
        return my_device_list


class BroadLinkDeviceManager:
    def __init__(self) -> None:
        self.devices = broadlink.discover()

    def refresh_and_get_raw_device_list(self):
        self.devices = broadlink.discover()
        return self.devices
    
    def refresh_and_get_processed_device_list(self):
        self.devices = broadlink.discover()
        process = DeviceInfoProcessor(self.devices)
        return process.process_raw_devicelist()



devices = broadlink.discover()
print(devices)
device = broadlink.switch.sp4(host=('192.168.3.70', 80), mac=b'\xec\x0b\xae\xfc\x8c\x73', devtype=30056)

# 连接到设备，并进行身份验证
device.auth()

# 打开SP4智能插座，并保持开启5秒钟
device.set_power(False)
time.sleep(5)

# 关闭SP4智能插座
device.set_power(True)
