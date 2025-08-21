import threading

"""
When multiple threads run in the same memory space, they can interfere with each other.
This creates race conditions — unpredictable behavior because two threads read/write the same data at the same time.
"""
counter = 0


# def increment():
#     global counter
#     for i in range(100000):
#         counter += 1
#
#
# threads = []
# for j in range(15):
#     t = threading.Thread(target=increment)
#     threads.append(t)
#     t.start()
#
# for thread in threads:
#     thread.join()
#
# print("Final counter:", counter)


"""
Expected result = 500000
Actual result = less than 500000 (different every run).
This happens because threads overwrite each other’s updates.
"""


#############################################################
# Solution for the above problem
"""
Lock
    A Lock (a.k.a. mutex) can be either locked or unlocked.
    If a thread calls lock.acquire():
        If it’s free → the thread acquires it.
        If it’s already held → the thread blocks until another thread releases it.
        If the same thread tries to acquire it again without releasing → deadlock (because it blocks on itself).
        
RLock (re-entrant lock)
    Re-entrant lock = a lock that can be acquired multiple times by the same thread without deadlocking.
    Internally, it keeps a counter of how many times it has been acquired by the owner thread.
    The thread must call release() the same number of times before another thread can acquire it.
"""
#############################################################

lock = threading.Lock()
rlock = threading.RLock()


# def increment():
#     """
#     Ensures only one thread at a time executes a critical section.
#     Equivalent to a mutex.
#     """
#     global counter
#     for i in range(100000):
#         with lock:          # acquire & release automatically
#             counter += 1
# # lock.acquire()
# # # critical section
# # lock.release()


def increment():
    """
    Like a Lock, but the same thread can acquire it multiple times without deadlock.
    Useful in recursive functions.
    """
    global counter
    for i in range(100000):
        with rlock:
            with rlock:  # same thread can re-acquire safely
                counter += 1
# rlock.acquire()
# rlock.acquire()   # allowed, no deadlock
# # critical section
# rlock.release()
# rlock.release()


threads = []
for j in range(5):
    t = threading.Thread(target=increment)
    threads.append(t)
    t.start()

for thread in threads:
    thread.join()

print("Final counter:", counter)
