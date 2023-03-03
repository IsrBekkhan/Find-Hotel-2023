from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    """
    Обработчик команды /start, которая отвечает клиенту приветственным сообщением

    """
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!")

