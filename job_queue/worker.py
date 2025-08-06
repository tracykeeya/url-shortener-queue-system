import time
from job_queue.database import SessionLocal
from job_queue.models import Job, JobStatus

def process_job(job):
    print(f"Processing job: {job.task_name}")
    time.sleep(2)  # simulate work
    print(f"Done: {job.task_name}")

def fetch_and_process():
    db = SessionLocal()
    while True:
        job = (
            db.query(Job)
            .filter(Job.status == JobStatus.pending)
            .order_by(Job.priority.desc())  # higher priority first
            .with_for_update(skip_locked=True)
            .first()
        )

        if not job:
            print("No pending jobs. Waiting...")
            time.sleep(3)
            continue

        job.status = JobStatus.processing
        db.commit()

        try:
            process_job(job)
            job.status = JobStatus.completed
            db.commit()
        except Exception as e:
            print(f"Error: {e}")
            job.status = JobStatus.pending
            db.commit()
        finally:
            db.close()

if __name__ == "__main__":
    fetch_and_process()
