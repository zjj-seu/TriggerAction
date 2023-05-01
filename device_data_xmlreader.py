
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
        

"""
{'317934913_cn': {'name': '台灯', 
                'did': '317934913', 
                'ip': '192.168.3.54', 
                'token': '9490458620e6604d712ccad862bc32b6', 
                'class': 'miio.integrations.yeelight.light.yeelight.Yeelight'}, 
'108412119_cn': {'name': '小爱音箱 万能遥控版', 
                'did': '108412119', 
                'ip': '192.168.3.64', 
                'token': '704e665a31787076614f354950436c6f'}, 
'ir.1543249323641991168_cn': {'name': '空调', 
                'did': 'ir.1543249323641991168', 
                'ip': None, 
                'token': None}, 
'127049371880428': {'did': '127049371880428', 
                'name': '博联智能插座', 
                'ip': '192.168.3.70', 
                'port': '80', 'mac': 
                '127049371880428', 
                'devtype': '30056', 
                'class': 'broadlink.switch.sp4'}}
"""



if __name__ == "__main__":
    
    filepathlist = {"mihome": Settings.mihome_devicefile_path, "broadlink": Settings.broadlink_devicefile_path}
    reader = AllBrandDeviceDataReader(filepathlist)
    mylist = reader.get_local_device_list()
    print(mylist)
    