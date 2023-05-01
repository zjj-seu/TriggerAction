from xml_reader import XmlReader
from threading import Lock

class EventRawFileXmlReader(XmlReader):
    def __init__(self, file_path, default_root_name = "types"):
        super().__init__(file_path, default_root_name)
        self.lock = Lock()
        self.event_raw_root = None
        
    def get_event_raw_dict(self):
        with self.lock:
            self.event_raw_root = super().get_root()
          
        
        eventraw_list = dict()

        # 获取元数据字典
        # eg.
        # eventraw_list{
        #   status(type):{param1:"targetdevicedid", param2:"targetstatus", param3:"targetdevicename"}
        #   time(type):{param1:"targettime"} 
        # }
        for child in self.event_raw_root:
            print(str(child.tag)+"\t"+str(child.attrib))
            type = child.attrib["name"]
            paramlist = dict()
            for grandchild in child:
                print(str(grandchild.tag)+"\t"+str(grandchild.attrib)+"\t"+str(grandchild.text))
                paramlist[grandchild.tag + grandchild.attrib["id"]] = grandchild.text
            eventraw_list[type] = paramlist
            
        return eventraw_list
        
    
class ClassRawFileXmlReader(XmlReader):
    def __init__(self, file_path, default_root_name = "classes"):
        super().__init__(file_path, default_root_name)
        self.lock = Lock()
        self.class_raw_root = None
        
    def get_class_raw_dict(self):
        with self.lock:
            self.class_raw_root = super().get_root()
            
        class_raw_list = dict()
        
        for child in self.class_raw_root:
            class_name = child.attrib["name"]
            paramdict = dict()
            for grandchild in child:
                paramdict[grandchild.tag + grandchild.attrib["id"]] = grandchild.text
            class_raw_list[class_name] = paramdict
        
        return class_raw_list