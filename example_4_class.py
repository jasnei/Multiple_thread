import threading
import time

class mop_floor(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        print('I am going to mop the floor.')
        time.sleep(1)
        print('Floor mopped.')

class heat_up_watrt(threading.Thread):
    def __init__(self,name):
        # name is the arg of the sub thread name
        super().__init__(name=name)

    def run(self):
        print('I am going to boil some water.')
        # print thread name
        print(self.name)
        print(threading.current_thread().name)
        # 这两个都是打印出当前子线程的名字
        time.sleep(3)
        print('Water boiled.')

start_time = time.time()
t1 = mop_floor()
t2 = heat_up_watrt('***I am a water heater***')
t1.start()
t2.start()
t1.join()
t2.join()
end_time = time.time()
print('总共耗时:{}'.format(end_time-start_time))