from telebot.custom_filters import SimpleCustomFilter
from telebot.types import Message


class HotelsInRange(SimpleCustomFilter):
    """
    Класс HotelsInRange. Родитель: SimpleCustomFilter.
    Фильтр сообщений.

    """
    key = 'hotels_amount'

    def check(self, message: Message) -> bool:
        """
        Функция, проверяющая является ли сообщение числом
        из диапазона от 1 до 10.

        """
        if message.text.isdigit():
            if 1 < int(message.text) <= 10:
                return True
        return False
