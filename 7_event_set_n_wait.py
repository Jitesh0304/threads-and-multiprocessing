import threading, time

"""
Event
    An Event is a simple flag (boolean) that threads can use to communicate.
    Initially, the flag is False.
    It has three main methods:
        set() → set the flag to True. (like turning a green light ON)
        clear() → set the flag back to False.
        wait(timeout=None) → block until the flag becomes True.
        
    event.wait() will block indefinitely until some thread calls event.set().
    Once set, the flag stays True until clear() is called.
    Any threads calling wait() after the event is already set will not block (they pass through immediately).
"""

event = threading.Event()


def waiter():
    print("Waiting for event...")
    if event.is_set():
        print('Already set event')
    event.wait()                    # blocks until event.set()
    print("Event received!", event.is_set())


def setter():
    time.sleep(2)
    print("Setting event")
    event.set()
    print("Set done")


t1 = threading.Thread(target=waiter)
t2 = threading.Thread(target=setter)
t1.start(); t2.start()


###################################################################################


from multiprocessing import Process, Event
import time


# set(), wait(), clear(), is_set().
def waiter(e, name):
    print(f"{name} waiting for event...")
    e.wait()   # blocks until event.set() is called
    print(f"{name} got the event!")


def setter(e):
    print("Setter sleeping...")
    time.sleep(3)
    print("Setter setting event")
    e.set()


if __name__ == "__main__":
    event = Event()

    p1 = Process(target=waiter, args=(event, "Process-1"))
    p2 = Process(target=waiter, args=(event, "Process-2"))
    p3 = Process(target=setter, args=(event, "Process-3"))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
