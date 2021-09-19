from multiprocessing import Process, Pipe

def f(conn):
    conn.send("hello father")
    print(conn.recv())
    conn.close()

if __name__ == "__main__":
    parent_conn, child_conn = Pipe()

    p = Process(target=f, args=(child_conn,))
    p.start()
    print(parent_conn.recv())
    parent_conn.send("hello child")
    p.join()