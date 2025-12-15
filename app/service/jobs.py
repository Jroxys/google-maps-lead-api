from sqlalchemy.orm import Session
from datetime import datetime
from app.db_models import Job, Lead


def create_job(db: Session, job_id: str, api_key: str):
    job = Job(
        job_id=job_id,
        api_key=api_key,
        status="processing"
    )
    db.add(job)
    db.commit()


def complete_job(db: Session, job_id: str, leads: list):
    job = db.query(Job).filter(Job.job_id == job_id).first()

    if not leads or len(leads) == 0:
        job.status = "failed"
        job.error = "No leads found"
        job.finished_at = datetime.utcnow()
        db.commit()
        return False

    job.status = "completed"
    job.finished_at = datetime.utcnow()

    for lead in leads:
        ...
    db.commit()
    return True


def fail_job(db: Session, job_id: str, error: str):
    job = db.query(Job).filter(Job.job_id == job_id).first()
    job.status = "failed"
    job.error = error
    job.finished_at = datetime.utcnow()
    db.commit()
