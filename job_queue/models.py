from sqlalchemy import Column, Integer, String, Enum
from .database import Base

from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class JobStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String, nullable=False)
    status = Column(Enum(JobStatus), default=JobStatus.pending)
    priority = Column(Integer, default=1)
