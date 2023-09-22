class Question:
    def __init__(
        self, title, a, b, c, d, correct_answer, theme_id, level_id, language_id
    ):
        self.text = title
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.correct_answer = correct_answer
        self.theme_id = theme_id
        self.level_id = level_id
        self.language_id = language_id

    @staticmethod
    def get_all(cur):
        cur.execute(f"SELECT * FROM question")
        all = cur.fetchall()
        return all

    @staticmethod
    def get_all_with_language_theme(cur, language_id, theme_id):
        cur.execute(
            f"SELECT * FROM question WHERE language_id = {language_id} AND theme_id = {theme_id}"
        )
        questions = cur.fetchall()
        return questions
    
    @staticmethod
    def check_user_progress_for_buttons(message, cur, button):
        chat_id = message.chat.id
        cur.execute(f"SELECT id FROM users WHERE chat_id = {chat_id}")
        user_id = cur.fetchone()
        cur.execute(f"SELECT id FROM user_progress WHERE user_id = {user_id}")
        all_question = cur.fetchall()
        print(all_question)