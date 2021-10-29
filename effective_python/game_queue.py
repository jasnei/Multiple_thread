import time
from queue import Queue
from threading import Lock, Thread
from concurrent.futures import ThreadPoolExecutor


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


class SimulationError(Exception):
    pass


ALIVE = '*'
EMPTY = '-'


class Grid:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

    def get(self, y, x):
        return self.rows[y % self.height][x % self.width]

    def set(self, y, x, state):
        self.rows[y % self.height][x % self.width] = state

    def __str__(self):
        output = ''
        for row in self.rows:
            for cell in row:
                output += cell
            output += '\n'
        return output


class LockingGrid(Grid):
    def __init__(self, height, width):
        super().__init__(height, width)
        self.lock = Lock()

    def __str__(self):
        with self.lock:
            return super().__str__()
    
    def get(self, y, x):
        with self.lock:
            return super().get(y, x)
    
    def set(self, y, x, state):
        with self.lock:
            return super().set(y, x, state)


def count_neighbors(y, x, get):
    n_ = get(y - 1, x + 0)
    ne = get(y - 1, x + 1)
    e_ = get(y + 0, x + 1)
    se = get(y + 1, x + 1)
    s_ = get(y + 1, x + 0)
    sw = get(y + 1, x - 1)
    w_ = get(y + 0, x - 1)
    nw = get(y - 1, x - 1)
    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    return count

def game_logic(state, neighbors):
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY     # Die: Too few
        elif neighbors > 3:
            return EMPTY     # Die: Too many
    else:
        if neighbors == 3:
            return ALIVE     # Regenerate
    return state

def game_logic_thread(item):
    y, x, state, neighbors = item
    try:
        next_state = game_logic(state, neighbors)
    except Exception as e:
        next_state = e
    return (y, x, next_state)

in_queue = ClosableQueue()
out_queue = ClosableQueue()
threads = []
for _ in range(5):
    thread = StoppableWorker(
        game_logic_thread, in_queue, out_queue)
    thread.start()
    threads.append(thread)

def step_cell(y, x, get, set):
    state = get(y, x)
    neighbors = count_neighbors(y, x, get)
    next_state = game_logic(state, neighbors)
    set(y, x, next_state)

def simulate_pipeline(grid, in_queue, out_queue):
    for y in range(grid.height):
        for x in range(grid.width):
            state = grid.get(y, x)
            neighbors = count_neighbors(y, x, grid.get)
            in_queue.put((y, x, state, neighbors))
    
    in_queue.join()
    out_queue.close()
    next_grid = Grid(grid.height, grid.width)
    for item in out_queue:
        y, x, next_state = item
        if isinstance(next_state, Exception):
            raise SimulationError(y, x) from next_state
        next_grid.set(y, x, next_state)
    
    return next_grid

def simulate_pool(pool, grid):
    next_grid = LockingGrid(grid.height, grid.width)

    futures = []
    for y in range(grid.height):
        for x in range(grid.width):
            args = (y, x, grid.get, next_grid.set)
            future = pool.submit(step_cell, *args)  # Fan out
            futures.append(future)
    
    for future in futures:
        future.result()                             # Fan out

    return next_grid


class ColumnPrinter:
    def __init__(self):
        self.columns = []

    def append(self, data):
        self.columns.append(data)

    def __str__(self):
        row_count = 1
        for data in self.columns:
            row_count = max(
                row_count, len(data.splitlines()) + 1)

        rows = [''] * row_count
        for j in range(row_count):
            for i, data in enumerate(self.columns):
                line = data.splitlines()[max(0, j - 1)]
                if j == 0:
                    padding = ' ' * (len(line) // 2)
                    rows[j] += padding + str(i) + padding
                else:
                    rows[j] += line

                if (i + 1) < len(self.columns):
                    rows[j] += ' | '

        return '\n'.join(rows)


grid = LockingGrid(5, 9)
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)
# print(grid)

columns = ColumnPrinter()
start = time.time()
# with ThreadPoolExecutor(max_workers=10) as pool:
#     for i in range(10000):
#         columns.append(str(grid))
#         grid = simulate_pool(pool, grid)

for i in range(10000):
    columns.append(str(grid))
    grid = simulate_pipeline(grid, in_queue, out_queue)

end = time.time()
# print(columns)
for thread in threads:
    in_queue.close()
for thread in threads:
    thread.join()
print(f"Elaps: {end - start:.4} seconds")