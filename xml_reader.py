import xml.etree.ElementTree as ET
import os

class XmlReader:
    def __init__(self, file_path, default_root_name):
        self.default_root_name = default_root_name
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            self.create_file_with_given_root()

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
        root = ET.Element()
        root.tag = self.default_root_name
        tree = ET.ElementTree(root)
        tree.write(self.file_path)
        print(f"Successfully created file {self.file_path}")