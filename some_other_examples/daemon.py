from multiprocessing import Process, Lock
import time

mutex = Lock()

def task(name):
    print(f"{name} is running")
    time.sleep(1)

if __name__ == "__main__":
    p = Process(target=task, args=("Kathy",))
    # p.daemon = True #一定要在p.start()前设置,设置p为守护进程,禁止p创建子进程,并且父进程代码执行结束,p即终止运行
    p.start()
    print("-" * 50)