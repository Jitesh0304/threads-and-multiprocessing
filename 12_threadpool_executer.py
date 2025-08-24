from concurrent.futures import ThreadPoolExecutor, as_completed
import time, threading

"""
Use ThreadPoolExecutor for I/O-bound jobs (web scraping, DB queries, file reads/writes, etc.).
"""


def task(n):
    print(f"Task {n} running on {threading.current_thread().name}")
    time.sleep(2)
    return n * 2


if __name__ == "__main__":
    # with ThreadPoolExecutor(max_workers=3) as executor:
    #     futures = [executor.submit(task, i) for i in range(5)]
    #
    #     for f in futures:
    #         print("Result:", f.result())

    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(lambda x: x * x, range(5)))
        print(results)

    """
    shutdown(wait=True) → wait for threads to finish.
    future.cancel() → cancel task if not started.
    as_completed() → get results as they complete.
    """
