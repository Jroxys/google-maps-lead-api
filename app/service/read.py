from sqlalchemy.orm import Session
from app.db_models import Job, Lead , UsageLog



def get_job_status(db: Session, job_id: str):
    return db.query(Job).filter(Job.job_id == job_id).first()


def get_job_leads(db: Session, job_id: str):
    return db.query(Lead).filter(Lead.job_id == job_id).all()

def get_usage_logs(
    db: Session,
    api_key: str,
    limit: int = 50
):
    return (
        db.query(UsageLog)
        .filter(UsageLog.api_key == api_key)
        .order_by(UsageLog.created_at.desc())
        .limit(limit)
        .all()
    )