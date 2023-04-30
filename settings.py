from threading import Lock


class Settings:
    username = "18305258602"
    password = "zjj139736672"

    mihome_devicefile_path = "D:/python_env/newTriggerAction/data_files/device_data_mihome.xml"
    broadlink_devicefile_path = "D:/python_env/newTriggerAction/data_files/device_data_broadlink.xml"
    event_path = "D:/python_env/newTriggerAction/data_files/event.xml"
    eventraw_path = "D:/python_env/newTriggerAction/data_files/eventraw.xml"
    eventclassraw_path = "D:/python_env/mytriggeraction/TriggerAction/data_files/eventclassraw.xml"
    
    test_event_path = "D:/python_env/newTriggerAction/data_files/example.xml"

    event_decode_interval_sec = 3
    trigger_listening_interval_sec = 0.01
    device_data_check_interval_sec = 0.01
    device_server_queue_check_interval_sec = 5
    event_data_update_interval_sec = 1

    broadlink_ssid = "18305258602"
    broadlink_pass = "zjj139736672"
    
    broadlink_device_dict_cache = dict()
    lock_for_broadlink_device_dict_cache = Lock()