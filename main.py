from loguru import logger

logger.add('debug.log',
           format='{time}  {level} \t {message}',
           level='DEBUG',
           rotation='3:00',
           compression='zip')

logger.info("Запуск бота")

from loader import bot
import common_handlers
from common_handlers import default_heandlers
from utils.set_bot_commands import set_default_commands
from database.database_core import SearchHistory


if __name__ == '__main__':
    set_default_commands(bot)
    SearchHistory.create_table()
    logger.info("Бот 'Find Hotel 2023' запущен!")
    bot.infinity_polling()
