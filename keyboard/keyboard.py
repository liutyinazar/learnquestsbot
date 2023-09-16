from telebot.types import ReplyKeyboardMarkup
from keyboard.message import Message as M
from learn.learn import learn_theme, learn_question


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
    def question(cls, language):
        questions = learn_question(language)
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
        answer_buttons = [_[2:6] for _ in answers]  # Вибираємо кнопки з кожного елемента answers
        buttons = [_ for _ in answer_buttons] if answer_buttons else []  # Вибираємо тексти кнопок

        return cls(
            (M.MAIN_MENU,),
            *buttons,
        )