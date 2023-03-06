from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def yes_no_markup() -> InlineKeyboardMarkup:
    """
    Функция, которая создаёт inline-кнопки 'Да' и 'Нет'.

    """
    yes_no = InlineKeyboardMarkup()
    yes_no.add(
        InlineKeyboardButton(text='Да', callback_data='1'),
        InlineKeyboardButton(text='Нет', callback_data='0')
    )
    return yes_no
