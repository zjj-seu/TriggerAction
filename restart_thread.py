# 适用于需要反复启动线程检查某个状态的事件，由于python线程不能多次启动

from threading import Thread


class MyThread:
    def __init__(self, target, *args):
        
        self.running = False
        self.target = target
        self.args = args

    def start(self):
        Thread(target=self.target, args=self.args).start()

