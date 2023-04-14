from abc import ABC, abstractmethod

class DeviceController(ABC):

    @abstractmethod
    def get_status(self):
        pass