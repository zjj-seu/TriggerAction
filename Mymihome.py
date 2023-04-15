from devicecontroller import DeviceController
from abc import ABC, abstractclassmethod
from miio.integrations.yeelight.light.yeelight import Yeelight,YeelightStatus



class MyMiHome(DeviceController):
    def __init__(self, devicedetails:dict) -> None:
        self.device_details = devicedetails
        self.device_class:str = self.device_details["class"]
        self.MiHomeDevice:MyMiHomeDevice = None
        
        if self.device_class.startswith("miio.integrations.yeelight.light.yeelight.Yeelight"):
            ip = self.device_details["ip"]
            token = self.device_details["token"]
            self.MiHomeDevice = MyYeelight(ip,token)
        
    def get_status(self):
        return self.MiHomeDevice.get_power_status()
        
    def status_action(self, cmd:str):
        self.MiHomeDevice.status_command(cmd)
        
class MyMiHomeDevice(ABC):
    def __init__(self, ip , token) -> None:
        self._ip = ip
        self._token = token
    
    @abstractclassmethod
    def get_power_status(self):
        print("status_check_not_impl")
    
    @abstractclassmethod
    def status_command(self, cmd:str):
        print("status_comand_not_impl")
    
class MyYeelight(MyMiHomeDevice):
    def __init__(self, ip, token) -> None:
        super().__init__(ip, token)
        self.yeelight = Yeelight(ip=self._ip, token=self._token)

    def get_power_status(self):
        status:YeelightStatus =self.yeelight.status()
        return "on" if status.is_on else "off"
    
    def status_command(self, cmd:str):
        if cmd == "on":
            self.action_turn_on()
        elif cmd == "off":
            self.action_turn_off()


    def action_turn_off(self):
        self.yeelight.off()

    def action_turn_on(self):
        self.yeelight.on()