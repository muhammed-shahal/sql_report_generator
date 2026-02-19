import re

def clean_sql(sql: str) -> str:
    # Remove code block markers if LLM sends them
    sql = sql.replace("```sql", "").replace("```", "")

    # Remove trailing semicolon(s)
    sql = re.sub(r";+\s*$", "", sql.strip())

    return sql