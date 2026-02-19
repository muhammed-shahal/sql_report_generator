from sqlalchemy.orm import Session
from backend.db.models import ExportJob

def user_has_running_export(user_id: int, db: Session):
    running = (
        db.query(ExportJob)
        .filter(ExportJob.user_id == user_id)
        .filter(ExportJob.status.in_(["pending", "running"]))
        .first()
    )
    return running
