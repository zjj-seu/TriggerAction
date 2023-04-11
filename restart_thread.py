from threading import Thread


class MyThread:
    def __init__(self, target, *args):
        
        self.running = False
        self.target = target
        self.args = args

    def start(self):
        Thread(target=self.target, args=self.args).start()

