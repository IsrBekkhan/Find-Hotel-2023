from telebot.types import InputMediaPhoto
from loguru import logger
from loader import bot
from custom_handlers.get_images_url_handler import get_images_url_handler
from utils.misc.hotels_short_description import hotels_short_description_maker
from keyboards.inline.hotels import hotels_markup
from typing import List


@logger.catch
def hotels_list_with_images_sender(hotels: List,
                                   user_id: int,
                                   images_amount: int,
                                   chat_id: int,
                                   user_name: str,
                                   days_amount: int,
                                   hotels_amount: int) -> None:
    """
    Функция, для отправки клиенту списка отелей с фотографиями

    """
    logger.info('Отправка пользователю {} списка отелей с фотографиями'.format(user_name))

    for count, hotel in enumerate(hotels):
        wait_message_id = bot.send_message(user_id, 'Подождите...').message_id
        images_url_list = get_images_url_handler(hotel_id=hotel['id'], images_amount=images_amount)
        bot.delete_message(chat_id, wait_message_id)

        if isinstance(images_url_list, list):
            bot.send_media_group(
                chat_id,
                [InputMediaPhoto(media=url, caption=description) for url, description in images_url_list])

            description = hotels_short_description_maker(hotels_info=hotel, count=count + 1, days=days_amount)
            bot.send_message(user_id,
                             description,
                             reply_markup=hotels_markup(hotel_info=hotel),
                             parse_mode='html',)

            if hotels_amount == count + 1:
                break
        else:
            logger.info('Отправка пользователю {user_name} сообщения об ошибке'.format(
                user_name=user_name))
            bot.send_message(user_id, images_url_list)
