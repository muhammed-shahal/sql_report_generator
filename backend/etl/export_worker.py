import os
import uuid
from datetime import datetime
import pandas as pd
from sqlalchemy import text
from backend.db.database import engine, SessionLocal
from backend.db.models import ExportJob
from backend.utils.sql_cleaner import clean_sql

EXPORT_DIR = "exports"

def run_export_job(job_id: int, user_id: int, sql: str):
    db = SessionLocal()

    try:
        # 1️⃣ mark job as running
        job = db.query(ExportJob).get(job_id)
        job.status = "running"
        db.commit()

        # 2️⃣ clean SQL (remove semicolon / code blocks)
        sql = clean_sql(sql)

        # 3️⃣ execute heavy query
        df = pd.read_sql(text(sql), engine)

        # 4️⃣ ensure exports/user_X folder exists
        user_folder = os.path.join(EXPORT_DIR, f"user_{user_id}")
        os.makedirs(user_folder, exist_ok=True)

        # 5️⃣ generate unique filename
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        short_uuid = uuid.uuid4().hex[:6]
        filename = f"{timestamp}_{job_id}_{short_uuid}.csv"

        file_path = os.path.join(user_folder, filename)

        # 6️⃣ save CSV
        df.to_csv(file_path, index=False)

        # 7️⃣ mark job completed
        job.status = "completed"
        job.file_path = file_path
        db.commit()

    except Exception as e:
        job.status = "failed"
        db.commit()
        print("Export failed:", e)

    finally:
        db.close()
