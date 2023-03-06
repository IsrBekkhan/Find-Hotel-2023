from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_markup() -> InlineKeyboardMarkup:
    """
    Функция, которая создаёт inline-кнопку 'Продолжить'

    """
    start = InlineKeyboardMarkup()
    start.add(
        InlineKeyboardButton(
            text='Продолжить',
            callback_data='start'
        )
    )
    return start
