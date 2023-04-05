import os
import xml.etree.ElementTree as ET
from device_data_xmlreader import miio_DeviceDataXmlReader
from xml_updater import xmlUpdater
from miio.cloud import CloudDeviceInfo

# test
from micloudconnector import MiCloudConnector
from midevicemanager import MiDeviceManager
from settings import Settings

# the form of device date .xml files
"""
<?xml version="1.0" ?> 
<devices>
    <device id="(did)">
        <did>(did)</did>
        <name>(name)</name>
        <ip>(lan ipv4)</ip>
        <token>(device token)</token>
    </device>
    ...
</devices>
"""
class miio_DeviceDataUpdater:
    """
    A class for handling XML files
    """
    def __init__(self, file_path, device_list:dict):
        """
        Initializes the XmlFileHandler class with the given file path
        """
        self._file_path = file_path
        self._device_list = device_list

    def update_data(self):
        miio_xml_reader = miio_DeviceDataXmlReader(self._file_path)
        former_device_list = miio_xml_reader.get_device_list()
        if former_device_list == self._device_list:
            print("check exist miio devices over: no need to update")
        else:
            xmlupdater = xmlUpdater(self._file_path)
            for did, mydeviceInfo in self._device_list.items():

                element = xmlupdater.create_Element({"name":"device","id":did})
                xmlupdater.add_SubElements(element,mydeviceInfo)

                if did in former_device_list.keys():
                    if mydeviceInfo == former_device_list[did]:
                        print(f"check existed device having did:{did} whose infomation is no need to update")
                    else:
                        print(f"did difference {did}")
                        print(mydeviceInfo)
                        print(former_device_list[did])

                        #TODO 未测试
                        xmlupdater.insert_new_or_update_data(element)
                        # print(mydeviceInfo["name"])
                        print(f"check existed device having did:{did} whose infomation has been changed")
                else:
                    xmlupdater.insert_new_or_update_data(element)
                    print(f"No device having did:{did} whose infomation has been added")
            xmlupdater.save_to_files()



def test():
    # 用于测试能否自动获取局域网内的小米IoT设备并写入本地xml文件。
    connector = MiCloudConnector(Settings.username,Settings.password)
    connector.connect_to_micloud()
    manager = MiDeviceManager(connector)
    my_devicelist = manager.get_processed_devicelist()
    deviceUpdater = miio_DeviceDataUpdater(Settings.devicefile_path,my_devicelist)
    deviceUpdater.update_data()


if __name__ == "__main__":
    test()