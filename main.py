import os
import telebot
from dotenv import load_dotenv
from database.config import conn, cur
from keyboard.keyboard import Keyboard as K
from keyboard.message import Message as M
from learn.learn import check_language, get_theme, get_questions
from users.users import CREATE_TABLE_QUERY, change_last_language
from admin.admin import check_admin, check_users, check_questions

load_dotenv()

TOKEN = os.environ.get("TOKEN")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(func=lambda message: M.MAIN_MENU in message.text)
@bot.message_handler(commands=["help", "start"])
def start_bot(message):
    # Створюємо таблицю, якщо вона не існує
    cur.execute(CREATE_TABLE_QUERY)
    conn.commit()

    chat_id = message.chat.id
    username = message.chat.username

    # Перевіряємо наявність користувача в таблиці
    cur.execute("SELECT * FROM users WHERE chat_id = %s", (chat_id,))
    user_row = cur.fetchone()

    if user_row is None:
        # Додавання нового користувача в таблицю
        cur.execute(
            "INSERT INTO users (chat_id, username) VALUES (%s, %s)", (chat_id, username)
        )
        conn.commit()
        bot.send_message(
            message.chat.id,
            f"Привіт {username}!.\nОбери галузь яку ви плануєте вивчати сьогодні",
            reply_markup=K.menu(),
        )
    else:
        # Перевірка на зміну імені користувача
        if user_row[2] != username:
            cur.execute(
                "UPDATE users SET username = %s WHERE chat_id = %s", (username, chat_id)
            )
            conn.commit()
            bot.send_message(
                message.chat.id,
                f"Вітаю знову, {username}! Твоє ім'я було оновлено.\nОбери галузь яку ви плануєте вивчати сьогодні",
                reply_markup=K.menu(),
            )
        else:
            bot.send_message(
                message.chat.id,
                f"Вітаю знову, {username}!\nОбери галузь яку ви плануєте вивчати сьогодні",
                reply_markup=K.menu(),
            )


@bot.message_handler(func=lambda message: os.environ.get("PASSWORD") in message.text)
def admin_panel(message):
    if check_admin(cur, message.chat.id, message) is None:
        bot.send_message(
            message.chat.id,
            f"{M.NOT_ADMIN}",
            reply_markup=K.menu(),
        )
    else:
        bot.send_message(
            message.chat.id,
            f"Ви ввійшли в адмін панель",
            reply_markup=K.admin_menu(),
        )


@bot.message_handler(
    func=lambda message: any(theme[1] in message.text for theme in get_theme())
)
def theme_select(message):
    # Отримуємо список тем з бази даних
    themes = [theme[1] for theme in get_theme()]
    language_id = check_language(select_language)

    # Перевіряємо, чи містить текст повідомлення якусь з тем
    for theme in themes:
        if theme in message.text:
            bot.send_message(
                message.chat.id,
                f"{M.CHOICE} тему {theme}",
                reply_markup=K.question(language_id),
            )
            break  # Зупиняємо перевірку, коли тему знайдено

    # get_questions(language_id,theme)


@bot.message_handler(func=lambda message: M.PROGRESS in message.text)
def progress(message):
    bot.send_message(message.chat.id, f"Ваш прогрес у навчанні:")


@bot.message_handler(func=lambda message: M.USER in message.text)
def users_list(message):
    if check_admin(cur, message.chat.id, message) is None:
        bot.send_message(
            message.chat.id,
            f"{M.NOT_ADMIN}",
            reply_markup=K.menu(),
        )
    else:
        result = check_users(cur)
        bot.send_message(
            message.chat.id,
            f"Ось усі користувачі боту",
            reply_markup=K.admin_menu(),
        )
        for i in result:
            bot.send_message(
                message.chat.id,
                f"USERNAME: {i[2]}",
            )


@bot.message_handler(func=lambda message: M.QUESTION in message.text)
def show_questions(message):
    if check_admin(cur, message.chat.id, message) is None:
        bot.send_message(
            message.chat.id,
            f"{M.NOT_ADMIN}",
            reply_markup=K.menu(),
        )
    else:
        bot.send_message(message.chat.id, f"Ось всі доступні запитання:\n")
        questions_list = check_questions(cur)
        formated_list = [item[1] for item in questions_list]
        all_questions = "\n".join(formated_list)
        bot.send_message(message.chat.id, f"Ось усі запитання:\n{all_questions}")


@bot.message_handler(func=lambda message: M.NOT_QUESTION in message.text)
def not_question(message):
    bot.send_message(
        message.chat.id,
        "Не проблема, повернемось назад до вибору",
        reply_markup=K.menu(),
    )


@bot.message_handler(func=lambda message: M.ADD_QUESTION in message.text)
def add_question(message):
    if check_admin(cur, message.chat.id, message) is None:
        bot.send_message(
            message.chat.id,
            f"{M.NOT_ADMIN}",
            reply_markup=K.menu(),
        )
    else:
        bot.send_message(
            message.chat.id, "Оберіть мову програмування", reply_markup=K.add_question()
        )


@bot.message_handler(
    func=lambda message: M.JAVA in message.text
    or M.PYTHON in message.text
    or M.JS in message.text
    or M.CPLUS in message.text
)
def learn_start(message):
    language = check_language(message=message.text)
    global select_language
    select_language = message.text
    if language is not None:
        change_last_language(message, cur, language, conn)
        bot.send_message(
            message.chat.id,
            f"{M.CHOICE} {message.text}",
            reply_markup=K.theme(language),
        )
    else:
        bot.send_message(message.chat.id, reply_markup=K.menu())


@bot.message_handler(func=lambda message: True)
def unknown_message(message):
    bot.send_message(message.chat.id, f"Хмм... 🤔\nНе розумію вас 🙁")


bot.infinity_polling()
