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


def change_last_theme(message, cur, theme_id, connect):
    chat_id = message.chat.id
    cur.execute(
        "UPDATE users SET last_choose_theme = %s WHERE chat_id = %s",
        (theme_id, chat_id),
    )
    connect.commit()


def get_user_progress(message, cur):
    chat_id = message.chat.id
    cur.execute(f"SELECT * FROM users WHERE chat_id = {chat_id}")
    id = cur.fetchone()
    cur.execute(f"SELECT * FROM user_progress WHERE user_id = {id[0]}")
    correct_answer = cur.fetchall()

    return len(correct_answer)


def change_question_in_db(chat_id, question_id, cur, connect):
    cur.execute(
        "UPDATE users SET question_id = %s WHERE chat_id = %s ",
        (question_id, chat_id),
    )
    connect.commit()


def add_current_answer(cur, connect, chat_id, array):
    cur.execute(
        "UPDATE users SET current_answer = current_answer || %s WHERE chat_id = %s",
        (array, chat_id),
    )
    connect.commit()

def convert_answer(answer):
    if answer == 'a':
        answer = 0
    elif answer == 'b':
        answer = 1
    elif answer == 'c':
        answer = 2
    elif answer == 'd':
        answer = 3

    return answer