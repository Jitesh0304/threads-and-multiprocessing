import multiprocessing
import threading
import time

"""
Concurrency = Doing multiple tasks seemingly at the same time (tasks may share a single CPU core but switch rapidly).
        Concurrency: A single chef cooking two dishes by switching between them.

Parallelism = Doing multiple tasks exactly at the same time on different CPU cores.
        Parallelism: Two chefs cooking two dishes at the same time.

Feature	            Multithreading	                                        Multiprocessing
Execution	    Multiple threads in a single process	                Multiple processes each with its own Python interpreter
Memory	        Shared memory space	                                    Separate memory space
Best for	    I/O-bound tasks (waiting for network, disk, etc.)	    CPU-bound tasks (heavy computation)
Limitation	    Affected by the GIL in CPython	                        No GIL limitation
Overhead	    Low (threads are lighter)	                            High (process creation is heavier)

Key Takeaway at this stage:
    1)  If task is waiting a lot → Use threading (or async).
    2)  If task is computing a lot → Use multiprocessing.
    
start()
    1)  Kick off work in background.
    2)  Purpose: Tells the thread or process to begin execution.
    3)  Fire-and-forget tasks (logging, analytics sending, background cleanup).

join()
    1)  Wait for it to complete before moving on.
    2)  Purpose: Makes the main program wait until the thread or process finishes.
    3)  Wait until all running tasks finish naturally, wait for workers to exit

Risks of skipping join()
    1)  If the main program exits, threads/processes that are not daemon will still try to finish — this can delay exit.
    2)  If the thread/process is daemon, it will be killed immediately when the main program exits — might leave work incomplete.
"""


def io_bound_task(name):
    print(f"Start {name} retrieving data")
    time.sleep(2)
    print(f"End {name} - Complete")


def cpu_bound_task(name):
    print(f"[START] {name} - Heavy calculation...")
    total = 0
    for i in range(10_000):
        total += i
    print(f"[END] {name} - Done!")


if __name__ == "__main__":
    print("\n=== 1. Concurrency with THREADS (I/O-bound) ===")
    start = time.time()

    """
        (demon=True)
        Daemon threads/processes are killed the moment your main program (or the parent process) exits.
        
        daemon=True → For non-critical background tasks that can be dropped anytime.
        daemon=False → For important tasks that must complete even if user already got a response.
    """
    threads = []
    for i in range(3):
        t = threading.Thread(target=io_bound_task, args=(f"Thread {i+1}",), daemon=False, name=f"Thread name - {i+1}")
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f"Time taken with threads: {time.time() - start:.2f} seconds\n")

    print("\n=== 2. Parallelism with PROCESSES (CPU-bound) ===")
    start = time.time()

    processes = []
    for i in range(3):
        p = multiprocessing.Process(target=cpu_bound_task, args=(f"Process-{i+1}",), daemon=False,
                                    name=f"Process name - {i+1}")
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    print(f"Time taken with processes: {time.time() - start:.2f} seconds\n")

