import broadlink# 用设备的IP地址、MAC地址和设备类型创建设备对象
import time

devices = broadlink.discover()
print(devices)
for a in devices:
    print(a.__class__.__module__ + a.__class__.__name__)


device = broadlink.switch.sp4(host=('192.168.3.70', 80), mac=b'\xec\x0b\xae\xfc\x8c\x73', devtype=30056)

# 连接到设备，并进行身份验证
device.auth()

print(device.ke)

# 打开SP4智能插座，并保持开启5秒钟
device.set_power(False)
time.sleep(5)

# 关闭SP4智能插座
device.set_power(True)
