from multiprocessing import Process, Queue
import time
import os
import numpy as np
from PIL import Image
import threading

def producer(q):
    for i in range(500):
        fn = "level_0_" + str(i)
        fn = r"some_other_examples\data" + "/" + fn + ".png"
        image = np.random.randint(0, 255, (1024, 1024, 3), dtype=np.uint8)
        q.put([fn, image])
        print(f"Generate {fn}")


def consumer(q):
    while True:
        res = q.get()
        if res is None:
            break  # End signal
        fn, image = res[0], res[1]
        save(fn, image)


def save(fn, image):
    tile = Image.fromarray(image)
    tile.save(fn, format="png", quality=100)
    print(f"{fn} saved")


def main():
    q = Queue(maxsize=500)

    # Now one 1 producer is most fast than others
    produce_list = []
    for i in range(1):
        p1 = Process(target=producer, args=(q,))
        # can be changed to threading.thead
        # p1 = threading.Thread(target=producer, args=(q,))
        p1.start()
        produce_list.append(p1)

    consum_list = []
    for i in range(10):
        c1 = Process(target=consumer, args=(q,))
        # c1 = threading.Thread(target=consumer, args=(q,))
        c1.start()
        consum_list.append(c1)

    for p in produce_list:
        p.join()

    for i in range(len(consum_list)):
        q.put(None)


if __name__ == "__main__":
    # q = Queue(maxsize=500)
    start_time = time.time()

    # # for i in range(100):
    # #     fn = "level_0_" + str(i)
    # #     fn = r"some_other_examples\data" + "/" + fn + ".png"
    # #     image = np.random.randint(0, 255, (1024, 1024, 3), dtype=np.uint8)
    # #     print(image.shape)
    # #     print(f"Generate {fn}")
    # #     tile = Image.fromarray(image)
    # #     tile.save(fn, format="png", quality=100)
    # #     print(f"{fn} saved")
    main()
    end_time = time.time()
    print(f"Elapse: {end_time - start_time}")
