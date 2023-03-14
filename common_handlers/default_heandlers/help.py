from telebot.types import Message
from loguru import logger

from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=['help'])
@logger.catch
def bot_help(message: Message) -> None:
    """
    Обработчик команды /help, которая отправляет клиенту сообщение со списком всех команд

    """
    logger.info('Справка для пользователя {}'.format(message.from_user.full_name))
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    text.insert(0, 'Список всех команд:\n')
    text.append('<i>\nНашли ошибку или есть вопросы?\nEmail для обратной связи</i> - <b>israpal@bk.ru</b>')
    bot.send_message(message.from_user.id, '\n'.join(text), parse_mode='html')
