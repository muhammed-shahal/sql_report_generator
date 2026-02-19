FORBIDDEN = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE"]

def validate_sql(sql: str):
    sql_upper = sql.upper()

    if not sql_upper.startswith("SELECT"):
        raise Exception("Only SELECT queries allowed")

    for keyword in FORBIDDEN:
        if keyword in sql_upper:
            raise Exception("Dangerous SQL detected")

    return True
