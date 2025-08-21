import threading
import time

"""
Semaphore / BoundedSemaphore
    Limits how many threads can access a resource simultaneously.
    Example: max 3 threads can write to a DB at once.
    
    A Semaphore is basically a counter + lock.
        You initialize it with a number N.
        At most N threads can hold the semaphore at the same time.
        If all N “permits” are taken, further .acquire() calls block until another thread releases.
"""
sema = threading.Semaphore(4)       # allow up to 3 threads at once


def worker(n):
    with sema:      # acquire and auto-release at exit
        print(f"Thread-{n} working")
        time.sleep(2)


# for i in range(6):
#     threading.Thread(target=worker, args=(i,)).start()
threads = []
for i in range(10):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

for thread in threads:
    thread.join()


#############################################################
"""
Barrier
    Blocks a set of threads until all of them reach the barrier.
    Example: start all threads together only after everyone is ready.
    Makes threads wait until all have reached a point.
    Keep in mind that if the number of workers does not equal the number specified in the barrier, 
        then all the tasks that are ready will have to wait until the required number of workers is reached.
        
    A Barrier is used to synchronize a fixed number of threads at a certain point.
    You initialize it with a number N.
    Each thread calls .wait() on the barrier.
    When N threads have called .wait(), the barrier is released → all threads proceed together.
"""
#############################################################


# barrier = threading.Barrier(3)
#
#
# def worker(n):
#     print(f"Thread-{n} waiting at barrier")
#     barrier.wait()
#     print(f"Thread-{n} started work")
#
#
# for i in range(12):
#     threading.Thread(target=worker, args=(i,)).start()

