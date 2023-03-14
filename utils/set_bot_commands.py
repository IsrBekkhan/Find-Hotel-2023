from telebot.types import BotCommand
from loguru import logger
from config_data.config import DEFAULT_COMMANDS
from telebot import TeleBot


@logger.catch
def set_default_commands(bot: TeleBot):
    """
    Функция, добавляющая список команд в меню бота.

    """
    logger.info("Добавление команд")
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )
