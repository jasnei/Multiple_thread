from multiprocessing import Process, Lock
import os, time

#======================================
# Without Lock
#======================================
# def work():
#     print(f"{os.getpid()} is running")
#     time.sleep(1)
#     print(f"{os.getpid()} is done")
#     print("-" * 50)

# if __name__ == "__main__":
#     for i in range(3):
#         p = Process(target=work)
#         p.start()

#======================================
# With Lock 
#======================================
# 由并发变成了串行,牺牲了运行效率,但避免了竞争
def work(lock):
    lock.acquire()
    print(f"{os.getpid()} is running")
    time.sleep(1)
    print(f"{os.getpid()} is done")
    print("-" * 50)
    lock.release()

if __name__ == "__main__":
    lock = Lock()
    for i in range(3):
        p = Process(target=work, args=(lock,))
        p.start()