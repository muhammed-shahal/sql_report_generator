import pandas as pd
from sqlalchemy import text
from backend.db.database import engine, SessionLocal
from backend.db.models import ExportJob
from backend.utils.sql_cleaner import clean_sql

EXPORT_DIR = "exports"

def run_export_job(job_id: int, user_id: int, sql: str):
    db = SessionLocal()

    try:
        # mark running
        job = db.query(ExportJob).get(job_id)
        job.status = "running"
        db.commit()

        # clean sql
        sql = clean_sql(sql)

        # heavy query execution
        df = pd.read_sql(text(sql), engine)

        file_path = f"{EXPORT_DIR}/{user_id}_report_{job_id}.csv"
        df.to_csv(file_path, index=False)

        # mark completed
        job.status = "completed"
        job.file_path = file_path
        db.commit()

    except Exception as e:
        job.status = "failed"
        db.commit()
        print("Export failed:", e)

    finally:
        db.close()
