from fastapi import FastAPI, BackgroundTasks
from app.database import SessionLocal
from app.models import LeadRequest, JobStatus
from app.scraper import run_scraper
from app.service.read import get_job_leads, get_job_status
from app.utils import generate_job_id
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi import Request
import concurrent.futures
import csv
import io
from fastapi import Header, HTTPException
from fastapi.responses import StreamingResponse
from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.service.auth import consume_credit, get_credits, refund_credit
from app.service.jobs import create_job, complete_job, fail_job
from app.db_models import Job, Lead
import time
from app.service.usage import log_usage
from app.config import MIN_LEAD_THRESHOLD
from app.service.read import get_usage_logs




app = FastAPI()

jobs = {}

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Too many requests. Please wait before retrying."}
    )

@app.post("/leads", response_model=JobStatus)
@limiter.limit("1/minute")
def create_lead_job(
    req: LeadRequest,
    background_tasks: BackgroundTasks,
    request: Request,
    x_api_key: str = Header(...),
    db: Session = Depends(get_db)
):
    if not consume_credit(db, x_api_key):
        raise HTTPException(status_code=402, detail="Insufficient credits")

    job_id = generate_job_id()

    create_job(db, job_id, x_api_key)  # commit içeriyor

    background_tasks.add_task(process_job, job_id, req)

    return JobStatus(job_id=job_id, status="processing")


def process_job(job_id: str, req: LeadRequest):
    db = SessionLocal()
    job = db.query(Job).filter(Job.job_id == job_id).first()

    try:
        results = run_scraper(f"{req.keyword} {req.location}", req.limit)

        if not results:
            job.status = "completed"
            db.commit()
            return

        for r in results:
            lead = Lead(
                job_id=job_id,
                name=r["name"],
                website=r["website"],
                phone=r["phone"],
                emails=r["emails"],
                ratings=r["ratings"]
            )
            db.add(lead)

        job.status = "completed"
        db.commit()

    except Exception as e:
        job.status = "failed"
        db.commit()
        raise e

    finally:
        db.close()

@app.get("/leads/status/{job_id}")
def job_status(job_id: str, db: Session = Depends(get_db)):
    job = get_job_status(db, job_id)
    if not job:
        return {"error": "Job not found"}

    return {"status": job.status}

@app.get("/leads/result/{job_id}")
def job_result(job_id: str, db: Session = Depends(get_db)):
    leads = db.query(Lead).filter(Lead.job_id == job_id).all()

    if not leads:
        return {"total": 0, "leads": []}

    return {
        "total": len(leads),
        "leads": leads
    }


@app.get("/leads/csv/{job_id}")
def download_csv(job_id: str):
    job = jobs.get(job_id)
    if not job:
        return {"error": "Job not found"}

    if job["status"] != "completed":
        return {"error": "Job not completed yet"}

    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=job["results"][0].keys()
    )
    writer.writeheader()
    writer.writerows(job["results"])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=leads_{job_id}.csv"
        }
    )
@app.get("/credits")
def credits(
    x_api_key: str = Header(...),
    db: Session = Depends(get_db)
):
    return {"remaining_credits": get_credits(db, x_api_key)}

@app.get("/usage")
def usage_logs(
    x_api_key: str = Header(...),
    db: Session = Depends(get_db),
    limit: int = 20
):
    logs = get_usage_logs(db, x_api_key, limit)

    return {
        "total": len(logs),
        "logs": [
            {
                "job_id": log.job_id,
                "keyword": log.keyword,
                "location": log.location,
                "lead_count": log.lead_count,
                "duration_seconds": log.duration_seconds,
                "created_at": log.created_at,
            }
            for log in logs
        ]
    }

