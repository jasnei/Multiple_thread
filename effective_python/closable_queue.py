from queue import Queue
from threading import Lock, Thread
import time

from PIL import Image
import numpy as np

class ClosableQueue(Queue):
    SENTINEL = None

    def close(self):
        self.put(self.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return  # Cause the thread to exit
                yield item
            finally:
                self.task_done()


class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)


def download(item):
    return item

def resize(item):
    img = Image.fromarray(item)
    img = np.array(img.resize((128, 128)))
    return img

def upload(item):
    return item

#======================================================================
# 扩展，多个线程同时处理某一个环节，以提高I/O并行度，从而大幅提升程序效率
#======================================================================
def start_threads(count, *args):
    threads = [StoppableWorker(*args) for _ in range(count)]
    for thread in threads:
        thread.start()
    return threads

def stop_threads(closable_queue, threads):
    for _ in threads:
        closable_queue.close()
    
    closable_queue.join()

    for thread in threads:
        thread.join()

download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()

dowload_threads = start_threads(
    3, download, download_queue, resize_queue
    )
resize_threads = start_threads(
    4, resize, resize_queue, upload_queue
    )
upload_threads = start_threads(
    5, upload, upload_queue, done_queue
    )
# threads = [
#     StoppableWorker(download, download_queue, resize_queue),
#     StoppableWorker(resize, resize_queue, upload_queue),
#     StoppableWorker(upload, upload_queue, done_queue),
# ]

# for thread in threads:
#     thread.start()

for i in range(1000):
    # print(f'Putting object {i}')
    img = np.random.randint(0, 256, [512, 512, 3], dtype=np.uint8)
    download_queue.put(img)

# download_queue.close()

# download_queue.join()
# resize_queue.close()
# resize_queue.join()
# upload_queue.close()
# upload_queue.join()
stop_threads(download_queue, dowload_threads)
stop_threads(resize_queue, resize_threads)
stop_threads(upload_queue, upload_threads)

print(f'Processed {done_queue.qsize()} items')

for thread in upload_threads:
    done_queue.put(None)
for i, object in enumerate(done_queue):
    print(object.shape, i)
    if object is None:
        break