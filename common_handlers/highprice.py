from telebot.types import Message, CallbackQuery
from time import sleep

from loader import bot
from keyboards.inline.start import start_markup
from states.common_states import CommonStates
from states.highprice_states import HighPriceStates


@bot.message_handler(commands=['highprice'])
def bot_start(message: Message) -> None:
    """
    Обработчик команды /highprice, которая начинает процесс поиска топ
    дорогих отелей и отправляет клиенту inline-кнопку начала диалога.

    """
    start_message_id = bot.send_message(
        message.from_user.id,
        'Эта функция поможет вам найти топ самых дорогих отелей интересующего вас города',
        reply_markup=start_markup()
    ).message_id
    bot.set_state(message.from_user.id, CommonStates.start)
    with bot.retrieve_data(message.from_user.id) as message_data:
        message_data['start_message_id'] = start_message_id
        message_data['chat_id'] = message.chat.id
        message_data['command'] = 'highprice'


@bot.callback_query_handler(func=lambda call: True, state=HighPriceStates.region)
def hotels_amount_asker(call: CallbackQuery):
    """
    Обработчик, который сохраняет выбранный пользователем район, и запрашивает
    у клиента количество отелей для рассмотрения.

    """
    with bot.retrieve_data(call.from_user.id) as search_data:
        hotels_from_region = search_data['regions'][call.data]
        reversed_hotels_list = sorted(hotels_from_region, key=lambda item: item['price'], reverse=True)
        search_data['selected_region'] = reversed_hotels_list
        region_name_message_id = search_data['region_name_message_id']
        chat_id = search_data['chat_id']
    bot.edit_message_text(
        f'Ищем в районе {call.data}',
        chat_id,
        region_name_message_id
    )
    sleep(1)
    bot.send_message(call.from_user.id, 'Сколько отелей хотели бы рассмотреть?\n(Введите количество)')
    bot.set_state(call.from_user.id, CommonStates.hotels_amount)
