import threading
import time
import queue

que = queue.Queue(maxsize=5)

def t1(que):
    for i in range(10):
        que.put(i)
            
def t2(que):
    while not que.empty():
        # que.qsize() acquire how many data in queue
        print(f'How many data in queue: {que.qsize()}')
        
        # que.get() is blocking to get a data
        print(f'Got from queue: {que.get()}')
        
        print(f'-'*20)
        time.sleep(0.1)

t1 = threading.Thread(target=t1, args=(que, ))
t2 = threading.Thread(target=t2, args=(que, ))
t1.start()
t2.start()
t1.join()
t2.join()