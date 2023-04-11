from miio.integrations.yeelight.light.yeelight import Yeelight,YeelightStatus


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