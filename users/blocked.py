def check_is_blocked(message, cur):
    chat_id = message.chat.id
    cur.execute(f"SELECT * FROM blocked_user WHERE blocked_id = {chat_id}")
    user = cur.fetchone()
    if user is not None:
        if user[1] == chat_id:
            return user
    else:
        False
