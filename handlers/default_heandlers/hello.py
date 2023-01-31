from telebot.types import Message
from loader import bot


@bot.message_handler(commands=['hello'])
def bot_start(message: Message):
    bot.reply_to(message, f"Приветствую вас, {message.from_user.full_name}, в тестовой команде!")


