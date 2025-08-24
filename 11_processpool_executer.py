from concurrent.futures import ProcessPoolExecutor, as_completed
import time, os, random

"""
Use ProcessPoolExecutor for CPU-bound jobs (video encoding, ML inference, heavy computations).
"""


def square(x, y):
    print(f"Worker {os.getpid()} computing {x} - Y{y}")
    time.sleep(2)
    return x * x


def task(x):
    sleep_time = random.randint(1, 5)
    time.sleep(sleep_time)
    return f"Task {x} done in {sleep_time}s"


def increment(x):
    return x + 1


if __name__ == "__main__":
    """
    Each submit() returns a Future object, from which you can:
        .result() → get the result (blocks until ready).
        .done() → check if finished.
        .cancel() → cancel before start.
    """
    # with ProcessPoolExecutor(max_workers=3) as executor:
    #     # Submit tasks (returns Future objects)
    #     futures = [executor.submit(square, i, 'i') for i in range(5)]
    #     # executor.shutdown(wait=True)   # waits for tasks to finish
    #     # executor.shutdown(wait=False)   # to return immediately / hard kill
    #
    #     # Wait and get results
    #     for f in futures:
    #         # print("Result:", f.cancel())
    #         # print("Result:", f.done())
    #         print("Result:", f.result())

    # """
    # Map-style (like Pool.map)
    # """
    # with ProcessPoolExecutor() as executor:
    #     results = list(executor.map(increment, range(5)))
    #     print(results)

    # """
    # Asynchronous with as_completed
    # """
    # with ProcessPoolExecutor(max_workers=3) as executor:
    #     futures = [executor.submit(task, i) for i in range(5)]
    #
    #     for f in as_completed(futures):  # gives results as they finish
    #         print(f.result())

    """
    future.cancel()
    Cancels a specific task, but only if it hasn’t started yet.
    If already running, cancel() returns False.
    """
    with ProcessPoolExecutor(max_workers=1) as executor:
        f1 = executor.submit(task, 1)
        f2 = executor.submit(task, 2)

        cancelled = f2.cancel()
        print("Cancelled second task:", cancelled)

        print("Result 1:", f1.result())
        # f2.result() would raise CancelledError if it was cancelled


