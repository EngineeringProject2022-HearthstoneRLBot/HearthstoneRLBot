import threading


class PrintQueue(threading.Thread):
    queue = []
    lock = threading.Lock()
    @staticmethod
    def add(msg):
        PrintQueue.lock.acquire(True)
        print(f'{threading.current_thread().name}: {msg}')
        PrintQueue.lock.release()