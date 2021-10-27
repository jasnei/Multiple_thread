from queue import Queue
from threading import Lock, Thread
import time

my_queue = Queue(1)

def consumer():
    print('Consumer waiting')
    time.sleep(0.1)
    my_queue.get()
    print('Consumer got 1')
    my_queue.get()
    print('Consumer got 2')
    my_queue.task_done()
    print('Consumer done')

thread = Thread(target=consumer)
thread.start()

print('Producer putting')
my_queue.put(object())
print('Producer put 1')
my_queue.put(object())
print('Producer put 2')
print('Producer done')
thread.join()