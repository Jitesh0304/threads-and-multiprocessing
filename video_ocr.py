from multiprocessing import Process, Queue, cpu_count
import random
import time


def init_models():
    yolo_model = {'yolo_key': 'perform your task'}
    ocr = {'ocr_key': 'perform your task'}
    return ocr, yolo_model


def crop_region(frame, area):
    # print(f"Cropping area {area} from frame {frame}")
    return f"crop_{area}"


def run_ocr(ocr, image):
    # print(f"OCR on {image}")
    time.sleep(0.5)
    return ocr.get('ocr_key')


def worker(frame_queue, result_queue, AREA1, AREA2, AREA3):
    ocr, yolo_model = init_models()
    while True:
        item = frame_queue.get()    # blocks until item arrives
        if item is None:                # poison pill = stop signal
            break
        frame_no, frame = item

        vehicle_speed_img = crop_region(frame, AREA1)
        suggested_speed_img = crop_region(frame, AREA2)
        traffic_area_img = crop_region(frame, AREA3)

        vehicle_speed = run_ocr(ocr, vehicle_speed_img)
        suggested_speed = run_ocr(ocr, suggested_speed_img)

        results = yolo_model.get('yolo_key')
        signs = []
        for i in range(2):  # dummy 2 signs
            signs.append({"label": i+1, "ocr": f"sign={i+1}"})
        time.sleep(0.7)

        result_queue.put({
            "frame": frame_no,
            "vehicle_speed": vehicle_speed,
            "suggested_speed": suggested_speed,
            "traffic_signs": signs
        })


def frame_reader(video_path, frame_queue):
    frame_no = 0
    while True:
        if frame_no > 100:  # mock 100 frames only
            break
        frame_no += 1
        frame_queue.put((frame_no, random.randint(1000, 9999)))


def process_video(video_path):
    AREA1, AREA2, AREA3 = (100,50,200,80), (350,50,200,80), (600,100,300,300)
    frame_queue, result_queue = Queue(maxsize=20), Queue()

    # Start reader
    reader = Process(target=frame_reader, args=(video_path, frame_queue))
    reader.start()          # start producing frames

    # Start workers
    num_workers = max(2, cpu_count()-1)
    workers = []
    for _ in range(num_workers):
        p = Process(target=worker, args=(frame_queue,result_queue,AREA1,AREA2,AREA3))
        p.start()
        workers.append(p)

    # Wait for reader to finish
    reader.join()
    print("Reader finished")

    # Send poison pills
    for _ in workers:
        frame_queue.put(None)   # tell workers to stop at the end

    from queue import Empty
    # Collect results while waiting
    results = []
    alive = True
    while alive:
        alive = any(p.is_alive() for p in workers) or not result_queue.empty()
        try:
            item = result_queue.get(timeout=0.5)  # non-blocking wait
            results.append(item)
        except Empty:
            pass

    # Join workers
    for p in workers:
        p.join()    # start consuming
    print("Workers finished")

    results.sort(key=lambda x: x["frame"])
    return results


if __name__ == "__main__":
    data = process_video("traffic.mp4")
    print("Sample results:", data)

"""
Working principle of your code
    Reader process
        Runs a while loop to generate frames.
        Since frame_queue has maxsize=20, once 20 items are inside, put() blocks.
        It will wait until a worker takes a frame → then it can push the next one.
        This way, even though it needs to produce 100 frames, only 20 exist in memory at any moment.

Workers
    Number of workers = cpu_count() - 1 (or at least 2).
    All workers share the same frame_queue.
    Each worker runs its own infinite while True loop, calling frame_queue.get().
    If there’s a frame, they process it and push results into result_queue.
    If they get a None → they break and exit.

Parallelism
    Reader produces frames (up to queue capacity).
    Workers consume frames simultaneously (parallel CPU usage).
    This keeps frame_queue flowing:
        Reader fills it up.
        Workers drain it.
        Reader resumes producing more.
    So production and consumption run concurrently until all 100 frames are handled.

Main process
    Waits for reader to finish (reader.join()).
    Once done, it pushes one poison pill per worker (frame_queue.put(None) for each worker).
    This signals all workers to gracefully stop once they finish current tasks.

Result collection
    Main keeps pulling results from result_queue while workers are alive OR results are still pending.
    Ensures every frame’s result is collected.

Clean exit
    After results are drained, p.join() waits for each worker to fully exit.
    At this point:
        Reader is dead
        Workers are dead
        Queues are drained
    Function returns sorted results.
"""


