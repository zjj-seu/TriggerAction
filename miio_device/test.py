from miio.cloud import CloudInterface
from miio.devicefactory import DeviceFactory
from miio.integrations.yeelight.light.yeelight import Yeelight

# 用户名和密码
username = '18305258602'
password = 'zjj139736672'

# 设备名称
device_name = '台灯'

# 登录云米账户
cloud_device = CloudInterface(username, password)

# 获取设备列表
devices = cloud_device.get_devices()

# 找到名为“YOUR_DEVICE_NAME”的设备
device_id = None
for did, dev in devices.items():
    if dev.name == device_name:
        device_id = did
        device_token = dev.token
        device_ip = dev.ip
        break

# 如果未找到设备，则退出程序
if device_id is None:
    print(f"No device named {device_name} found")
    exit()

# 获取设备的token
print(f"{device_name}'s device_token:{device_token}")
# 执行开灯操作
dev = Yeelight(ip=device_ip, token=device_token)
dev.on()

