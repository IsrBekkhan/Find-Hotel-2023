from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Dict


def region_markup(regions_dict: Dict) -> InlineKeyboardMarkup:
    """
    Функция, которая создаёт inline-кнопки с названиями районов города

    """
    regions = InlineKeyboardMarkup()
    for region_name, hotels_list in regions_dict.items():
        regions.add(
            InlineKeyboardButton(
                text=region_name,
                callback_data=region_name
            )
        )
    return regions