# import cv2
# import torch
# import easyocr
# from multiprocessing import Process, Queue, cpu_count
#
#
#
# # Load models globally (each worker loads its own copy)
# def init_models():
#     ocr = easyocr.Reader(['en'])
#     yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
#     return ocr, yolo_model
#
#
# # Crop function
# def crop_region(frame, area):
#     x, y, w, h = area
#     return frame[y:y+h, x:x+w]
#
#
# def run_ocr(ocr, image):
#     results = ocr.readtext(image, detail=0)
#     return results[0] if results else None
#
#
# # Worker function
# def worker(frame_queue, result_queue, AREA1, AREA2, AREA3):
#     ocr, yolo_model = init_models()
#
#     while True:
#         item = frame_queue.get()
#         if item is None:  # poison pill to stop worker
#             break
#         frame_no, frame = item
#         count = 1
#
#         # Extract ROIs
#         vehicle_speed_img = crop_region(frame, AREA1)
#         suggested_speed_img = crop_region(frame, AREA2)
#         traffic_area_img = crop_region(frame, AREA3)
#
#         # OCR
#         vehicle_speed = run_ocr(ocr, vehicle_speed_img)
#         suggested_speed = run_ocr(ocr, suggested_speed_img)
#
#         # YOLO
#         results = yolo_model(traffic_area_img)
#         signs = []
#         for *xyxy, conf, cls in results.xyxy[0].tolist():
#             x1, y1, x2, y2 = map(int, xyxy)
#             sign_crop = traffic_area_img[y1:y2, x1:x2]
#             sign_value = run_ocr(ocr, sign_crop)
#             signs.append({"label": int(cls), "ocr": sign_value})
#
#         result_queue.put({
#             "frame": frame_no,
#             "vehicle_speed": vehicle_speed,
#             "suggested_speed": suggested_speed,
#             "traffic_signs": signs
#         })
#
#
# # Frame reader
# def frame_reader(video_path, frame_queue):
#     cap = cv2.VideoCapture(video_path)
#     frame_no = 0
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         frame_no += 1
#         frame_queue.put((frame_no, frame))
#     cap.release()
#
#
# # Main pipeline
# def process_video(video_path):
#     AREA1 = (100, 50, 200, 80)
#     AREA2 = (350, 50, 200, 80)
#     AREA3 = (600, 100, 300, 300)
#
#     frame_queue = Queue(maxsize=20)   # frame buffer
#     result_queue = Queue()
#
#     # Start frame reader
#     reader = Process(target=frame_reader, args=(video_path, frame_queue))
#     reader.start()
#
#     # Start workers
#     num_workers = max(2, cpu_count() - 1)  # leave 1 core free
#     workers = []
#     for _ in range(num_workers):
#         p = Process(target=worker, args=(frame_queue, result_queue, AREA1, AREA2, AREA3))
#         p.start()
#         workers.append(p)
#
#     # Collect results
#     results = []
#     reader.join()
#
#     # send poison pills to stop workers
#     for _ in workers:
#         frame_queue.put(None)
#
#     from queue import Empty
#     # Collect results while waiting
#     results = []
#     alive = True
#     while alive:
#         alive = any(p.is_alive() for p in workers) or not result_queue.empty()
#         try:
#             item = result_queue.get(timeout=0.5)  # non-blocking wait
#             results.append(item)
#         except Empty:
#             pass
#
#     for p in workers:
#         p.join()
#
#     # while not result_queue.empty():
#     #     results.append(result_queue.get())
#
#     return results
#
#
# if __name__ == "__main__":
#     data = process_video("traffic.mp4")
#     print("Sample results:", data[:3])

