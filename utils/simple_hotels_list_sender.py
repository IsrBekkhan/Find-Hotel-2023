from loguru import logger
from loader import bot
from utils.misc.hotels_short_description import hotels_short_description_maker
from keyboards.inline.hotels import hotels_markup
from typing import List


@logger.catch
def simple_hotels_list_sender(hotels: List,
                              days_amount: int,
                              user_id: int,
                              user_name: str,
                              hotels_amount: int) -> None:
    """
    Функция, для отправки клиенту списка отелей без фотографий

    """
    logger.info('Отправка пользователю {} списка отелей без фотографий'.format(user_name))
    for count, hotel in enumerate(hotels):
        description = hotels_short_description_maker(hotels_info=hotel, count=count + 1, days=days_amount)
        bot.send_message(
            user_id,
            description,
            reply_markup=hotels_markup(hotel_info=hotel),
            parse_mode='html')

        if hotels_amount == count + 1:
            break
