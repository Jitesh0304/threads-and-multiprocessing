from fastapi import FastAPI, UploadFile, BackgroundTasks
from multiprocessing import Pool, Manager
import time, uuid, os

app = FastAPI()

# Shared dictionary to track job status
manager = Manager()
job_status = manager.dict()

# Pool of workers (e.g., 4 parallel jobs)
pool = Pool(processes=4)

# -------------------------
# Worker function (video split)
# -------------------------


def split_video(video_path, job_id):
    try:
        job_status[job_id] = "processing"
        time.sleep(5)  # simulate splitting with ffmpeg
        # Example: ffmpeg splitting (replace with real code)
        # os.system(f"ffmpeg -i {video_path} -c copy -map 0 -segment_time 60 -f segment output_%03d.mp4")
        job_status[job_id] = "completed"
        return f"Job {job_id} completed"
    except Exception as e:
        job_status[job_id] = f"failed: {e}"
        raise


def on_success(result):
    print(result)


def on_error(e):
    print("Error:", e)


@app.post("/split_video/")
async def split(video: UploadFile):
    # Save uploaded file
    video_path = f"temp_{video.filename}"
    with open(video_path, "wb") as f:
        f.write(await video.read())

    # Create unique job_id
    job_id = str(uuid.uuid4())
    job_status[job_id] = "queued"

    # Run in background using Pool
    pool.apply_async(split_video, args=(video_path, job_id),
                     callback=on_success, error_callback=on_error)

    return {"job_id": job_id, "status": "queued"}


@app.get("/status/{job_id}")
def get_status(job_id: str):
    return {"job_id": job_id, "status": job_status.get(job_id, "not_found")}
