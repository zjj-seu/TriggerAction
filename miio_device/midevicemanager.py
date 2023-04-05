from micloudconnector import MiCloudConnector



class DeviceInfoProcessor:
    def __init__(self, raw_device_list:dict) -> None:
        self._raw_device_list = raw_device_list

    def get_dict_with_selected_keys(self, keys_list:list):
        my_device_list = {}

        for did, miclouddeviceInfo in self._raw_device_list.items():
            mydeviceInfo = {}
            for key in keys_list:
                if hasattr(miclouddeviceInfo,key):
                    """
                    if key == "name":
                        mydeviceInfo[key] = self.gbk_to_utf8(getattr(miclouddeviceInfo, key))
                    else:
                        mydeviceInfo[key] = getattr(miclouddeviceInfo, key)
                    """
                    attr = getattr(miclouddeviceInfo, key)
                    if attr == "":
                        attr = None
                    mydeviceInfo[key] = attr
                    print(f"processed attr named {key},value:{mydeviceInfo[key]}")
                else:
                    print(f"can't find the attr named {key}")

            my_device_list[did] = mydeviceInfo

        return my_device_list
    
    def gbk_to_utf8(self, name:str):
        gbk_str = name
        utf8_str = gbk_str.decode('gbk').encode('utf-8')
        return utf8_str
            

class MiDeviceManager:
    def __init__(self, miConnector:MiCloudConnector) -> None:
        self._miConnector = miConnector
        self._device_dict = self._miConnector._cloud_interface.get_devices()

    
    def get_devicelist(self):
        # dict{device_id(str):CloudDeviceInfo(class)}
        return self._device_dict
    
    def get_processed_devicelist(self, keys_list:list = ["name","did","ip","token"]):
        processor = DeviceInfoProcessor(self._device_dict)
        return processor.get_dict_with_selected_keys(keys_list)


    
    def get_ip_token_with_name(self,name:str):

        for did, dev in self._device_dict.items():
            if dev.name == name:
                return dev.ip, dev.token
        
        return None, None
            
    def get_ip_token_with_did(self,given_did:str):
        for did, dev in self._device_dict.items():
            if did == given_did:
                return dev.ip, dev.token
        
        return None, None

    @property
    def devices_count(self):
        if self._miConnector._cloud_interface!= None:
            return len(self._device_dict)
        else:
            print("未成功连接到小米服务器")