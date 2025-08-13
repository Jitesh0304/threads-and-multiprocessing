import multiprocessing
import time, uuid


# def split_video(file_path, task_id, tasks):
#     tasks[task_id]['status'] = 'running'
#     time.sleep(5)
#     tasks[task_id]['status'] = 'completed'
#
#
# if __name__ == "__main__":
#     with multiprocessing.Manager() as manager:
#         tasks = manager.dict()
#         processes = []
#
#         def start_task(file_path):
#             task_id = str(uuid.uuid4())
#             tasks[task_id] = manager.dict({'file': file_path, 'status': 'pending'})
#             p = multiprocessing.Process(target=split_video, args=(file_path, task_id, tasks), name=f"VideoSplit-{task_id[:8]}")
#             p.start()
#             processes.append(p)
#             return task_id
#
#         t1 = start_task("video1.mp4")
#         t2 = start_task("video2.mp4")
#
#         # Wait for all processes to finish
#         for p in processes:
#             p.join()
#
#         print({k: dict(v) for k, v in tasks.items()})  # convert nested manager.dicts to normal dicts









def split_video(file_path, task_id, tasks):
    tasks[task_id]['status'] = 'running'
    time.sleep(5)  # simulate work
    tasks[task_id]['status'] = 'completed'
    print(f"Process name - {multiprocessing.current_process().name}")
    print(f"Process alive - {multiprocessing.current_process().is_alive()}")


if __name__ == "__main__":
    with multiprocessing.Manager() as manager:
        tasks = manager.dict()

        def start_task(file_path):
            task_id = str(uuid.uuid4())
            tasks[task_id] = {'file': file_path, 'status': 'pending'}
            p = multiprocessing.Process(
                target=split_video,
                args=(file_path, task_id, tasks),
                name=f"VideoSplit-{task_id[:8]}"
            )
            p.start()
            return task_id

        # Start tasks
        task1 = start_task("video1.mp4")
        task2 = start_task("video2.mp4")

        print("Tasks started:", dict(tasks))

        # Instead of join, just wait enough time to see updates
        time.sleep(6)
        print("Tasks after 6s:", dict(tasks))
