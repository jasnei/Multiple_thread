from multiprocessing import Lock, Process
import time, json, random

"""可以用Queue改写"""

def search():
    data = json.load(open(r"some_other_examples\data\db.txt"))
    # \033[43m *** \033[0m is for the font background color
    print('剩余票数%s' %data['count'])

def get():
    data = json.load(open(r"some_other_examples\data\db.txt"))
    time.sleep(0.1) # simulate internet delay
    if data['count'] > 0:
        data['count'] -= 1
        time.sleep(0.2) # simulate write data delay
        json.dump(data, open(r"some_other_examples\data\db.txt", "w"))
        print("购票成功")
    else:
        print("购票失败")

def task(lock):
    search()
    lock.acquire()
    get()
    lock.release()


if __name__ == "__main__":
    lock = Lock()
    for i in range(100):
        p = Process(target=task, args=(lock, ))
        p.start()
    # search()

    """
    加锁可以保证多个进程修改同一块数据时，同一时间只能有一个任务可以进行修改，即串行的修改，没错，速度是慢了，但牺牲了速度却保证了数据安全。
    虽然可以用文件共享数据实现进程间通信，但问题是：
    1.效率低（共享数据基于文件，而文件是硬盘上的数据）
    2.需要自己加锁处理

    #因此我们最好找寻一种解决方案能够兼顾：
    1、效率高（多个进程共享一块内存的数据）
    2、帮我们处理好锁问题。这就是mutiprocessing模块为我们提供的基于消息的IPC通信机制：队列和管道。

    1 队列和管道都是将数据存放于内存中
    2 队列又是基于（管道+锁）实现的，可以让我们从复杂的锁问题中解脱出来，
    我们应该尽量避免使用共享数据，尽可能使用消息传递和队列，避免处理复杂的同步和锁问题，而且在进程数目增多时，往往可以获得更好的可获展性。
    """
