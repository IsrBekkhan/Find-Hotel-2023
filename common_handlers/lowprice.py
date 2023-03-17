from telebot.types import Message, CallbackQuery
from time import sleep
from loguru import logger

from loader import bot
from keyboards.inline.start import start_markup
from states.common_states import CommonStates
from states.lowprice_states import LowPriceStates


@bot.message_handler(commands=['lowprice'])
@logger.catch
def low_price_start(message: Message) -> None:
    """
    Обработчик команды /lowprice, которая начинает процесс поиска топ
    дешёвых отелей и отправляет клиенту inline-кнопку начала диалога.

    """
    logger.info('Запуск диалога lowprice пользователем {}'.format(message.from_user.full_name))
    start_message_id = bot.send_message(
        message.from_user.id,
        'Эта функция поможет вам найти топ самых дешёвых отелей интересующего вас города',
        reply_markup=start_markup()
    ).message_id
    bot.set_state(message.from_user.id, CommonStates.start)
    with bot.retrieve_data(message.from_user.id) as message_data:
        message_data['start_message_id'] = start_message_id
        message_data['chat_id'] = message.chat.id
        message_data['command'] = message.text


@bot.callback_query_handler(func=lambda call: True, state=LowPriceStates.region)
@logger.catch
def hotels_amount_asker(call: CallbackQuery):
    """
    Обработчик, который сохраняет выбранный пользователем район, и запрашивает
    у клиента количество отелей для рассмотрения.

    """
    logger.info('Сохранение списка отелей района {} по возрастанию цены '.format(call.data))
    with bot.retrieve_data(call.from_user.id) as search_data:
        hotels_from_region = search_data['regions'][call.data]
        search_data['selected_region'] = hotels_from_region
        region_name_message_id = search_data['region_name_message_id']
        chat_id = search_data['chat_id']

    bot.edit_message_text(
        f'Ищем в районе {call.data}',
        chat_id,
        region_name_message_id
    )
    sleep(1)
    logger.info('Запрос у пользователя {} количества рассматриваемых отелей в районе {}'.format(
        call.from_user.full_name, call.data))
    bot.send_message(call.from_user.id, 'Сколько отелей хотели бы рассмотреть?\n(Введите количество)')
    bot.set_state(call.from_user.id, CommonStates.hotels_amount)
