import requests

BASE_URL = "http://localhost:8000"

def register(email, password):
    return requests.post(f"{BASE_URL}/auth/register",
                         params={"email": email, "password": password})

def login(email, password):
    return requests.post(f"{BASE_URL}/auth/login",
                         params={"email": email, "password": password})

def create_session(token):
    return requests.post(
        f"{BASE_URL}/sessions/create",
        headers={"Authorization": f"Bearer {token}"}
    )

def ask_question(token, session_id, question):
    return requests.post(
        f"{BASE_URL}/query/ask",
        headers={"Authorization": f"Bearer {token}"},
        params={"session_id": session_id, "question": question}
    )

def get_history(token):
    return requests.get(
        f"{BASE_URL}/query/history",
        headers={"Authorization": f"Bearer {token}"}
    )

def preview_history(token, query_id):
    return requests.post(
        f"{BASE_URL}/query/preview-history",
        headers={"Authorization": f"Bearer {token}"},
        params={"query_id": query_id}
    )

def export_session(token, session_id, query_id):
    return requests.post(
        f"{BASE_URL}/export/session",
        headers={"Authorization": f"Bearer {token}"},
        params={"session_id": session_id, "query_id": query_id}
    )

def export_history(token, query_id):
    return requests.post(
        f"{BASE_URL}/export/history",
        headers={"Authorization": f"Bearer {token}"},
        params={"query_id": query_id}
    )

def get_export_status(token, job_id):
    return requests.get(
        f"{BASE_URL}/export/status/{job_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
