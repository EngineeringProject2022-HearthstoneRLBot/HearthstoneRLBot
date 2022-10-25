import threading
from threading import Thread
from time import sleep

import waiting


class Producer(Thread):
    def __init__(self):
        super().__init__()
        self.queue = [0]*10
        self.output = [0]*10
        self.factor = 1
        self.lock = threading.Condition()
        self.readLock = threading.Lock()
    def insert(self, i, value):
        self.queue[i] = value
    def waitForEval(self):
        print('Producing out of ', self.queue)
        sleep(5)
        self.queue = [0]*10
        self.output = list(range(0,10*self.factor, 1*self.factor))
        self.factor*=2
        print('Produced output of ', self.output)

    def get(self, i):
        with self.lock:
            self.lock.wait()
            a = self.output[i]
            self.output[i] = 0
            return a
    def run(self):
        while True:
            waiting.wait(lambda: sum(self.queue) == 10)
            self.lock.acquire()
            self.waitForEval()
            self.lock.notify_all()
            self.lock.release()

class Worker(Thread):
    def __init__(self, prod, v):
        super().__init__()
        self.prod = prod
        self.i = v
    def run(self):
        while True:
            self.prod.insert(self.i, 1)
            value = self.prod.get(self.i)
            print(f'Worker {self.i} continuing to work, got value of {value}')
global b
b = Producer()
b.start()
for wid in range(10):
    w = Worker(b, wid)
    w.start()

b.join()




