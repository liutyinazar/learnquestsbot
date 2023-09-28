from telebot.types import ReplyKeyboardMarkup
from keyboard.message import Message as M
from learn.learn import learn_theme
from users.users import check_progress
from models.models import Question
from database.config import cur



class Keyboard:
    def __new__(self, *buttons) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        _ = [keyboard.add(*i) for i in buttons]

        return keyboard

    @classmethod
    def menu(cls):
        return cls(
            (
                M.PYTHON,
                M.JAVA,
            ),
            (
                M.JS,
                M.CPLUS,
            ),
            (M.PROGRESS,),
        )

    @classmethod
    def admin_menu(cls):
        return cls(
            (M.MAIN_MENU,),
            (M.USER,),
            (
                M.QUESTION,
                M.ADD_QUESTION,
            ),
        )

    @classmethod
    def add_question(cls):
        return cls(
            (M.MAIN_MENU,),
            (
                M.PYTHON[:-2],
                M.JAVA[:-2],
                M.JS[:-2],
                M.CPLUS[:-2],
            ),
        )

    @classmethod
    def question(cls, language, theme_id, chat_id):
        completed_questions = check_progress(chat_id, cur)
        questions = Question.get_all_with_language_theme(cur, language, theme_id)
        if not questions:
            return cls(
                (M.NOT_QUESTION,),
            )
        
        buttons = [(_[1],) for _ in questions] if questions else []

        for i, button in enumerate(buttons):
            if button[0] in completed_questions:
                buttons[i] = (button[0] + " ✅ ",)
            else:
                buttons[i] = (button[0] + " ❓ ",)

        return cls(
            (M.MAIN_MENU,),
            *buttons,
        )

    @classmethod
    def theme(cls, language):
        questions = learn_theme(language)
        if not questions:
            return cls(
                (M.NOT_QUESTION,),
            )
        buttons = [_[1] for _ in questions] if questions else []

        # Розбиваємо кнопки на пари
        button_pairs = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]

        # Переводимо пари кнопок в кортежі
        button_tuples = tuple(tuple(pair) for pair in button_pairs)

        return cls(
            (M.MAIN_MENU,),
            *button_tuples,
        )

    @classmethod
    def corrent_question(cls, answers):
        answer_buttons = [_[2:6] for _ in answers]
        buttons = [_ for _ in answer_buttons] if answer_buttons else []
        # print(type(buttons))

        return cls(
            (M.MAIN_MENU,),
            *buttons,
        )
