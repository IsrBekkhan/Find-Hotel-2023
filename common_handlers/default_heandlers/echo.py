from telebot.types import Message
from loguru import logger

from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
@logger.catch
def bot_echo(message: Message) -> None:
    """
    Эхо обработчик, куда летят текстовые сообщения без указанного состояния

    """
    logger.info('Неуместное сообщение пользователя {}'.format(message.from_user.full_name))
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, f'И вам привет, {message.from_user.full_name}!')
    else:
        bot.reply_to(message, "Неожиданный ответ🧐.\nНе могу понять почему вы так написали🤔."
                              "\nСообщение: "
                              f"{message.text}")
