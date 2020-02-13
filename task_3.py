from threading import Thread, Lock

a = 0
thread_lock = Lock()

def function(arg):
    with thread_lock:
        global a
        for _ in range(arg):
            a += 1


def main():
    threads = []
    for i in range(5):
        thread = Thread(target=function, args=(1000000,))
        thread.start()
        threads.append(thread)

    [t.join() for t in threads]
    print("----------------------", a)  # ???


main()
