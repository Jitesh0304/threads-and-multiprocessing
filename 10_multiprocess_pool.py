from multiprocessing import Pool
import time

"""
A Pool manages a group of worker processes.
Instead of manually creating and tracking Process objects, you just give a function + data, and Pool distributes the work automatically.

If you need results → use map / apply (blocking).
If you just want to fire-and-forget → use map_async / apply_async with no .get().

Single job: apply, apply_async
Batch jobs: map, map_async, starmap, starmap_async
Streaming: imap, imap_unordered
Control: close, terminate, join
Extras: callback, error_callback, chunksize
"""


def square(n):
    time.sleep(1)  # simulate heavy work
    print(n)
    return n * n


def power(a, b):
    return a ** b


def on_done(results):
    print("Task completed with:", results)


def on_error(e):
    print("Error:", e)


if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]

    # Create a pool of 3 worker processes

    # """
    # map(func, iterable)
    #     Applies func to each element of iterable.
    #     Blocks until all results are ready.
    #     Works like map() but in parallel.
    # """
    # with Pool(processes=3) as pool:
    #     results = pool.map(square, numbers)  # map function to data
    #     print("Squares:", results)


    # """
    # starmap(func, iterable_of_args, chunksize)
    #     Like map, but passes multiple args to function.
    #
    # When you give a Pool an iterable (like [1,2,3,4,...]), it doesn’t send each element individually.
    # Instead, it splits the iterable into chunks of size chunksize and gives each chunk to a worker process.
    # Each worker then processes its chunk item by item.
    #
    # If there are 9 tasks (range(1,10)).
    #     With chunksize=2, Pool will split into [(1,2), (3,4), (5,6), (7,8), (9,)].
    #     Each worker will get a chunk instead of a single number at a time.
    #
    # If tasks are very fast/lightweight → increase chunksize (to reduce IPC overhead).
    # If tasks are slow/heavy → keep smaller chunksize (better load balancing).
    #
    # """
    # with Pool(2) as pool:
    #     results = pool.starmap(power, [(2, 3), (3, 4), (4, 2)])
    #     print(results)


    # """
    # map_async(func, iterable, chunksize, callback, error_callback)
    #     Same as map, but non-blocking.
    #     Returns a result object → you can call .get() later.
    # """
    # with Pool(processes=3) as pool:
    #     result = pool.map_async(square, numbers, callback=on_done, error_callback=on_error)          # run task in background
    #     print("Doing other work...")
    #     # print(result.get())       # blocks only here => get means wait till all task complete
    #     # time.sleep(10)


    # """
    # apply(func, args)
    #     Runs the function in one worker.
    #     Blocking.
    # """
    # with Pool(processes=3) as pool:
    #     result = pool.apply(square, (5,))
    #     print(result)


    # """
    # apply_async(func, args)
    #     Non-Blocking.
    # """
    # with Pool(processes=3) as pool:
    #     result = pool.apply_async(square, (5,))
    #     print(result.get())

    # # Close pool (no more tasks allowed)
    # pool.close()      # Gracefully finish ongoing jobs, stop new ones.
    # # Wait for workers to finish
    # pool.join()       # Wait for workers to exit (always use after close/terminate).  # wait for workers to exit
    # # kill everything immediately
    # pool.terminate()      # Emergency stop, kill all jobs.

    """
    imap and imap_unordered
        Like map, but returns an iterator.
        imap_unordered yields results as soon as each task finishes (faster streaming).
    """
    with Pool(processes=3) as pool:
        print("===imap (ordered) ===")
        for result in pool.imap(square, numbers):
            # results come in same order [3,1,2]
            print(result)

        print("=== imap_unordered (faster) ===")
        for result in pool.imap_unordered(square, numbers):
            # results come as soon as finished (order changes!)
            print(result)

