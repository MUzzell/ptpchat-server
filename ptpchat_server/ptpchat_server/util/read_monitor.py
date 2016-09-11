import threading

class ReadMonitor:

    def __init__(self):
        self.count = 0

        self.write_cond = threading.Condition()

    def start_read(self):
        self.write_cond.acquire()
        self.count += 1
        self.write_cond.release()

    def end_read(self):
        self.write_cond.acquire()
        self.count -= 1
        if self.count == 0:
            self.write_cond.notify()
        self.write_cond.release()

    def start_write(self):

        self.write_cond.acquire()
        while not self.count == 0:
            self.write_cond.wait(0.5)

    def end_write(self):
        self.write_cond.notify()
        self.write_cond.release()

    def write(self):
        return WriteMonitor(self)

    def read(self):
        return ReadMonitor(self)

class WriteMonitor:
    def __init__(self, monitor):
        self.monitor = monitor

    def __enter__(self):
        self.monitor.start_write()

    def __exit__(self):
        self.monitor.end_write()

class ReadMonitor:
    def __init__(self, monitor):
        self.monitor = monitor

    def __enter__(self):
        self.monitor.start_read()

    def __exit__(self):
        self.monitor.end_read()

def read(monitor):

    def read_wrapper(func):
        monitor.start_read()
        func()
        monitor.end_read()
    return read_wrapper

def write(monitor):

    def write_wrapper(func):
        monitor.start_write()
        func()
        monitor.end_write()
    return write_wrapper


