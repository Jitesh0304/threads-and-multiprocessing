import time
import threading
import multiprocessing
import uuid


tasks = {}


def split_video(file_path, task_id):
    tasks[task_id]['status'] = 'running'
    try:
        print(f"[{threading.current_thread().name}] Splitting {file_path} started...")
        print(f"Thread alive - {threading.current_thread().is_alive()}")
        time.sleep(5)  # simulate work
        tasks[task_id]['status'] = 'completed'
    except Exception as e:
        tasks[task_id]['status'] = 'failed'
        tasks[task_id]['error'] = str(e)
    finally:
        tasks[task_id]['end_time'] = time.time()


def start_split_task(file_path):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        'file': file_path,
        'status': 'pending',
        'start_time': time.time(),
        'end_time': None,
        'error': None
    }
    t = threading.Thread(
        target=split_video,
        args=(file_path, task_id),
        name=f"VideoSplit-{task_id[:8]}",
        daemon=False
    )
    t.start()
    return task_id


task1 = start_split_task("video1.mp4")
task2 = start_split_task("video2.mp4")

time.sleep(2)
print("Current tasks:", tasks)

