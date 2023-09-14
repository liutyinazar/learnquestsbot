CREATE_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT UNIQUE,
        username TEXT
    )
"""


def change_last_language(message, cur, language_id, connect):
    chat_id = message.chat.id
    cur.execute(
        "UPDATE users SET last_choose_language = %s WHERE chat_id = %s",
        (language_id, chat_id),
    )
    connect.commit()
