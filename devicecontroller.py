from abc import ABC, abstractmethod

class DeviceController(ABC):

    @abstractmethod
    def get_status(self):
        print("[DeviceController] get_status_not_impl")
    
    @abstractmethod
    def status_action(self):
        print("[DeviceController] status_action_not_impl")