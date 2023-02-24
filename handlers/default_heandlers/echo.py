from telebot.types import Message

from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message) -> None:
    """
    Эхо обработчик, куда летят текстовые сообщения без указанного состояния

    """
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, f'И вам привет, {message.from_user.full_name}!')
    else:
        bot.reply_to(message, "Эхо без состояния или фильтра.\nСообщение: "
                              f"{message.text}")
