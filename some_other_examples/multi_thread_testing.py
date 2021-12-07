import os
import numpy as np
import time
from multiprocessing import Process
from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from threading import Thread
from memory_profiler import profile

# Time calculator
class Benchmark:
    def __init__(self, text):
        self.text = text
    def __enter__(self):
        self.start = time.time()
    def __exit__(self, *args):
        self.end = time.time()
        print("%s: consume: %s" % (self.text, self.end - self.start))

# Base Task
def store_task(data: np.ndarray, output, index):
    fname = "%s_worker_%s.txt" % (output, index)
    # np.savetxt(fname, data, delimiter='\t')
    np.save(fname, data)

#main data source
worker_num = os.cpu_count()
big_data = np.random.rand(1000000, 10)
task_num = big_data.shape[0] // worker_num

# 1. multiprocessing.Porcess loop mp: consume: 11.032109022140503
@profile
def loop_mp():
    pool = []
    for i in range(worker_num):
        start = i * task_num
        end = (i+1) * task_num
        p = Process(target=store_task, args=(big_data[start: end], './data/mp_process', i))
        p.start()
        pool.append(p)
    for p in pool:
        p.join()

# 2. threading.Thread mt thread: consume: 0.03189706802368164
@profile
def mt_thread():
    pool = []
    for i in range(worker_num):
        start = i * task_num
        end = (i+1) * task_num
        t = Thread(target=store_task, args=(big_data[start: end], './data/thread', i))
        t.start()
        pool.append(t)
    for p in pool:
        p.join()

# 3. multiprocessing.Pool mp pool: consume: 3.398695707321167
@profile
def mp_pool():
    with Pool(processes=worker_num) as pool:
        tasks = []
        for i in range(worker_num):
            start = i * task_num
            end = (i+1) * task_num
            tasks.append(
                pool.apply_async(store_task, (big_data[start: end], './data/mp_pool', i)))
        pool.close()
        pool.join()

# 4. ProcessPoolExecutor loop pool: consume: 3.5791423320770264
@profile
def loop_pool():
    with ProcessPoolExecutor(max_workers=worker_num) as exe:
        for i in range(worker_num):
            start = i * task_num
            end = (i+1) * task_num
            exe.submit(store_task, big_data[start: end], './data/pool', i)

# 5. ThreadPoolExecutor Thread: consume: 0.028922557830810547
@profile
def loop_thread():
    with ThreadPoolExecutor(max_workers=worker_num) as exe:
        for i in range(worker_num):
            start = i * task_num
            end = (i+1) * task_num
            exe.submit(store_task, big_data[start: end], './data/pool_thread', i)

# 6.  direct direct: consume: 0.11469340324401855
@profile
def direct():
    store_task(big_data, './data/all', 0)

if __name__ == '__main__':
    with Benchmark("loop mp"):
        loop_mp()
    with Benchmark("mt thread"):
        mt_thread()
    with Benchmark("mp pool"):
        mp_pool()
    with Benchmark("loop pool"):
        loop_pool()
    with Benchmark("Thread"):
        loop_thread()
    with Benchmark("direct"):
        direct()
    