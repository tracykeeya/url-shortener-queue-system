from job_queue.database import SessionLocal
from job_queue.models import Job

db = SessionLocal()

jobs = [
    Job(task_name="Send welcome email", priority=2),
    Job(task_name="Resize user image", priority=1),
    Job(task_name="Generate invoice", priority=3),
]

db.add_all(jobs)
db.commit()
db.close()

print("Sample jobs added.")
