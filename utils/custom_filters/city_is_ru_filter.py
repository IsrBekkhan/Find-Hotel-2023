from telebot.custom_filters import SimpleCustomFilter
from telebot.types import Message
from re import search


class CityIsRu(SimpleCustomFilter):
    """
    Класс CityIsRu. Родитель: SimpleCustomFilter.
    Фильтр сообщений.

    """
    key = 'is_ru'

    def check(self, message: Message) -> bool:
        """
        Функция, проверяющая введено ли название города на русском языке.

        """
        check_result = search(r'[а-яА-Я- ]*', message.text)

        if check_result.group(0) == message.text:
            return True
        return False
