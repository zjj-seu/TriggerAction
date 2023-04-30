import xml.etree.ElementTree as ET
import os

class XmlReader:
    def __init__(self, file_path, default_root_name):
        self.default_root_name = default_root_name
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            self.create_file_with_given_root()
            
        file_size = os.stat(file_path).st_size
        if file_size == 0:
            # 创建根节点为 events 的 XML 文件
            root = ET.Element(default_root_name)
            tree = ET.ElementTree(root)
            # 保存文件
            tree.write(file_path)
            print("Empty XML file detected. Added root tag 'events' and saved to file.")

        self.root = None
        self.parse_xml()

    def parse_xml(self):
        tree = ET.parse(self.file_path)
        self.root = tree.getroot()

    def get_root(self):
        return self.root

    def create_file_with_given_root(self):
        """
        Creates an XML file with the given root element at the specified path
        """
        root = ET.Element(self.default_root_name)
        tree = ET.ElementTree(root)
        tree.write(self.file_path,encoding='utf-8')
        print(f"Successfully created file {self.file_path}")