import sys
import time
import threading

def loop():
    """
    Define a loop
    """
    l.acquire()
    # threading.current_thread().name is threading name, you could define yourself
    print(f'thread {threading.current_thread().name} is running...' )
    
    n = 0
    while n < 10:
        n = n + 1
        print(f'{threading.current_thread().name} >>> {n}')
    print(f'thread {threading.current_thread().name} ended.' )
    l.release()
print(f'thread {threading.current_thread().name} is running...')

#================= Thread core usage ==============================================
#======== including target name which is your function name, args is function args
t = threading.Thread(target=loop, name='Thread_name:')
# Lock
l = threading.Lock()
t.start()
t.join()
print('thread %s ended.' % threading.current_thread().name)