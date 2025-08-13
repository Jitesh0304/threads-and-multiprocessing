from threading import Thread, Event
import time


# def split_video(stop_event):
#     print("Splitting started...")
#     for i in range(10):
#         if stop_event.is_set():
#             print("Splitting stopped!")
#             return
#         time.sleep(1)
#     print("Splitting completed!")
#
#
# stop_event = Event()
# t = Thread(target=split_video, args=(stop_event,), name="VideoSplit-1")
# t.start()
#
# time.sleep(3)  # Let it run for 3 seconds
# stop_event.set()  # Ask it to stop


tasks = []

def worker(task_id, stop_event):
    print(f"Task-{task_id} started")
    for i in range(10):
        if stop_event.is_set():
            print(f"Task-{task_id} stopped")
            return
        time.sleep(1)
    print(f"Task-{task_id} completed")

# Start 5 tasks
for i in range(1, 6):
    stop_event = Event()
    t = Thread(target=worker, args=(i, stop_event), name=f"Task-{i}")
    tasks.append({"thread": t, "stop_event": stop_event})
    t.start()

time.sleep(3)  # Let them run
tasks[2]["stop_event"].set()

