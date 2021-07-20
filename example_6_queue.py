import threading
import time
import queue

'''
模拟包子店卖包子
厨房每一秒钟制造一个包子
顾客每三秒吃掉一个包子
厨房一次性最多存放100个包子
'''
q = queue.Queue(maxsize=100)
# 厨房一次性最多存放100个包子

def produce(q):
    # 这个函数专门产生包子
    for i in range(20):
        # 生产出包子，表明包子的id号
        q.put('第{}个包子'.format(str(i)))
        # 要0.2秒才能造出一个包子
        time.sleep(0.2)
        

def consume(q):
    # 只要包子店里有包子
    while not q.empty():
        # q.qsize()是获取队列中剩余的数量
        print('包子店的包子剩余量：'+str(q.qsize()))
        # q.get()是一个堵塞的，会等待直到获取到数据
        print('小桃红吃了:'+str(q.get()))
        print('-'*20)
        time.sleep(0.5)

start_time = time.time()
t1 = threading.Thread(target=produce,args=(q,))
t2 = threading.Thread(target=consume,args=(q,))
t1.start()
t2.start()
t1.join()
t2.join()
end_time = time.time()
print(f"消耗时间为：{end_time - start_time}")