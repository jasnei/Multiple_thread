from multiprocessing import Process, JoinableQueue
import time
import os


def producer(name, q):
    for i in range(2):
        time.sleep(0.1)
        res = "%s-%s" % (name, i)
        q.put(res)
        print('%s 生产了 %s' % (os.getpid(), res))
    # q.put(None) # send ending signal, also could be in send in main


def consumer(q):
    while True:
        res = q.get()
        if res is None:
            break  # End signal
        time.sleep(0.1)
        print('%s 吃 %s' % (os.getpid(), res))


if __name__ == "__main__":
    q = JoinableQueue()

    p1 = Process(target=producer, args=("Bread", q))
    p2 = Process(target=producer, args=("Honey", q))
    p3 = Process(target=producer, args=("Duck", q))

    c1 = Process(target=consumer, args=(q,))
    c2 = Process(target=consumer, args=(q,))
    c1.daemon = True
    c2.daemon = True

    produce = [p1, p2, p3, c1, c2]
    for p in produce:
        p.start()

    p1.join()  # 必须保证生产者全部生产完毕,才应该发送结束信号
    p2.join()
    p3.join()

    # 主进程等--->p1, p2, p3 等---->c1, c2
    # p1, p2, p3结束了，证明c1, c2肯定全都收完了p1, p2, p3发到队列的数据
    # 因而c1, c2也没有存在的价值了，应该随着主进程的结束而结束，所以设置成守护进程
    # 结果也只会每个消费线程只产生一次消费
