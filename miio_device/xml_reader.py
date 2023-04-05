import xml.etree.ElementTree as ET

class XmlReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.root = None
        self.parse_xml()

    def parse_xml(self):
        tree = ET.parse(self.file_path)
        self.root = tree.getroot()

    def get_root(self):
        return self.root
