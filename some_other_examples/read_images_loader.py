from multiprocessing import Process, Queue
import time
import os
import numpy as np
from PIL import Image
import threading

def default_loader(file_name):
    return Image.open(file_name)

def transform_image(image):
    return image.resize((480, 480))

def producer(file_name):
    img = default_loader(file_name)
    new_img = transform_image(img)
    # fn = "level_0_" + str(i)
    # fn = r"some_other_examples\data" + "/" + fn + ".png"
    # image = np.random.randint(0, 255, (1024, 1024, 3), dtype=np.uint8)
    # q.put([fn, image])
    # print(f"Open {file_name}")
    return np.array(new_img)

def multi_loader(files):
    images = []
    # p = ProcessPoolExecutor(max_workers=8) # slower than ThredPoolExecutor
    executor = ThreadPoolExecutor(max_workers=8)
    results = executor.map(producer, files)
    for result in results:
        images.append(result)

    return images


def producer_1(q):
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
    from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
    from multiprocessing import Pool
    from utils import  get_specified_files
    path = r"F:\Work\Data\svs_ano\test_split"
    files = get_specified_files(path, suffixes=[".png", ".jpg"], recursive=True)
    print(len(files))
    i = 0
    batch_size = 64
    batch_files = files[i:batch_size]

    start_time = time.time()
    #===================================================================
    # Read 16007 image in 3.49s(lazy read), resize 480 247.26s
    #===================================================================
    # images = []
    # for file in batch_files:
    #     # img = Image.open(file)
    #     # new_img = img.resize((480, 480))
    #     img = producer(file)
    #     images.append(img)

    #===================================================================
    # Read 16007 image in 11.62s, resize 480 76.59s-4, 66.27-6, 59.04-8, 51.69-10
    #====================================================================
    # images = []
    # # p = ProcessPoolExecutor(max_workers=8) # slower than ThredPoolExecutor
    # executor = ThreadPoolExecutor(max_workers=8)
    # results = executor.map(producer, batch_files)
    # for result in results:
    #     images.append(result)
    images = multi_loader(batch_files)

    #=================Not Working=================
    # produce_list = []
    # for i in range(2):
    #     p1 = Process(target=producer, args=(files[1],))
    #     p1.start()
    #     produce_list.append(p1)

    end_time = time.time()
    print(f"Elapse: {end_time - start_time}")

    images = np.stack(images)
    print(f"images.shape: {images.shape}")

    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 10))
    for i in range(images.shape[0]):
        plt.subplot(8, 8, i+1)
        img = images[i, :, :, :]
        img = np.squeeze(img)
        plt.imshow(img)
        plt.axis('off')
        plt.subplots_adjust(hspace=0.1, wspace=0.001)
    plt.show()
