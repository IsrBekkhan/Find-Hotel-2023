from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Dict


def hotels_markup(hotel_info: Dict) -> InlineKeyboardMarkup:
    """
    Функция, которая создаёт inline-кнопку с названием отеля.

    """
    hotel = InlineKeyboardMarkup()
    markup_text = 'Выбрать {}'.format(hotel_info['name'])
    hotel.add(
        InlineKeyboardButton(
            text=markup_text,
            callback_data=hotel_info['id']
        ))
    return hotel
