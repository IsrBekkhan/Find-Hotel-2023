from telebot.types import Message, CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar
from time import sleep
from loguru import logger

from loader import bot
from keyboards.inline.start import start_markup
from states.common_states import CommonStates
from states.bestdeal_states import BestDealStates
from custom_handlers.get_regions_from_city_handler import get_regions_from_city_handler

from keyboards.inline.regions import region_markup


@bot.message_handler(commands=['bestdeal'])
@logger.catch
def best_deal_start(message: Message) -> None:
    """
    Обработчик команды /bestdeal, которая начинает процесс поиска отелей с подходящей ценой
    и отправляет клиенту inline-кнопку начала диалога.

    """
    logger.info('Запуск диалога bestdeal пользователем {}'.format(message.from_user.full_name))
    start_message_id = bot.send_message(
        message.from_user.id,
        'Эта функция поможет найти самых ближайших к центру отелей интересующего вас города по предложенной вами цене',
        reply_markup=start_markup()
    ).message_id
    bot.set_state(message.from_user.id, CommonStates.start)
    with bot.retrieve_data(message.from_user.id) as message_data:
        message_data['start_message_id'] = start_message_id
        message_data['chat_id'] = message.chat.id
        message_data['command'] = message.text


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(), state=BestDealStates.min_price)
@logger.catch
def min_price_asker(call: CallbackQuery):
    """
    Обработчик, запращивающий у клиента минимальную цену номера отеля

    """
    logger.info('Запрос минимальной цены номера отеля у пользователя, {}'.format(call.from_user.full_name))
    bot.send_message(call.from_user.id, 'Введите минимальную цену номера отеля (в долларах $)')
    bot.set_state(call.from_user.id, BestDealStates.max_price)


@bot.message_handler(state=BestDealStates.max_price, is_min=True)
@logger.catch
def max_price_asker(message: Message):
    """
    Обработчик, запращивающий у клиента максимальную цену номера отеля

    """
    with bot.retrieve_data(message.from_user.id) as search_data:
        search_data['min_price'] = int(message.text)

    logger.info('Запрос максимальной цены номера отеля у пользователя, {}'.format(message.from_user.full_name))
    bot.send_message(message.from_user.id, 'Введите максимальную цену (в долларах $)')
    bot.set_state(message.from_user.id, BestDealStates.region)


@bot.message_handler(state=BestDealStates.max_price, is_min=False)
@logger.catch
def incorrect_min_price_handler(message: Message) -> None:
    """
    Обработчик, который отправляет сообщение ошибки, если клиентом не было
    введено числовое значение в диапазоне от 1 до 300 на запрос минимальной
    цены номера отеля.

    """
    logger.info('Сообщение ошибки пользователю {user_name}. Введенное сообщение: {message_text}'.format(
        user_name=message.from_user.full_name,
        message_text=message.text))
    bot.send_message(message.from_user.id,
                     'Что-то не то. Пожалуйста, введите числовое значение в диапазоне от 1 до 300')


@bot.message_handler(state=BestDealStates.region, is_max=True)
@logger.catch
def best_deal_region_asker(message: Message):
    """
    Обработчик, который получает список районов из API-запроса, и отправляет
    клиенту inline-кнопки для выбора района поиска.

    """
    with bot.retrieve_data(message.from_user.id) as search_data:
        city_id = search_data['city_info']['id']
        city_name = search_data['city_info']['city']
        check_in_date = search_data['check_in']
        check_out_date = search_data['check_out']
        chat_id = search_data['chat_id']
        days_amount = check_out_date - check_in_date
        search_data['days_amount'] = days_amount.days
        min_price = search_data['min_price']

    wait_again_message_id = bot.send_message(message.from_user.id, 'Подождите несколько секунд...').message_id
    regions_from_city = get_regions_from_city_handler(
        city_id=city_id,
        city_name=city_name,
        check_in=check_in_date,
        check_out=check_out_date,
        min_price=min_price,
        max_price=int(message.text),
        sort_by='DISTANCE')
    bot.delete_message(chat_id, wait_again_message_id)

    if isinstance(regions_from_city, dict):
        logger.info('Запрос района поиска у пользователя {}'.format(message.from_user.full_name))
        region_name_message_id = bot.send_message(
            message.from_user.id,
            'Уточните, пожалуйста, в каком районе ищем:',
            reply_markup=region_markup(regions_dict=regions_from_city)
        ).message_id
        with bot.retrieve_data(message.from_user.id) as search_data:
            search_data['regions'] = regions_from_city
            search_data['region_name_message_id'] = region_name_message_id

        bot.set_state(message.from_user.id, BestDealStates.hotels_amount)

    else:
        logger.info('Отправка пользователю {user_name} сообщения об ошибке'.format(
            user_name=message.from_user.full_name))
        bot.send_message(message.from_user.id, regions_from_city)


@bot.message_handler(state=BestDealStates.region, is_max=False)
@logger.catch
def incorrect_max_price_handler(message: Message) -> None:
    """
    Обработчик, который отправляет сообщение ошибки, если клиентом не было
    введено числовое значение больше значения минимальной цены и меньше 300 на запрос максимальной
    цены номера отеля.

    """
    with bot.retrieve_data(message.from_user.id) as search_data:
        min_price = search_data['min_price']

    logger.info('Сообщение ошибки пользователю {user_name}. Введенное сообщение: {message_text}'.format(
        user_name=message.from_user.full_name,
        message_text=message.text))
    bot.send_message(message.from_user.id,
                     'Что-то не то. Пожалуйста, введите числовое значение в диапазоне от {} до 300'.format(min_price))


@bot.callback_query_handler(func=lambda call: True, state=BestDealStates.hotels_amount)
@logger.catch
def best_deal_hotels_amount_asker(call: CallbackQuery):
    """
    Обработчик, который сохраняет выбранный пользователем район, и запрашивает
    у клиента количество отелей для рассмотрения.

    """
    logger.info('Сохранение списка отелей района {} с сортировкой по отдаленности от центра'.format(call.data))
    with bot.retrieve_data(call.from_user.id) as search_data:
        search_data['region_name'] = call.data
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
