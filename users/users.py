CREATE_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT UNIQUE,
        username TEXT
    )
"""
    