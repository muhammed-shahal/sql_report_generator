import hashlib

def hash_query(sql: str) -> str:
    return hashlib.sha256(sql.encode()).hexdigest()