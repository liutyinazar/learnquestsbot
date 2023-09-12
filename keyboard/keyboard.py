from telebot.types import ReplyKeyboardMarkup
from keyboard.message import Message as M
from learn.learn import learn


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
            (
                M.PYTHON[:-2],
                M.JAVA[:-2],
                M.JS[:-2],
                M.CPLUS[:-2],
            ),
        )

    @classmethod
    def question(cls, language):
        questions = learn(language)
        if not questions:
            return cls(
                (M.NOT_QUESTION,),
            )
        buttons = [_[1] for _ in questions] if questions else []
        print(buttons)

        return cls(
            (M.MAIN_MENU,),
            (*buttons,),
        )
