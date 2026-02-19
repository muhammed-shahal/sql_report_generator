from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.auth.dependencies import get_current_user
from backend.db.database import get_db
from backend.db.models import QueryHistory
from backend.llm.sql_generator import generate_sql
from backend.mcp_sql_guard.validator import validate_sql
from backend.query_engine.executor import run_preview

router = APIRouter(prefix="/query")

@router.post("/ask")
def ask_question(
    session_id: str,
    question: str,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    # 1. Generate SQL
    sql = generate_sql(question)

    # 2. Validate SQL
    validate_sql(sql)

    # 3. Preview data
    preview = run_preview(sql)

    # 4. Store query history
    q = QueryHistory(
        session_id=session_id,
        user_id=user_id,
        question=question,
        sql_query=sql
    )
    db.add(q)
    db.commit()

    return {
        "generated_sql": sql,
        "preview_rows": preview
    }

@router.get("/history")
def get_history(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    queries = (
        db.query(QueryHistory)
        .filter(QueryHistory.user_id == user_id)
        .order_by(QueryHistory.id.desc())
        .all()
    )
    return queries
