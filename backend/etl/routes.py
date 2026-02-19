from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from backend.auth.dependencies import get_current_user
from backend.db.database import get_db
from backend.db.models import ExportJob
from backend.utils.hash import hash_query
from backend.etl.export_worker import run_export_job
from backend.utils.query_fetcher import get_sql_by_query_id
from backend.utils.export_checks import session_has_running_export, user_has_running_history_export, history_query_exported_today

router = APIRouter(prefix="/export")

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

@router.post("/session")
def export_from_session(
    session_id: str,
    query_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    # 1️⃣ block if export running in same session
    running = session_has_running_export(session_id, db)
    if running:
        return {
            "message": "Export already running for this session",
            "job_id": running.id
        }

    # 2️⃣ get SQL
    sql = get_sql_by_query_id(query_id, user_id, db)
    query_hash = hash_query(sql)

    if not sql:
        raise Exception("No query found")

    # 3️⃣ prevent duplicate export inside same session
    existing = (
        db.query(ExportJob)
        .filter(ExportJob.session_id == session_id)
        .filter(ExportJob.query_hash == query_hash)
        .first()
    )

    if existing:
        return {
            "message": "Already exported in this session",
            "job_id": existing.id
        }

    # 4️⃣ create job
    job = ExportJob(
        user_id=user_id,
        session_id=session_id,
        query_id=query_id,
        query_hash=query_hash,
        sql_query=sql,
        status="pending"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    background_tasks.add_task(run_export_job, job.id, user_id, sql)

    return {"job_id": job.id, "message":"sucess"}

@router.post("/history")
def export_from_history(
    query_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    # 1️⃣ block if history export already running
    running = user_has_running_history_export(user_id, db)
    if running:
        return {
            "message": "Another history export running",
            "job_id": running.id
        }

    # 2️⃣ get SQL
    sql = get_sql_by_query_id(query_id, user_id, db)
    query_hash = hash_query(sql)

    if not sql:
        raise Exception("No query found")
    
    query_hash = hash_query(sql)

    # 3️⃣ prevent duplicate export today
    existing_today = history_query_exported_today(user_id, query_hash, db)

    if existing_today:
        return {
            "message": "This report was already exported today",
            "job_id": existing_today.id,
            "status": existing_today.status,
            "file": existing_today.file_path
        }

    # 4️⃣ create job
    job = ExportJob(
        user_id=user_id,
        session_id=None,
        query_id=query_id,
        query_hash=query_hash,
        sql_query=sql,
        status="pending"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    background_tasks.add_task(run_export_job, job.id, user_id, sql)

    return {"job_id": job.id, "message":"sucess"}
