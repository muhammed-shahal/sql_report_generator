from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.auth.dependencies import get_current_user
from backend.db.database import get_db
from backend.db.models import QueryHistory
from backend.llm.sql_generator import generate_sql
from backend.mcp_sql_guard.validator import validate_sql
from backend.query_engine.executor import run_preview
from backend.utils.hash import hash_query

router = APIRouter(prefix="/query")

@router.post("/ask")
def ask_question(
    session_id: str,
    question: str,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    # 1️⃣ Generate SQL
    sql = generate_sql(question)

    # 2️⃣ Validate SQL
    validate_sql(sql)

    # 3️⃣ Generate hash
    query_hash = hash_query(sql)

    # 4️⃣ Check if query already exists for user
    existing_query = (
        db.query(QueryHistory)
        .filter(QueryHistory.user_id == user_id)
        .filter(QueryHistory.query_hash == query_hash)
        .first()
    )

    if existing_query:
        preview = run_preview(existing_query.sql_query)

        return {
            "query_id": existing_query.id,
            "generated_sql": existing_query.sql_query,
            "preview_rows": preview,
            "message": "Query already saved"
        }

    # 5️⃣ Preview data
    preview = run_preview(sql)

    # 6️⃣ Store query history
    q = QueryHistory(
        session_id=session_id,
        user_id=user_id,
        question=question,
        sql_query=sql,
        query_hash=query_hash
    )

    db.add(q)
    db.commit()
    db.refresh(q)

    return {
        "query_id": q.id,
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

@router.post("/preview-history")
def preview_from_history(
    query_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    query = (
        db.query(QueryHistory)
        .filter(QueryHistory.id == query_id)
        .filter(QueryHistory.user_id == user_id)
        .first()
    )

    if not query:
        raise Exception("Query not found")

    preview = run_preview(query.sql_query)

    return {
        "generated_sql": query.sql_query,
        "preview_rows": preview
    }