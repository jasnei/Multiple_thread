"""
Parallel load data from same file. not working yet!!!
"""
import os
import time
from functools import wraps
from multiprocessing import Process, Pool, Manager
import numpy as np

#main data source
worker_num = os.cpu_count()
big_data = np.random.rand(1000000, 10)
task_num = big_data.shape[0] // worker_num

# Time calculator
class Benchmark:
    def __init__(self, text):
        self.text = text
    def __enter__(self):
        self.start = time.time()
    def __exit__(self, *args):
        self.end = time.time()
        print("%s: consume: %s" % (self.text, self.end - self.start))

def parallize_load(file, total_num, worker_num):
    """Load embedding file parallelization
       @emb_file: source filename
       @total_num: total lines
       @worker_num: parallelize process num
    return: np.ndaary
    """
    # @wraps(file)
    def load_from_txt(emb, start, n_rows, arr_list):
        data = np.loadtxt(emb, skiprows=start, max_rows=n_rows)
        arr_list.append(data)

    worker_load_num = total_num // worker_num
    pool = []
    with Manager() as manager:
        arr_list = manager.list([])
        for index in range(worker_num):
            s = index * worker_load_num
            if index != worker_num - 1:
                e = worker_load_num
            else:
                e = total_num - (worker_load_num * index)
            p = Process(target=load_from_txt, args=(file, s, e, arr_list))
            pool.append(p)
            p.start()
        for p in pool:
            p.join()
        arr = np.concatenate(arr_list)
    return arr
if __name__ == '__main__':
    with Benchmark("parallel_load"):
        # data = np.loadtxt(r"data\all_worker_0.txt")
        source_total_num = sum(1 for line in open("data/all_worker_0.txt"))
        print(source_total_num)
        source_emb_data = parallize_load("data/all_worker_0.txt", source_total_num, 1)
