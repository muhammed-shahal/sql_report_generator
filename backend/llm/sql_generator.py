import requests
from backend.llm.schema_loader import get_db_schema

OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_TEMPLATE = """
You are a senior data analyst.
Convert natural language into MySQL SELECT queries.

Rules:
- ONLY generate SELECT queries
- No INSERT/UPDATE/DELETE
- Use valid MySQL syntax
- Avoid SELECT *
- Prefer joins when needed
- Do not add explanations, return only SQL

Database schema:
{schema}

User question:
{question}
"""

def generate_sql(question: str) -> str:
    schema = get_db_schema()

    prompt = SYSTEM_TEMPLATE.format(schema=schema, question=question)

    response = requests.post(
        OLLAMA_URL,
        json={"model": "llama3", "prompt": prompt, "stream": False},
        timeout=120
    )

    sql = response.json()["response"].strip()
    return sql.replace("```sql", "").replace("```", "").strip()
