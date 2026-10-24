import threading
from collections import deque

class KeyValueStore:
    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()
    
    def put(self, key, value):
        with self.lock:
            self.data[key] = value

    def get(self, key):
        with self.lock:
            return self.data.get(key)

class TaskQueue:
    def __init__(self):
        self.queue = deque()
        self.condition = threading.Condition()

    def enqueue(self, task):
        with self.condition:
            self.queue.append(task)
            self.condition.notify()

    def dequeue(self):
        with self.condition:
            while not self.queue:
                self.condition.wait()
            
            return self.queue.popleft()
