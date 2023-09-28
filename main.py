import os
import telebot
from dotenv import load_dotenv
from database.config import conn, cur
from keyboard.keyboard import Keyboard as K
from keyboard.message import Message as M
from learn.learn import (
    check_language,
    get_theme,
    get_theme_id,
    get_all_questions,
    get_questions_info,
    get_current_answer,
)
from admin.admin import check_admin, check_users
from users.blocked import check_is_blocked
from users.users import (
    CREATE_TABLE_QUERY,
    change_last_language,
    get_user_progress,
    change_last_theme,
    change_question_in_db,
    add_current_answer,
    convert_answer,
    add_user_progress,
    get_question_id,
)
from models.models import Question

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
    defend = check_is_blocked(message, cur)
    if defend is not None:
        bot.send_message(
            message.chat.id,
            f"Привіт {username}!.\nТи не можеш користуватись цим ботом, по причині: {defend[2]}",
        )
    else:
        # Перевіряємо наявність користувача в таблиці
        cur.execute("SELECT * FROM users WHERE chat_id = %s", (chat_id,))
        user_row = cur.fetchone()

        if user_row is None:
            # Додавання нового користувача в таблицю
            cur.execute(
                "INSERT INTO users (chat_id, username) VALUES (%s, %s)",
                (chat_id, username),
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
                    "UPDATE users SET username = %s WHERE chat_id = %s",
                    (username, chat_id),
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
    chat_id = message.chat.id

    # Перевіряємо, чи містить текст повідомлення якусь з тем
    for theme in themes:
        if theme in message.text:
            theme_id = get_theme_id(language_id, theme)
            change_last_theme(message, cur, theme_id, conn)
            bot.send_message(
                message.chat.id,
                f"{M.CHOICE} тему {theme}",
                reply_markup=K.question(language_id, theme_id, chat_id),
            )
            break


@bot.message_handler(
    func=lambda message: any(
        question[1] in message.text[:-2] for question in get_all_questions()
    )
)
def current_question(message):
    chat_id = message.chat.id
    question = get_questions_info(cur, message.text[:-2])
    change_question_in_db(chat_id, question[0][0], cur, conn)
    all_answer = question[0][2:7]
    add_current_answer(cur, conn, chat_id, list(all_answer))
    bot.send_message(
        message.chat.id,
        f"{message.text[:-2]}\n",
        reply_markup=K.corrent_question(question),
    )


@bot.message_handler(
    func=lambda message: any(
        answer in message.text for answer in get_current_answer(cur, message)
    )
    if get_current_answer(cur, message)
    else False
)
def current_answer(message):
    answer = get_current_answer(cur, message)
    correct_answer = convert_answer(*answer[4:5])
    if message.text == answer[correct_answer]:
        bot.send_message(
            message.chat.id, f"Відповідь правильна, вітаю! 🎊", reply_markup=K.menu()
        )
        id = get_question_id(message, cur)
        add_user_progress(message, *id, cur, conn)
    else:
        bot.send_message(message.chat.id, f"Відповідь не правильна, спробуйте щераз 🙁")


@bot.message_handler(func=lambda message: M.PROGRESS in message.text)
def progress(message):
    all_questions = get_all_questions()
    correct_answer = get_user_progress(message, cur)

    interest = (correct_answer / len(all_questions)) * 100
    if correct_answer is None or correct_answer == 0:
        bot.send_message(message.chat.id, f"Ви ще не почали відповідати на питання 🙁")
    else:
        bot.send_message(
            message.chat.id,
            f"Ваш прогрес у навчанні\nКількість правильно пройдених запитань - {correct_answer}, так тримати 🤩\nВи пройшли {round(interest,2)}% від усіх питань 😎\nЗагальна кількість питань {len(all_questions)}",
        )


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
        questions_list = Question.get_all(cur)
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


@bot.message_handler(func=lambda message: True)
def unknown_message(message):
    bot.send_message(message.chat.id, f"Хмм... 🤔\nНе розумію вас 🙁")


bot.infinity_polling()
