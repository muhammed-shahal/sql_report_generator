from sqlalchemy.orm import Session
from backend.db.models import ExportJob
from datetime import date

def user_has_running_export(user_id: int, db: Session):
    running = (
        db.query(ExportJob)
        .filter(ExportJob.user_id == user_id)
        .filter(ExportJob.status.in_(["pending", "running"]))
        .first()
    )
    return running

def session_has_running_export(session_id: str, db: Session):
    return (
        db.query(ExportJob)
        .filter(ExportJob.session_id == session_id)
        .filter(ExportJob.status.in_(["pending", "running"]))
        .first()
    )

def user_has_running_history_export(user_id: int, db: Session):
    return (
        db.query(ExportJob)
        .filter(ExportJob.user_id == user_id)
        .filter(ExportJob.session_id.is_(None))
        .filter(ExportJob.status.in_(["pending", "running"]))
        .first()
    )

def history_query_exported_today(user_id: int, query_hash: str, db: Session):
    today = date.today()

    job = (
        db.query(ExportJob)
        .filter(ExportJob.user_id == user_id)
        .filter(ExportJob.session_id.is_(None))  # history mode only
        .filter(ExportJob.query_hash == query_hash)
        .filter(ExportJob.created_at >= today)
        .first()
    )

    return job