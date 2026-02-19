import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db.models import Session as DBSession
from backend.auth.dependencies import get_current_user

router = APIRouter(prefix="/sessions")

@router.post("/create")
def create_session(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session_id = str(uuid.uuid4())

    db_session = DBSession(id=session_id, user_id=user_id)
    db.add(db_session)
    db.commit()

    return {"session_id": session_id}

@router.delete("/logout")
def logout_all_sessions(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    deleted = (
        db.query(DBSession)
        .filter(DBSession.user_id == user_id)
        .delete(synchronize_session=False)
    )

    db.commit()

    return {
        "message": "All sessions logged out successfully",
        "deleted_sessions": deleted
    }