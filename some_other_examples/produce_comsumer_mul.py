from multiprocessing import Process, Queue
import time
import os


def producer(name, q):  # sourcery skip: replace-interpolation-with-fstring
    for i in range(3):
        time.sleep(0.1)
        res = "%s-%s" %(name, i)
        q.put(res)
        print('%s 生产了 %s' % (os.getpid(), res))
    # q.put(None) # send ending signal, also could be in send in main


def consumer(q):  # sourcery skip: replace-interpolation-with-fstring
    while True:
        res = q.get()
        if res is None: break # End signal
        time.sleep(0.1)
        print('%s 吃 %s' % (os.getpid(), res))


if __name__ == "__main__":
    q = Queue()

    p1 = Process(target=producer, args=("Bread", q))
    p2 = Process(target=producer, args=("Honey", q))
    p3 = Process(target=producer, args=("Duck", q))

    c1 = Process(target=consumer, args=(q,))
    c2 = Process(target=consumer, args=(q,))

    p1.start()
    p2.start()
    p3.start()
    c1.start()
    c2.start()

    p1.join() #必须保证生产者全部生产完毕,才应该发送结束信号
    p2.join()
    p3.join()
    q.put(None) #有几个消费者就应该发送几次结束信号None
    q.put(None) #发送结束信号