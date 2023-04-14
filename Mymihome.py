from devicecontroller import DeviceController

from miio.integrations.yeelight.light.yeelight import Yeelight,YeelightStatus



class MyMiHome(DeviceController):
    def __init__(self, devicedetails:dict) -> None:
        self.device_details = devicedetails
    
    def get_status(self):
        device_class:str = self.device_details["class"]
        if device_class.startswith("miio.integrations.yeelight.light.yeelight.Yeelight"):
            ip = self.device_details["ip"]
            token = self.device_details["token"]
            yeelight = MyYeelight(ip,token)
            return yeelight.get_power_status()
        

    
class MyYeelight:
    def __init__(self, ip , token) -> None:
        self._ip = ip
        self._token = token
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