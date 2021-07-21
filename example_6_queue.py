import threading
import time
import queue

'''
Simulate a bread store
0.2 second produce a bread
0.5 second consume a bread
Maxmum storage is 100
'''
# maxmum storage
q = queue.Queue(maxsize=100)

def produce(q):
    """
    Produce fuction
    """
    for i in range(20):
        # produce bread & number is the ID
        q.put('{}th bread'.format(str(i)))
        # 0.2 second produce one
        time.sleep(0.2)
        

def consume(q):
    # only if store has bread
    while not q.empty():
        # q.qsize() is the total bread in store
        print('Total storage: '+str(q.qsize()))
        # q.get() is block, to get the bread from store
        print('Cosume: '+str(q.get()))
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
print(f"Total elapse: {end_time - start_time}")