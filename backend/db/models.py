from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from backend.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    password_hash = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())


class Session(Base):
    __tablename__ = "sessions"
    id = Column(String(64), primary_key=True)
    user_id = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())


class QueryHistory(Base):
    __tablename__ = "query_history"
    id = Column(Integer, primary_key=True)
    session_id = Column(String(64))
    user_id = Column(Integer)
    question = Column(Text)
    sql_query = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())


class ExportJob(Base):
    __tablename__ = "export_jobs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    session_id = Column(String(64), nullable=True)
    query_id = Column(Integer, nullable=True)
    query_hash = Column(String(64))
    sql_query = Column(Text)
    status = Column(String(50))
    file_path = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
