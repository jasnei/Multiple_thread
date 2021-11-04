import time
from threading import Thread, Lock

class NoNewData(Exception):
    pass


def readline(handle):
    offset = handle.tell()
    handle.seek(0, 2)
    length = handle.tell()

    if length == offset:
        raise NoNewData

    handle.seek(offset, 0)

    return handle.readline



def tail_file(handle, interval, writer_func):
    while not handle.closed:
        try:
            line = readline(handle)
        except NoNewData:
            time.sleep(interval)
        else:
            writer_func(line)

def run_threads(handles, interval, output_path):
    with open(output_path, 'wb') as out:
        lock = Lock()
        def write(data):
            with lock:
                out.write(data)

    threads = []
    for handle in handles:
        args = (handle, interval, write)
        thread = Thread(target=tail_file, args=args)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()