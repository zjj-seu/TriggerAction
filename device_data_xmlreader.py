
from threading import Lock

from settings import Settings
from xml_reader import XmlReader

class miio_DeviceDataXmlReader(XmlReader):
    def __init__(self, file_path, default_root_name = "devices"):
        self.file_path = file_path

        super().__init__(file_path, default_root_name)

    def get_device_list(self):
        root = super().get_root()
        device_list = {}
        # 遍历XML文件
        for child in root:
            # print(str(child.tag)+"\t"+str(child.attrib))
            did = child.attrib["id"]
            deviceInfo = {}
            for grandchild in child:
                # print(str(grandchild.tag)+"\t"+str(grandchild.attrib)+"\t"+str(grandchild.text))
                deviceInfo[grandchild.tag] = grandchild.text
            device_list[did] = deviceInfo

        return device_list
    
class broadlink_DeviceDataXmlReader(XmlReader):
    def __init__(self, file_path, default_root_name = "devices"):
        self.file_path = file_path

        super().__init__(file_path, default_root_name)
    
    def get_device_list(self):
        root = super().get_root()
        device_list = {}
        # 遍历XML文件
        for child in root:
            # print(str(child.tag)+"\t"+str(child.attrib))
            did = child.attrib["id"]
            deviceInfo = {}
            for grandchild in child:
                # print(str(grandchild.tag)+"\t"+str(grandchild.attrib)+"\t"+str(grandchild.text))
                deviceInfo[grandchild.tag] = grandchild.text
            device_list[did] = deviceInfo

        return device_list

class AllBrandDeviceDataReader:
    def __init__(self,filepathlist:dict) -> None:
        self.filepathlist = filepathlist
        self.lockforfiles = Lock()

    def get_local_device_list(self):
        devicelist = dict()
        with self.lockforfiles:
            for brand, path in self.filepathlist.items():
                if brand == "mihome":
                    mireader = miio_DeviceDataXmlReader(path)
                    devices = mireader.get_device_list()
                    devicelist.update(devices)
                elif brand == "broadlink":
                    broadlinkreader = broadlink_DeviceDataXmlReader(path)
                    devices = broadlinkreader.get_device_list()
                    devicelist.update(devices)
                    
        return devicelist
        

    



if __name__ == "__main__":
    reader = miio_DeviceDataXmlReader("data_files/device_data_broadlink.xml")
    mylist = reader.get_device_list()
    print(mylist)
    