from threading import Lock

from xml_reader import XmlReader
from settings import Settings
from xml_updater import xmlUpdater

class EventDictAccess:
    def __init__(self, eventlist:dict) -> None:
        self.eventlist = eventlist
        self.lock = Lock()
        
    


class EventAccessController:
    def __init__(self, eventfilepath:str, event_raw_path:str, event_class_raw_path:str) -> None:
        self.eventfilepath = eventfilepath
        self.event_raw_path = event_raw_path
        event_class_raw_path = event_class_raw_path
        self.lock = Lock()
        
    def get_event_list(self):
        with self.lock:
            fetcher = EventFetcher(self.eventfilepath, self.event_raw_path)
            return fetcher.get_event_list()
        
    def update_event(self,new_event:dict):
        """
        'id': '001', 'name': 'save energy', 'status': 'on', 
                'eventdetails': {'trigger': {'type': 'status', 
                                            'id': '001101',
                                            'targetdevicedid': '317934913', 
                                            'targetstatus': 'on', 
                                            'targetdevicename': '台灯'}, 
                                'conditions': {'001201': {'type': 'time', 
                                                    'id': '001201', 
                                                    'targettimefrom': '18:00', 
                                                    'targettimeto': '18:10'}}, 
                                'actions': {'001301': {'type': 'status', 
                                                'id': '001301', 
                                                'targetdevicedid': '317934913', 
                                                'targetstatus': 'off', 
                                                'targetdevicename': '台灯'}}}
        """
        with self.lock:
            xmlupdater = xmlUpdater(self.eventfilepath)
        
        
        branch_node_dict = {"tag": "event"}
        branch_node_dict["id"] = new_event["id"]
        branch_node_dict["name"] = new_event["name"]
        branch_node_dict["status"] = new_event["status"]
        
        new_branch = xmlupdater.create_Element(branch_node_dict)
        
        for key, value in new_event["eventdetails"].items():
            if key == "trigger":
                trigger_node_dict = {"tag":"trigger"}
                trigger_node_dict["id"] = value.pop("id")
                trigger_node_dict["type"] = value.pop("type")
                trigger_node = xmlupdater.create_Element(trigger_node_dict)

                xmlupdater.add_SubElements(trigger_node, value)
                xmlupdater.add_selected_SubElement(new_branch, trigger_node)
            if key == "conditions":
                ConditionS_dict = {"tag":"conditions"}
                ConditionS_node = xmlupdater.create_Element(ConditionS_dict)
                
                for condition_id, condition_value in value.items():
                    condition_node_dict = {"tag":"condition"}
                    condition_node_dict["id"] = condition_value.pop("id")
                    condition_node_dict["type"] = condition_value.pop("type")
                    condition_node = xmlupdater.create_Element(condition_node_dict)
                    
                    xmlupdater.add_SubElements(condition_node, condition_value)
                    xmlupdater.add_selected_SubElement(ConditionS_node, condition_node)
                    
                xmlupdater.add_selected_SubElement(new_branch, ConditionS_node)
                
            if key == "actions":
                ActionS_dict = {"tag":"actions"}
                AcitonS_node = xmlupdater.create_Element(ActionS_dict)
                
                for action_key, action_value in value.items():
                    action_node_dict = {"tag":"action"}
                    action_node_dict["id"] = action_value.pop("id")
                    action_node_dict["type"] = action_value.pop("type")
                    action_node = xmlupdater.create_Element(action_node_dict)
                    
                    xmlupdater.add_SubElements(action_node, action_value)
                    xmlupdater.add_selected_SubElement(AcitonS_node, action_node)
                
                xmlupdater.add_selected_SubElement(new_branch, AcitonS_node)
                
        
        with self.lock:
            xmlupdater.add_to_tree_and_save(new_branch)
            xmlupdater.save_to_files()
        
        
                    
        
        pass

