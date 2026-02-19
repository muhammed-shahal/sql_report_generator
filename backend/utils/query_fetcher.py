from sqlalchemy.orm import Session
from backend.db.models import QueryHistory

def get_sql_by_query_id(query_id: int, user_id: int, db: Session):
    query = (
        db.query(QueryHistory)
        .filter(QueryHistory.id == query_id)
        .filter(QueryHistory.user_id == user_id)
        .first()
    )

    if not query:
        raise Exception("Query not found")

    return query.sql_query
