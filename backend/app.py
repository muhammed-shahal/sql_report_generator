from fastapi import FastAPI
from backend.auth.routes import router as auth_router
from backend.sessions.routes import router as session_router
from backend.query_engine.routes import router as query_router
from backend.etl.routes import router as export_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(session_router)
app.include_router(query_router)
app.include_router(export_router)