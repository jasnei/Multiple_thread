from multiprocessing import Lock, Process, Queue
import time
import random
import os


def consumer(q):
    while True:
        res = q.get()
        if res is None: break # End signal
        time.sleep(0.1)
        print('%s 吃 %s' % (os.getpid(), res))


def producer(q):
    for i in range(10):
        time.sleep(0.1)
        res = "包子%s" % i
        q.put(res)
        print('%s 生产了 %s' % (os.getpid(), res))
    # q.put(None) # send ending signal, also could be in send in main


if __name__ == "__main__":
    q = Queue()

    produce = Process(target=producer, args=(q,))

    consum = Process(target=consumer, args=(q,))

    produce.start()
    consum.start()

    produce.join()
    q.put(None)   # main send ending signal
    consum.join()