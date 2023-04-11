import xml_reader as xml_reader
import os
import xml.etree.ElementTree as ET

class miio_DeviceDataXmlReader(xml_reader.XmlReader):
    def __init__(self, file_path):
        self.file_path = file_path

        if not self.check_file_exists():
            self.create_file_with_miio_device_root()

        super().__init__(file_path, "devices")

    def check_file_exists(self):
        """
        Checks if the file exists at the specified path
        """
        return os.path.exists(self.file_path)

    def create_file_with_miio_device_root(self, root_tag:str = "devices"):
        """
        Creates an XML file with the given root element at the specified path
        """
        if self.check_file_exists():
            print(f"Error: File {self._file_path} already exists.")
            return

        root = ET.Element()
        root.tag = root_tag
        tree = ET.ElementTree(root)
        tree.write(self.file_path)
        print(f"Successfully created file {self.file_path}")

    def get_device_list(self):
        root = super().get_root()
        device_list = {}
        # 遍历XML文件
        for child in root:
            print(str(child.tag)+"\t"+str(child.attrib))
            did = child.attrib["id"]
            deviceInfo = {}
            for grandchild in child:
                print(str(grandchild.tag)+"\t"+str(grandchild.attrib)+"\t"+str(grandchild.text))
                deviceInfo[grandchild.tag] = grandchild.text
            device_list[did] = deviceInfo

        return device_list



if __name__ == "__main__":
    reader = miio_DeviceDataXmlReader("data_files/device_data.xml")
    reader.get_device_list()
    