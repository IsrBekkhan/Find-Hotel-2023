from telebot.custom_filters import SimpleCustomFilter
from telebot.types import Message


class IsAlpha(SimpleCustomFilter):
    """
    Класс IsAlpha. Родитель: SimpleCustomFilter.
    Фильтр сообщений.

    """
    key = 'is_alpha'

    def check(self, message: Message) -> bool:
        """
        Функция, проверяющая наличие цифр в тексте.

        """
        for letter in message.text:
            if letter.isdigit():
                return False
        return True
