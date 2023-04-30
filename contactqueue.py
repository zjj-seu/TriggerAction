from threading import Lock

class ContactQueue:
    def __init__(self) -> None:
        self.lock = Lock()
        self.queue = dict()