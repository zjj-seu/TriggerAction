from abc import ABC,abstractclassmethod
import broadlink

from settings import Settings
from devicecontroller import DeviceController


class MyBroadLink(DeviceController):
    def __init__(self, devicedetails:dict) -> None:
        self.devicedetails = devicedetails
        self.dev_class:str = self.devicedetails["class"]
        
        self.broadlink_device:MyBroadLinkDevice = None
        
        if self.dev_class.startswith("broadlink.switch.sp4"):
            ip = self.devicedetails["ip"]
            port = self.devicedetails["port"]
            mac = self.devicedetails["mac"]
            devtype = self.devicedetails["devtype"]
            self.broadlink_device = SwitchSp4(ip,port,mac,devtype)
        
    def get_status(self)->str:
        return self.broadlink_device.get_status()
        
    def status_action(self, cmd:str):
        self.broadlink_device.status_cmd(cmd)
            
class MyBroadLinkDevice(ABC):
    def __init__(self, ip:str, port:str, mac:str, devtype:str) -> None:
        self.ip = ip
        self.port = int(port)
        byte_len = (int(mac).bit_length() + 7) // 8
        self.mac = int.to_bytes(int(mac), length=byte_len, byteorder="big")
        self.devtype = int(devtype)
    
    @abstractclassmethod
    def get_status(self)->str:
        pass
    
    @abstractclassmethod
    def status_cmd(self):
        pass
    
class SwitchSp4(MyBroadLinkDevice):
    def __init__(self, ip:str, port:str, mac:str, devtype:str) -> None:
        super().__init__(ip, port, mac, devtype)
        
        device_cache:dict = Settings.broadlink_device_dict_cache
        if mac not in device_cache:
            new_dev = broadlink.switch.sp4((self.ip, self.port),self.mac,self.devtype)
            new_dev.auth()
            device_cache[mac] = new_dev
        else:
            new_dev = device_cache[mac]
        
        self.device = new_dev
    

    def status_cmd(self, cmd:str):
        if cmd == "on":
            self.device.set_power(True)
        elif cmd == "off":
            self.device.set_power(False)
            

    def get_status(self)->str:
        return "on" if self.device.check_power() else "off"
    
    
