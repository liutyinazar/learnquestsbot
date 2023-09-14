from database.config import cur


# GET REQUEST TO GET DATA
def learn_question(language):
    cur.execute(f"SELECT * FROM question WHERE language_id = {language}")
    questions = cur.fetchall()  # LIST
    return questions

def learn_theme(language):
    cur.execute(f"SELECT * FROM theme WHERE language_id = {language}")
    theme = cur.fetchall()  # LIST
    return theme


# CHECK WICH LANGUAGE USER SELECT
def check_language(message):
    if message == "Python 🐍":
        language = 1
    elif message == "Java ☕":
        language = 2
    elif message == "JavaScript 💻":
        language = 3
    elif message == "C++ 🚀":
        language = 4
    else:
        None

    return language


def get_theme():
    cur.execute(f"SELECT * FROM theme")
    theme = cur.fetchall()

    return theme

def get_questions(id, theme):
    cur.execute(f"SELECT * FROM theme WHERE title = '{theme}'")
    theme = cur.fetchone()
    theme_id = theme[0]
    cur.execute(f"SELECT * FROM question WHERE language_id = {id} AND theme_id = {theme_id}")
    questions= cur.fetchall()
    return questions