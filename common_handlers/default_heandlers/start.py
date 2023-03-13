from telebot.types import Message
from loguru import logger

from loader import bot


@bot.message_handler(commands=['start'])
@logger.catch
def bot_start(message: Message) -> None:
    """
    Обработчик команды /start, которая отвечает клиенту приветственным сообщением

    """
    logger.info('Приветствие пользователя {}'.format(message.from_user.full_name))
    hello_text = "\tПривет, {user_name}!\n\n"\
                 "<i>Я предоставлю вам справочную информацию об отелях любого интересующего вас города "\
                 "(кроме российского, конечно, тут я думаю итак всё понятно🙃)</i>\n\n"\
                 "Выберите один их вариантов поиска:\n" \
                 "/lowprice - поиск самых дешёвых отелей города\n" \
                 "/highprice - поиск самых дорогих отелей города\n" \
                 "/bestdeal - поиск ближайшего к центру города отеля по предложенной вами цене\n" \
                 "/history - ваша история поиска\n" \
                 "/help - информация для обратной связи".format(user_name=message.from_user.full_name)
    bot.send_message(message.from_user.id, hello_text, parse_mode='html')

