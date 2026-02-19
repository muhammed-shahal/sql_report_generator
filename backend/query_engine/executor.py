from sqlalchemy import text
from backend.db.database import engine

def run_preview(sql: str, limit: int = 20):
    # preview_sql = f"SELECT * FROM ({sql}) AS subquery LIMIT {limit}"
    preview_sql = f"{sql[:-1]} LIMIT {limit}"

    with engine.connect() as conn:
        result = conn.execute(text(preview_sql))
        rows = [dict(r._mapping) for r in result]

    return rows
