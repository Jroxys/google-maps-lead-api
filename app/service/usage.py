from sqlalchemy.orm import Session
from app.db_models import UsageLog


def log_usage(
    db: Session,
    api_key: str,
    job_id: str,
    keyword: str,
    location: str,
    lead_count: int,
    duration_seconds: int
):
    log = UsageLog(
        api_key=api_key,
        job_id=job_id,
        keyword=keyword,
        location=location,
        lead_count=lead_count,
        duration_seconds=duration_seconds
    )
    db.add(log)
    db.commit()
