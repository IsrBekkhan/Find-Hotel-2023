from telebot.custom_filters import SimpleCustomFilter
from loader import bot
from telebot.types import Message


class IsPriceMax(SimpleCustomFilter):
    """
    Класс IsPriceMax. Родитель: SimpleCustomFilter.
    Фильтр сообщений.

    """
    key = 'is_max'

    def check(self, message: Message) -> bool:
        """
        Функция, проверяющая является ли сообщение числом
        больше значения минимальной цены и меньше 300.

        """
        if message.text.isdigit():
            with bot.retrieve_data(message.from_user.id) as search_data:
                min_price = search_data['min_price']

            if min_price < int(message.text) <= 300:
                return True
        return False
