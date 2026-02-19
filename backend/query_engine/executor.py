from sqlalchemy import text
from backend.db.database import engine
from backend.utils.sql_cleaner import clean_sql

def run_preview(sql: str, limit: int = 20):
    sql = clean_sql(sql)  #sanitize first

    preview_sql = f"SELECT * FROM ({sql}) AS subquery LIMIT {limit}"

    with engine.connect() as conn:
        result = conn.execute(text(preview_sql))
        rows = [dict(r._mapping) for r in result]

    return rows
