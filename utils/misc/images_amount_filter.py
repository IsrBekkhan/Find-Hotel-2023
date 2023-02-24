from telebot.custom_filters import SimpleCustomFilter
from telebot.types import Message


class ImagesInRange(SimpleCustomFilter):
    """
    Класс ImagesInRange. Родитель: SimpleCustomFilter.
    Фильтр сообщений.

    """
    key = 'images_amount'

    def check(self, message: Message) -> bool:
        """
        Функция, проверяющая является ли сообщение числом
        из диапазона от 0 до 15.

        """
        if message.text.isdigit():
            if 0 < int(message.text) <= 15:
                return True
        return False