class EventFetcher():
    def __init__(self, event_file_path, eventraw_file_path):
        self.event_file_path = event_file_path
        self.eventraw_file_path = eventraw_file_path

        self.event_raw_root = XmlReader(self.eventraw_file_path, "types").get_root()
        self.event_root = XmlReader(self.event_file_path, "events").get_root()

    def get_event_list(self):
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
        

        # 根据元数据获取事件
        """
        本项目事件集合采用字典嵌套的树形结构
        eg.
        {'001': {'id': '001', 'name': 'save energy', 'status': 'off', 
        'eventdetails': {'trigger': {'type': 'status', 
                                    'id': '001101', 
                                    'targetdevicedid': '317934913_cn', 
                                    'targetstatus': 'on', 
                                    'targetdevicename': '台灯'}, 
                        'conditions': {'001201': {'type': 'time', 
                                                'id': '001201', 
                                                'targettimefrom': '18:00', 
                                                'targettimeto': '18:10'}}, 
                        'actions': {'001301': {'type': 'status', 
                                                'id': '001301', 
                                                'targetdevicedid': '317934913_cn', 
                                                'targetstatus': 'off', 
                                                'targetdevicename': '台灯'}}}}, 
        '002': {'id': '002', 'name': 'save energy', 'status': 'on', 
        'eventdetails': {'trigger': {'type': 'status', 
                                    'id': '002101', 
                                    'targetdevicedid': '317934913_cn', 
                                    'targetstatus': 'off', 
                                    'targetdevicename': '台灯'}, 
                        'conditions': {'002201': {'type': 'status', 
                                                'id': '002201', 
                                                'targetdevicedid': '127049371880428', 
                                                'targetstatus': 'on', 
                                                'targetdevicename': '博联智能插座'}}, 
                        'actions': {'002301': {'type': 'status', 
                                                'id': '002301', 
                                                'targetdevicedid': '127049371880428', 
                                                'targetstatus': 'off', 
                                                'targetdevicename': '博联智能插座'}}}}}
        
        """
        total_events = dict()
        for child in self.event_root:
            print(str(child.tag)+"\t"+str(child.attrib))
            event_id = child.attrib["id"]
            event_name = child.attrib["name"]
            event_status = child.attrib["status"]

            event = dict()
            eventdetails = dict()
            total_events[event_id] = event

            event["id"] = event_id
            event["name"] = event_name
            event["status"] = event_status
            event["eventdetails"] = eventdetails

            for grandchild in child:
                if grandchild.tag == "trigger":
                    trigger_type = grandchild.attrib["type"]
                    trigger_id = grandchild.attrib["id"]
                    trigger_details_dict = dict()
                    trigger_details_dict["type"] = trigger_type
                    trigger_details_dict["id"] = trigger_id
                    for key, value in eventraw_list[trigger_type].items():
                        trigger_details_dict[value] = grandchild.find(value).text

                    eventdetails["trigger"] = trigger_details_dict
                elif grandchild.tag == "conditions":
                    conditions_dict = dict()
                    for grandgrandchild in grandchild:
                        condition_type = grandgrandchild.attrib["type"]
                        condition_id = grandgrandchild.attrib["id"]
                        condition_details_dict = dict()
                        condition_details_dict["type"] = condition_type
                        condition_details_dict["id"] = condition_id
                        for key,value in eventraw_list[condition_type].items():
                            condition_details_dict[value] = grandgrandchild.find(value).text
                        
                        conditions_dict[grandgrandchild.attrib["id"]] = condition_details_dict
                    
                    eventdetails["conditions"] = conditions_dict
                elif grandchild.tag == "actions":
                    actions_dict = dict()
                    for grandgrandchild in grandchild:
                        action_type = grandgrandchild.attrib["type"]
                        action_id = grandgrandchild.attrib["id"]
                        action_details_dict = dict()
                        action_details_dict["type"] = action_type
                        action_details_dict["id"] = action_id
                        for key,value in eventraw_list[action_type].items():
                            action_details_dict[value] = grandgrandchild.find(value).text
                        
                        actions_dict[grandgrandchild.attrib["id"]] = action_details_dict
                    
                    eventdetails["actions"] = actions_dict

        return total_events
        
                
def main():
    eventfetcher = EventFetcher(Settings.event_path,Settings.eventraw_path)
    total_events = eventfetcher.get_event_list()
    print(total_events)

    pass

def test_for_add():
    new_event = {'id': '002', 'name': 'save energy', 'status': 'on', 
        'eventdetails': {'trigger': {'type': 'status', 
                                    'id': '002101', 
                                    'targetdevicedid': '317934913_cn', 
                                    'targetstatus': 'off', 
                                    'targetdevicename': '台灯'}, 
                        'conditions': {'002201': {'type': 'status', 
                                                'id': '002201', 
                                                'targetdevicedid': '127049371880428', 
                                                'targetstatus': 'on', 
                                                'targetdevicename': '博联智能插座'}}, 
                        'actions': {'002301': {'type': 'status', 
                                                'id': '002301', 
                                                'targetdevicedid': '127049371880428', 
                                                'targetstatus': 'off', 
                                                'targetdevicename': '博联智能插座'}}}}
    
    adder = EventAccessController(Settings.test_event_path, Settings.eventraw_path, Settings.eventclassraw_path)
    adder.update_event(new_event)

if __name__ == "__main__":
    test_for_add()