import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

from xml_reader import XmlReader


# 更新xml文件的通用类
# 功能1：create_Element:创建一个节点，指定tag和attrib,tag和attrib存在同一个字典里
# 功能2：add_SubElements为指定节点创建数个子节点，数个子节点name和text存储在同一个字典里
# 功能3：add_selected_SubElement:连接两个节点的从属关系

class xmlUpdater:
    def __init__(self, filepath:str) -> None:
        self._filepath = filepath
        xmlreader = XmlReader(filepath, "events")
        
        self._tree = ET.parse(filepath)
        self._root = self._tree.getroot()

    def create_Element(self, data_dict:dict):
        new_element = ET.Element(data_dict['tag'])

        for key, value in data_dict.items():
            if key == "tag":
                continue
            new_element.set(key,value)

        return new_element

    def add_SubElements(self,fathernote:ET.Element,children:dict):
        for key, value in children.items():
            subelement = ET.SubElement(fathernote,key)
            subelement.text = value

    # TODO 未测试
    def add_selected_SubElement(self,fathernode:ET.Element,childrennode:ET.Element):
        fathernode.append(childrennode)


    def add_to_tree_and_save(self, element:ET.Element):
        self._root.append(element)

        # 将XML树写入内存中
        xml_str = ET.tostring(self._root)

        # 使用minidom模块进行格式化输出，并过滤掉空行,md gpt终于给了一个能用的操作了
        xml_str = minidom.parseString(xml_str).toprettyxml(indent='\t')
        xml_str = '\n'.join([line for line in xml_str.split('\n') if line.strip()])

        # 将格式化后的XML字符串写入文件
        with open(self._filepath, 'w', encoding='utf-8') as f:
            f.write(xml_str)

    def save_to_files(self):
        # 将XML树写入内存中
        xml_str = ET.tostring(self._root)

        # 使用minidom模块进行格式化输出，并过滤掉空行,md gpt终于给了一个能用的操作了
        xml_str = minidom.parseString(xml_str).toprettyxml(indent='\t')
        xml_str = '\n'.join([line for line in xml_str.split('\n') if line.strip()])

        # 将格式化后的XML字符串写入文件
        with open(self._filepath, 'w', encoding='utf-8') as f:
            f.write(xml_str)

    def insert_new_or_update_data(self,new_node:ET.Element):
        root = self._root
        # 遍历 root 的子孙结点
        for node in root.iter():
            # 检查结点是否与新结点具有相同的 tag
            if node.tag == new_node.tag:
                # 检查结点的所有属性是否相同
                if node.attrib["id"] == new_node.attrib["id"]:
                    # 检查结点的文本内容是否相同
                    if node.text == new_node.text:
                        # 如果结点相同，则什么都不需要做
                        return
                    else:
                        # 删除结点的所有子元素
                        node.clear()
                        node.set("id", new_node.attrib["id"])
                        node.set("name", new_node.attrib["name"])
                        node.set("status", new_node.attrib["status"])
                        # 将新结点的子元素添加到该结点中
                        for child in new_node:
                            node.append(child)

                        return     
        
        # 如果没有找到相同的结点，则将新结点添加到 root 中
        root.append(new_node)
        
    



def main():
    xmlmanager = xmlUpdater("data_files/example.xml")
    element =  xmlmanager.create_Element({"tag":"book", "name":"mybook","id":"5"})
    book_data = {"name":"the last of US","year":"2014"}
    xmlmanager.add_SubElements(element,book_data)
    xmlmanager.insert_new_or_update_data(element)
    xmlmanager.save_to_files()



if __name__ == "__main__":
    main()