def check_admin(cursor, chat_id, message):
    cursor.execute("SELECT * FROM admin WHERE chat_id = %s", (chat_id,))
    user_row = cursor.fetchone()

    return user_row

def check_users(cursor):
    cursor.execute("SELECT * FROM users" )
    users = cursor.fetchall()
    return users

def check_questions(cursor):
    cursor.execute("SELECT * FROM question")
    question = cursor.fetchall()
    return question