from queue import Queue
from threading import Lock, Thread
import time

class ClosableQueue(Queue):
    SENTINEL = object()

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
    return item

def upload(item):
    return item

download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()
threads = [
    StoppableWorker(download, download_queue, resize_queue),
    StoppableWorker(resize, resize_queue, upload_queue),
    StoppableWorker(upload, upload_queue, done_queue),
]

for thread in threads:
    thread.start()

for i in range(1000):
    # print(f'Putting object {i}')
    download_queue.put(object())

download_queue.close()

download_queue.join()
resize_queue.close()
resize_queue.join()
upload_queue.close()
upload_queue.join()

print(f'Processed {done_queue.qsize()} items')

for thread in threads:
    thread.join()


# # Example 1
# def download(item):
#     return item

# def resize(item):
#     return item

# def upload(item):
#     return item

# # Example 17
# class ClosableQueue(Queue):
#     SENTINEL = object()

#     def close(self):
#         self.put(self.SENTINEL)


# # Example 18
#     def __iter__(self):
#         while True:
#             item = self.get()
#             try:
#                 if item is self.SENTINEL:
#                     return  # Cause the thread to exit
#                 yield item
#             finally:
#                 self.task_done()


# # Example 19
# class StoppableWorker(Thread):
#     def __init__(self, func, in_queue, out_queue):
#         super().__init__()
#         self.func = func
#         self.in_queue = in_queue
#         self.out_queue = out_queue

#     def run(self):
#         for item in self.in_queue:
#             result = self.func(item)
#             self.out_queue.put(result)


# # Example 20
# download_queue = ClosableQueue()
# resize_queue = ClosableQueue()
# upload_queue = ClosableQueue()
# done_queue = ClosableQueue()
# threads = [
#     StoppableWorker(download, download_queue, resize_queue),
#     StoppableWorker(resize, resize_queue, upload_queue),
#     StoppableWorker(upload, upload_queue, done_queue),
# ]


# # Example 21
# for thread in threads:
#     thread.start()

# for _ in range(1000):
#     download_queue.put(object())

# download_queue.close()


# # Example 22
# download_queue.join()
# resize_queue.close()
# resize_queue.join()
# upload_queue.close()
# upload_queue.join()
# print(done_queue.qsize(), 'items finished')

# for thread in threads:
#     thread.join()