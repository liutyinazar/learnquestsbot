from database.config import cur


# GET REQUEST TO GET DATA
def learn(language):
    cur.execute(f"SELECT * FROM theme WHERE language_id = {language}")
    questions = cur.fetchall()  # LIST
    return questions


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
