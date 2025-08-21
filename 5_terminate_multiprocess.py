from multiprocessing import Process, Manager
import time


# def split_video():
#     print("Splitting started...")
#     time.sleep(10)
#     print("Splitting completed!")
#
#
# if __name__ == "__main__":
#     p = Process(target=split_video, name="VideoSplit-1")
#     p.start()
#
#     time.sleep(3)  # Let it run for 3 seconds
#     p.terminate()  # or p.kill()
#     print("Process terminated?", not p.is_alive())


#############################################################################

# processes = []
#
# def worker(task_id):
#     print(f"Task-{task_id} started")
#     time.sleep(10)
#     print(f"Task-{task_id} completed")
#
# if __name__ == "__main__":
#     # for i in range(1, 6):
#     #     p = Process(target=worker, args=(i,), name=f"Task-{i}")
#     #     processes.append(p)
#     #     p.start()
#     #
#     # time.sleep(3)  # Let them run
#     # processes[2].terminate()  # Kill only the 3rd process (index 2)
#     # print("3rd task terminated")
#
#     with Manager() as manager:
#         tasks = manager.dict()
#         for i in range(1, 6):
#             p = Process(target=worker, args=(i,), name=f"Task-{i}")
#             processes.append(p)
#             p.start()
#
#         time.sleep(3)  # Let them run
#         # processes[2].terminate()  # Kill only the 3rd process (index 2)
#         print("3rd task terminated")


def worker(task_id, tasks):
    print(f"Task-{task_id} started")
    tasks[task_id] = 'running'

    for i in range(10):
        if tasks.get(f"terminate-{task_id}", False):
            print(f"Task-{task_id} received terminate signal")
            tasks[task_id] = 'terminated'
            return
        time.sleep(1)

    tasks[task_id] = 'completed'
    print(f"Task-{task_id} completed")


if __name__ == "__main__":
    with Manager() as manager:
        tasks = manager.dict()
        processes = {}

        # Start tasks
        for i in range(1, 6):
            p = Process(target=worker, args=(i, tasks), name=f"Task-{i}")
            p.start()
            processes[i] = p

        time.sleep(3)

        # Send termination signal to Task-3
        tasks["terminate-3"] = True
        print("Sent termination signal to Task-3")

        # Join all processes
        for pid, proc in processes.items():
            proc.join()

        # Final task statuses
        print("\nTask Statuses:")
        for i in range(1, 6):
            print(f"Task-{i}: {tasks.get(i)}")



