from sqlalchemy import text
from backend.db.database import engine

def get_db_schema():
    query = """
    SELECT table_name, column_name
    FROM information_schema.columns
    WHERE table_schema = 'analytics'
    ORDER BY table_name;
    """

    with engine.connect() as conn:
        rows = conn.execute(text(query)).fetchall()

    schema = {}
    for table, column in rows:
        schema.setdefault(table, []).append(column)

    schema_text = ""
    for table, cols in schema.items():
        schema_text += f"{table}({', '.join(cols)})\n"

    return schema_text