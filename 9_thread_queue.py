import queue
import threading

"""
A Queue is a thread-safe data structure (FIFO — first-in-first-out) for exchanging data between threads.
Unlike using a plain list, a Queue handles:
Synchronization (no need to use your own locks).
Blocking (threads can wait until items are available/space is free).
Safe producer-consumer pattern.
"""

q = queue.Queue()
# q = queue.Queue(maxsize=2)


def producer():
    for i in range(5):
        q.put(i)    # add item to queue
        print("Produced", i)


def consumer():
    while True:
        item = q.get()      # blocks until item is available
        # print(q.qsize())
        if item is None:  # exit signal
            break
        print("Consumed", item)
        q.task_done()


threading.Thread(target=producer).start()
threading.Thread(target=consumer, daemon=True).start()
q.join()

"""
put(item) → add item (blocks if queue is full).
get() → remove & return item (blocks if empty).
task_done() → signal that a fetched task is completed.
join() → block until all tasks are marked done.
qsize() → approx size (not reliable in multithreaded code).
empty() / full() → check status (also not 100% reliable).
"""