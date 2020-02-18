from concurrent.futures import ThreadPoolExecutor
from threading import Lock as ThreadLock
from multiprocessing import Process, Value as ProcessValue, Lock as ProcessLock
from time import time


class ProcessCounter:
    def __init__(self):
        self.value = ProcessValue('i', 0)
        self.lock = ProcessLock()

    def function(self, arg):
        for i in range(arg):
            self.increment()

    def increment(self):
        with self.lock:
            self.value.value += 1

    def get_value(self):
        with self.lock:
            return self.value.value


class ThreadCounter:
    def __init__(self):
        self.value = 0
        self.lock = ThreadLock()
        self.delta_time = 0

    def function(self, arg):
        start_time = time()
        for i in range(arg):
            self.increment()
        end_time = time()
        self.delta_time= end_time - start_time

    def increment(self):
        with self.lock:
            self.value += 1

    def get_value(self):
        with self.lock:
            return self.value

    def get_time(self):
        return "time: {}".format(self.delta_time)


def start_process_counter():
    counter = ProcessCounter()
    processes = [Process(target=counter.function, args=(1000000, )) for i in range(5)]
    start_time = time()
    [process.start() for process in processes]
    [process.join() for process in processes]
    end_time = time()
    print("""ProcessCounter
        a = {}
        time: {}""".format(counter.get_value(), end_time - start_time))
    print("-" * 80)


def start_thread_counter():
    counter = ThreadCounter()
    with ThreadPoolExecutor(max_workers=5) as executor:
        for index in range(5):
            executor.submit(counter.function, 1000000)
    print("""ThreadCounter
    a = {}
    time: {}""".format(counter.get_value(), counter.get_time()))
    print("-"*80)


if __name__ == '__main__':
    start_process_counter()
    start_thread_counter()
