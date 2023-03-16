from telebot.custom_filters import SimpleCustomFilter
from telebot.types import Message


class IsPriceMin(SimpleCustomFilter):
    """
    Класс IsPriceMin. Родитель: SimpleCustomFilter.
    Фильтр сообщений.

    """
    key = 'is_min'

    def check(self, message: Message) -> bool:
        """
        Функция, проверяющая является ли сообщение числом
        из диапазона от 1 до 300.

        """
        if message.text.isdigit():
            if 1 < int(message.text) <= 300:
                return True
        return False
