from memory_profiler import profile

@profile
def read_random():
    with open("data/random_data.txt", "rb") as source:
        content = source.read(1024 * 10000)
        content_to_write = memoryview(content)[1024:]
    print(f"content length: {len(content)}, content to write length {len(content_to_write)}")
    with open("data/random_write.txt", "wb") as target:
        target.write(content_to_write)


if __name__ == "__main__":
    read_random()

# import numpy as np

# data = np.random.randint(0, 255, [1, 2048*10000])
# with open("data/random_data.txt", "wb") as target:
#     target.write(data)

#==Memory view===========================================================
# import socket
# s = socket.socket(…)
# s.connect(…)
# # Build a bytes object with more than 100 millions times the letter `a`
# data = b"a" * (1024 * 100000)
# mv = memoryview(data)
# while mv:
#     sent = s.send(mv)
#     # Build a new memoryview object pointing to the data which remains to be sent
#     mv = mv[sent:]
