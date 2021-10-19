import os
import numpy as np
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from memory_profiler import profile

from multiprocessing import shared_memory # python3.8
def store_task_sha_v2(start, end, output, index, sha_name, shape, dtype):
    fname = "%s_worker_%s.csv" % (output, index)
    exist_sham = shared_memory.SharedMemory(name=sha_name)
    data = np.ndarray(shape, dtype=dtype, buffer=exist_sham.buf)
    print(sha_name, data.shape, index)
    np.savetxt(fname, data[start: end], delimiter='\t')
    del data
    exist_sham.close()

#main data source
worker_num = os.cpu_count()
big_data = np.random.rand(1000000, 10)
task_num = big_data.shape[0] // worker_num

@profile
def mp_pool_sha():
    shm = shared_memory.SharedMemory(create=True, size=big_data.nbytes)
    b = np.ndarray(big_data.shape, dtype=big_data.dtype, buffer=shm.buf)
    b[:] = big_data[:]
    print(b.shape)
    with ProcessPoolExecutor(max_workers=worker_num) as pool:
        tasks = []
        for i in range(worker_num):
            start = i * task_num
            end = (i+1) * task_num
            tasks.append(
                pool.submit(store_task_sha_v2, 
                    start, end, 'testdata/mp_pool_sha', i ,
                    shm.name, b.shape, b.dtype))
        for t in tasks:
            # Note! 在这里捕获异常，ProcessPoolExecutor推荐这么使用!
            try:
                print(t.result())
            except Exception as e:
                print(f'{e}')
    del b
    shm.close()
    shm.unlink()