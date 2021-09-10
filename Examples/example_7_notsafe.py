import threading
import random
import queue

q = queue.Queue(maxsize=100)

def produce(q):
    for i in range(20):
        result = str(random.randint(1,100))
        q.put(result)
        print('Generate a random number: '+result)
def consume(q):
    while not q.empty():
        res = q.get()
        print('I got the number you generate: '+str(res))

t1 = threading.Thread(target=produce, args=(q, ))
t2 = threading.Thread(target=consume, args=(q, ))
t1.start()
t2.start()