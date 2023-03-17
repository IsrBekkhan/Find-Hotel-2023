from telebot.types import Message
from loguru import logger

from loader import bot
from database.database_core import SearchHistory, db


@bot.message_handler(commands=['history'])
@logger.catch
def history_start(message: Message) -> None:
    """
    Обработчик команды /history, которая получает из базы данных историю поиска пользователя и
    отправлюет ему же в виде сообщения.

    """
    logger.info('Запрос в базу данных истории поиска пользователя {}'.format(message.from_user.full_name))

    with db:
        history = SearchHistory.select().where(SearchHistory.user_id == message.from_user.id).order_by(
            SearchHistory.datetime_of_search.desc()).limit(10)

    logger.info('Отправка истории поиска пользователю {}'.format(message.from_user.full_name))
    bot.send_message(message.from_user.id, 'История поиска')

    for count, register in enumerate(history):
        datetime_str = register.datetime_of_search.strftime('%d.%m.%Y %H:%M:%S')

        message_text = '<b>{count}. Дата и время:</b> {date}\n' \
                       '<i>город:</i> {city_name}\n' \
                       '<i>район:</i> {region}\n' \
                       '<i>отель:</i> {hotel_name}'.format(count=count+1,
                                                           date=datetime_str,
                                                           city_name=register.city_name,
                                                           region=register.region,
                                                           hotel_name=register.hotel_name)
        bot.send_message(message.from_user.id, message_text, parse_mode='html')


