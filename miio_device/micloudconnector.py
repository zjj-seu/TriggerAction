from miio.cloud import CloudInterface


class MiCloudConnector():
    def __init__(self, username:str, password:str) -> None:
        self._username = username
        self._password = password
        self._cloud_interface = None

    def connect_to_micloud(self):
        self._cloud_interface = CloudInterface(self._username, self._password)