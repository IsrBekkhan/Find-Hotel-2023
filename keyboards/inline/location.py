from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def location_markup() -> InlineKeyboardMarkup:
    """
    Функция, которая создаёт inline-кнопку 'Получить местоположение отеля'

    """
    location = InlineKeyboardMarkup()
    location.add(
        InlineKeyboardButton(
            text='Получить местоположение отеля',
            callback_data='get_location'
        ))
    return location
