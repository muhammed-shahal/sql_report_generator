from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from backend.auth.dependencies import get_current_user
from backend.db.database import get_db
from backend.db.models import ExportJob
from backend.utils.hash import hash_query
from backend.etl.export_worker import run_export_job
from backend.utils.query_fetcher import get_sql_by_query_id
from backend.utils.export_checks import user_has_running_export

router = APIRouter(prefix="/export")

@router.post("/start")
def start_export(
    query_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    # 1️⃣ allow only one running export per user
    running = user_has_running_export(user_id, db)
    if running:
        return {
            "message": "Another export already running",
            "running_job_id": running.id,
            "status": running.status
        }

    # 2️⃣ get SQL from query history
    sql = get_sql_by_query_id(query_id, user_id, db)
    query_hash = hash_query(sql)

    # 3️⃣ prevent duplicate export
    existing = (
        db.query(ExportJob)
        .filter(ExportJob.user_id == user_id)
        .filter(ExportJob.query_hash == query_hash)
        .first()
    )

    if existing:
        return {
            "message": "Report already generated",
            "job_id": existing.id,
            "status": existing.status,
            "file": existing.file_path
        }

    # 4️⃣ create export job
    job = ExportJob(
        user_id=user_id,
        query_hash=query_hash,
        sql_query=sql,
        status="pending"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # 5️⃣ run ETL async
    background_tasks.add_task(run_export_job, job.id, sql)

    return {
        "job_id": job.id,
        "status": "pending"
    }

@router.get("/status/{job_id}")
def get_status(
    job_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    job = (
        db.query(ExportJob)
        .filter(ExportJob.id == job_id)
        .filter(ExportJob.user_id == user_id)
        .first()
    )

    return {
        "status": job.status,
        "file": job.file_path
    }
