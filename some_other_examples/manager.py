# 进程间数据是独立的，可以借助于队列或管道实现通信，二者都是基于消息传递的
# 虽然进程间数据独立，但可以通过Manager实现数据共享，事实上Manager的功能远不止于此
from multiprocessing import Manager, Process, Lock


def work(d, lock):
    with lock: #不加锁而操作共享的数据,肯定会出现数据错乱
        d['count'] -= 1


if __name__ == '__main__':
    lock = Lock()
    with Manager() as m:
        dic = m.dict({'count': 1000})
        p_l = []
        for _ in range(1000):
            p = Process(target=work, args=(dic, lock))
            p_l.append(p)
            p.start()
        for p in p_l:
            p.join()
        print(dic)
        #{'count': 94}
