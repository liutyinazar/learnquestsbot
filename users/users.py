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


def add_user_progress(message, question_id, cur, connect):
    chat_id = message.chat.id

    # Перевіряємо, чи існує запис з такими user_id та question_id
    cur.execute(
        "SELECT id FROM user_progress WHERE user_id = %s AND question_id = %s",
        (chat_id, question_id),
    )
    existing_record = cur.fetchone()
    
    if existing_record:
        # Якщо запис існує, оновлюємо його
        cur.execute(
            "UPDATE user_progress SET is_correct = %s, date_answered = now() WHERE id = %s",
            (True, existing_record[0]),
        )
    else:
        # Якщо запис не існує, отримуємо або створюємо user_id з таблиці users
        cur.execute(
            "SELECT id FROM users WHERE chat_id = %s",
            (chat_id,),
        )
        user_id = cur.fetchone()
        
        if not user_id:
            # Якщо user_id не існує, то створюємо новий запис в таблиці users
            cur.execute(
                "INSERT INTO users (chat_id) VALUES (%s) RETURNING id",
                (chat_id,)
            )
            user_id = cur.fetchone()
        
        # Перевіряємо, чи існує запис з такими user_id та question_id ще раз
        cur.execute(
            "SELECT id FROM user_progress WHERE user_id = %s AND question_id = %s",
            (user_id, question_id),
        )
        existing_record = cur.fetchone()
        
        if existing_record:
            # Якщо запис існує (існував під час попередньої перевірки), оновлюємо його
            cur.execute(
                "UPDATE user_progress SET is_correct = %s, date_answered = now() WHERE id = %s",
                (True, existing_record[0]),
            )
        else:
            # Якщо запис все ще не існує, то вставляємо новий
            cur.execute(
                "INSERT INTO user_progress (user_id, question_id, is_correct, date_answered) VALUES (%s, %s, %s, now())",
                (user_id, question_id, True),
            )
    
    connect.commit()



def get_question_id(message, cur):
    chat_id = message.chat.id
    cur.execute(f'SELECT question_id FROM users WHERE chat_id = {chat_id}')
    id = cur.fetchone()
    return id


def change_question_in_db(chat_id, question_id, cur, connect):
    cur.execute(
        "UPDATE users SET question_id = %s WHERE chat_id = %s ",
        (question_id, chat_id),
    )
    connect.commit()


def add_current_answer(cur, connect, chat_id, array):
    cur.execute(
        "UPDATE users SET current_answer = %s WHERE chat_id = %s",
        (array, chat_id),
    )
    connect.commit()


def convert_answer(answer):
    if answer == "a":
        answer = 0
    elif answer == "b":
        answer = 1
    elif answer == "c":
        answer = 2
    elif answer == "d":
        answer = 3

    return answer
