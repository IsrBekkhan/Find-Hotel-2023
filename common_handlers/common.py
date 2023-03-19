import datetime

from telebot import custom_filters
from telebot.types import Message, CallbackQuery
from telebot.handler_backends import ContinueHandling
from datetime import date, timedelta, datetime
from time import sleep
from loguru import logger

from loader import bot
from states.common_states import CommonStates
from states.lowprice_states import LowPriceStates
from states.highprice_states import HighPriceStates
from states.bestdeal_states import BestDealStates

from custom_handlers.get_city_info_handler import get_city_info_handler
from custom_handlers.get_regions_from_city_handler import get_regions_from_city_handler
from custom_handlers.get_hotel_info_handler import get_hotel_info_handler
from utils.misc.date_reverser import date_reverser
from utils.misc.hotels_full_description import hotels_full_description_maker
from utils.simple_hotels_list_sender import simple_hotels_list_sender
from utils.hotels_list_with_images_sender import hotels_list_with_images_sender

from telegram_bot_calendar import DetailedTelegramCalendar
from keyboards.calendar_LSTEP_ru import LSTEP
from keyboards.inline.regions import region_markup
from keyboards.inline.yes_no import yes_no_markup
from keyboards.inline.location import location_markup

from utils.custom_filters.city_isalpha_filter import IsAlpha
from utils.custom_filters.hotels_amount_filter import HotelsInRange
from utils.custom_filters.images_amount_filter import ImagesInRange
from utils.custom_filters.city_is_ru_filter import CityIsRu
from utils.custom_filters.is_price_min import IsPriceMin
from utils.custom_filters.is_price_max import IsPriceMax

from database.database_core import SearchHistory, db


@bot.callback_query_handler(func=lambda call: True, state=CommonStates.start)
@logger.catch
def city_name_asker(call: CallbackQuery) -> None:
    """
    Обработчик, запрашивающий у клиента название города.

    """
    logger.info('Запрос ввода города у пользователя {}'.format(call.from_user.full_name))
    with bot.retrieve_data(call.from_user.id) as message_data:
        start_message_id = message_data['start_message_id']
        chat_id = message_data['chat_id']

    bot.edit_message_text('Эта функция поможет вам найти топ самых дешёвых отелей интересующего вас города',
                          chat_id,
                          start_message_id)
    sleep(1)
    bot.send_message(
        call.from_user.id,
        'Введите название города на русском\n<i>Важно: для российских городов поиск не работает</i>',
        parse_mode='html'
    )
    bot.set_state(call.from_user.id, CommonStates.city)


@bot.message_handler(state=CommonStates.city, is_alpha=True, is_ru=True)
@logger.catch
def correct_city_handler(message: Message) -> ContinueHandling:
    """
    Обработчик, куда приходит сообщение с названием города,
    для получения id города из API-запроса.

    """
    logger.info('Обработка сообщения {message_text} от пользователя {user_name}'.format(
        message_text=message.text,
        user_name=message.from_user.full_name))
    wait_message_id = bot.send_message(message.from_user.id, 'Подождите пару секунд...').message_id
    city_info = get_city_info_handler(city_name=message.text)
    bot.delete_message(message.chat.id, wait_message_id)

    if isinstance(city_info, dict):
        with bot.retrieve_data(message.from_user.id) as search_data:
            search_data['city_info'] = city_info
        return ContinueHandling()
    else:
        logger.info('Отправка пользователю {user_name} сообщения об ошибке'.format(
            user_name=message.from_user.full_name))
        bot.send_message(message.from_user.id, city_info)


@bot.message_handler(state=CommonStates.city, is_alpha=False)
@logger.catch
def incorrect_city_handler(message: Message) -> None:
    """
    Обработчик, отправляющий клиенту сообщение ошибки,
    если в названии города есть цифры.

    """
    logger.info('Сообщение ошибки пользователю {user_name}. Введенное сообщение: {message_text}'.format(
        user_name=message.from_user.full_name,
        message_text=message.text))
    bot.send_message(
        message.from_user.id,
        'В названии города не должно быть цифр.\nВведите корректное название города'
    )


@bot.message_handler(state=CommonStates.city, is_ru=False)
@logger.catch
def incorrect_language_handler(message: Message) -> None:
    """
    Обработчик, отправляющий клиенту сообщение ошибки,
    если в названии города введено не на русском языке.

    """
    logger.info('Сообщение ошибки пользователю {user_name}. Введенное сообщение: {message_text}'.format(
        user_name=message.from_user.full_name,
        message_text=message.text))
    bot.send_message(
        message.from_user.id,
        'Пожалуйста, введите название города на русском языке'
    )


@bot.message_handler(state=CommonStates.city, is_alpha=True)
@logger.catch
def check_in_date_asker(message: Message) -> None:
    """
    Обработчик, который отправляет клиенту календарь, для выбора даты заезда в отель.

    """
    logger.info('Запрос даты заезда у пользователя {}'.format(message.from_user.full_name))
    calendar, step = DetailedTelegramCalendar(locale='ru', min_date=date.today()).build()
    bot.send_message(
        message.from_user.id,
        f"Выберите дату заезда в отель:\nВыберите {LSTEP[step]}",
        reply_markup=calendar
    )
    bot.set_state(message.from_user.id, CommonStates.check_in_date)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(), state=CommonStates.check_in_date)
@logger.catch
def check_in_date_handler(call: CallbackQuery) -> ContinueHandling:
    """
    Обработчик, который обрабатывает и сохраняет дату заезда в отель.

    """
    result, key, step = DetailedTelegramCalendar(locale='ru', min_date=date.today()).process(call.data)
    if not result and key:
        bot.edit_message_text(f"Выберите дату заезда в отель:\nВыберите {LSTEP[step]}",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        logger.info('Обработка даты заезда от пользователя {}'.format(call.from_user.full_name))
        bot.edit_message_text('Дата заезда {date}'.format(date=date_reverser(date_object=result)),
                              call.message.chat.id,
                              call.message.message_id)
        with bot.retrieve_data(call.from_user.id) as search_data:
            search_data['check_in'] = result

        return ContinueHandling()


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(), state=CommonStates.check_in_date)
@logger.catch
def check_out_date_asker(call: CallbackQuery) -> None:
    """
    Обработчик, который отправляет клиенту новый календарь, для выбора даты выезда из отеля.

    """
    logger.info('Запрос даты выезда у пользователя {}'.format(call.from_user.full_name))
    with bot.retrieve_data(call.from_user.id) as search_data:
        check_in_date = search_data['check_in']
    sleep(1)
    calendar, step = DetailedTelegramCalendar(locale='ru', min_date=check_in_date).build()
    bot.send_message(
        call.from_user.id,
        f"Выберите дату выезда из отеля:\nВыберите {LSTEP[step]}",
        reply_markup=calendar
    )
    bot.set_state(call.from_user.id, CommonStates.check_out_date)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(), state=CommonStates.check_out_date)
@logger.catch
def check_out_date_handler(call: CallbackQuery) -> ContinueHandling:
    """
    Обработчик, который обрабатывает и сохраняет дату выезда из отеля.

    """
    with bot.retrieve_data(call.from_user.id) as search_data:
        min_date = search_data['check_in'] + timedelta(days=1)

    result, key, step = DetailedTelegramCalendar(locale='ru', min_date=min_date).process(call.data)
    if not result and key:
        bot.edit_message_text(f"Выберите дату выезда из отеля:\nВыберите {LSTEP[step]}",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        logger.info('Обработка даты выезда от пользователя {}'.format(call.from_user.full_name))
        bot.edit_message_text('Дата выезда {date}'.format(date=date_reverser(date_object=result)),
                              call.message.chat.id,
                              call.message.message_id)
        with bot.retrieve_data(call.from_user.id) as search_data:
            search_data['check_out'] = result
            command = search_data['command']

        if command == '/bestdeal':
            bot.set_state(call.from_user.id, BestDealStates.min_price)

        return ContinueHandling()


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(), state=CommonStates.check_out_date)
@logger.catch
def region_asker(call: CallbackQuery):
    """
    Обработчик, который получает список районов из API-запроса, и отправляет
    клиенту inline-кнопки для выбора района поиска.

    """

    with bot.retrieve_data(call.from_user.id) as search_data:
        city_id = search_data['city_info']['id']
        city_name = search_data['city_info']['city']
        check_in_date = search_data['check_in']
        check_out_date = search_data['check_out']
        chat_id = search_data['chat_id']
        days_amount = check_out_date - check_in_date
        search_data['days_amount'] = days_amount.days

    wait_again_message_id = bot.send_message(call.from_user.id, 'Подождите несколько секунд...').message_id
    regions_from_city = get_regions_from_city_handler(
        city_id=city_id,
        city_name=city_name,
        check_in=check_in_date,
        check_out=check_out_date
    )
    bot.delete_message(chat_id, wait_again_message_id)

    if isinstance(regions_from_city, dict):
        logger.info('Запрос района поиска у пользователя {}'.format(call.from_user.full_name))
        region_name_message_id = bot.send_message(
            call.from_user.id,
            'Уточните, пожалуйста, в каком районе ищем:',
            reply_markup=region_markup(regions_dict=regions_from_city)
        ).message_id
        with bot.retrieve_data(call.from_user.id) as search_data:
            search_data['regions'] = regions_from_city
            search_data['region_name_message_id'] = region_name_message_id
            command = search_data['command']

        if command == '/lowprice':
            bot.set_state(call.from_user.id, LowPriceStates.region)
        elif command == '/highprice':
            bot.set_state(call.from_user.id, HighPriceStates.region)

    else:
        logger.info('Отправка пользователю {user_name} сообщения об ошибке'.format(
            user_name=call.from_user.full_name))
        bot.send_message(call.from_user.id, regions_from_city)


@bot.message_handler(state=CommonStates.hotels_amount, hotels_amount=True)
@logger.catch
def is_image_asker(message: Message) -> None:
    """
    Обработчик, куда приходит сообщение с количеством отелей для рассмотрения,
    и который отправляет клиенту inline-кнопки с вопросом о необходимости загрузки
    фотографий для каждого отеля.

    """
    logger.info('Предоставление возможности выбора фотографий пользователю {}'.format(message.from_user.full_name))
    is_image_message_id = bot.send_message(
        message.from_user.id,
        'Хотите рассмотреть фотографии для каждого отеля из списка?',
        reply_markup=yes_no_markup()
    ).message_id
    with bot.retrieve_data(message.from_user.id) as search_data:
        search_data['hotels_amount'] = int(message.text)
        search_data['is_image_message_id'] = is_image_message_id

    bot.set_state(message.from_user.id, CommonStates.is_image)


@bot.message_handler(state=CommonStates.hotels_amount, hotels_amount=False)
@logger.catch
def incorrect_hotels_amount_handler(message: Message) -> None:
    """
    Обработчик, который отправляет сообщение ошибки, если клиентом не было
    введено числовое значение в диапазоне от 1 до 10 на запрос количества
    отелей.

    """
    logger.info('Сообщение ошибки пользователю {user_name}. Введенное сообщение: {message_text}'.format(
        user_name=message.from_user.full_name,
        message_text=message.text))
    bot.send_message(message.from_user.id, 'Что-то не то. Пожалуйста, введите числовое значение от 1 до 10')


@bot.callback_query_handler(func=lambda call: call.data == '1', state=CommonStates.is_image)
@logger.catch
def image_amount_asker(call: CallbackQuery) -> None:
    """
    Обработчик, который запрашивает у клиента количество фотографий для
    вывода, если клиент ответил 'да' на вопрос о необходимости
    фотографий.

    """
    with bot.retrieve_data(call.from_user.id) as message_data:
        is_image_message_id = message_data['is_image_message_id']
        chat_id = message_data['chat_id']

    bot.delete_message(chat_id, is_image_message_id)
    sleep(1)
    logger.info('Запрос количества фотографий у пользователя {}'.format(call.from_user.full_name))
    bot.send_message(call.from_user.id,
                     'Сколько фотографий хотели бы рассмотреть?\n(введите количество)')
    bot.set_state(call.from_user.id, CommonStates.images_amount)


@bot.callback_query_handler(func=lambda call: call.data == '0', state=CommonStates.is_image)
@logger.catch
def hotels_list_sender(call: CallbackQuery) -> None:
    """
    Обработчик, который отправляет клиенту список отелей без фотографий с inline-кнопками,
    если клиент ответил 'нет' на вопрос о необходимости
    фотографий.

    """
    logger.info('Подготовка списка отелей без фотографий для отправки пользователю {}'.format(
        call.from_user.full_name))
    with bot.retrieve_data(call.from_user.id) as search_data:
        hotels_list = search_data['selected_region']
        hotels_amount = search_data['hotels_amount']
        is_image_message_id = search_data['is_image_message_id']
        chat_id = search_data['chat_id']
        days_amount = search_data['days_amount']

    bot.edit_message_text(
        'Список отелей с краткой информацией без фотографий\n(выберите подходящий вам):',
        chat_id,
        is_image_message_id
    )
    simple_hotels_list_sender(hotels=hotels_list,
                              days_amount=days_amount,
                              user_id=call.from_user.id,
                              user_name=call.from_user.full_name,
                              hotels_amount=hotels_amount)
    logger.info('Отправка списка отелей без фотографий пользователю {} завершена'.format(call.from_user.full_name))
    bot.set_state(call.from_user.id, CommonStates.hotel)


@bot.message_handler(state=CommonStates.images_amount, images_amount=True)
@logger.catch
def hotels_list_with_image_sender(message: Message) -> None:
    """
    Обработчик, куда приходит сообщение с количеством фотографий для вывода.
    Далее обработчик получает фотографии из API-запроса и отправляет их
    клиенту со список отелей и inline-кнопками для выбора.

    """
    logger.info('Подготовка списка отелей с фотографиями для пользователя {}'.format(message.from_user.full_name))
    with bot.retrieve_data(message.from_user.id) as search_data:
        hotels_list = search_data['selected_region']
        hotels_amount = search_data['hotels_amount']
        days_amount = search_data['days_amount']

    bot.send_message(message.from_user.id,
                     'Список отелей с краткой информацией и фотографиями\n(выберите подходящий вам):')
    hotels_list_with_images_sender(hotels=hotels_list,
                                   user_id=message.from_user.id,
                                   images_amount=int(message.text),
                                   chat_id=message.chat.id,
                                   user_name=message.from_user.full_name,
                                   days_amount=days_amount,
                                   hotels_amount=hotels_amount)
    logger.info('Отправка списка отелей с фотографиями пользователю {} завершена'.format(message.from_user.full_name))
    bot.set_state(message.from_user.id, CommonStates.hotel)


@bot.message_handler(state=CommonStates.images_amount, images_amount=False)
@logger.catch
def incorrect_images_amount_handler(message: Message) -> None:
    """
    Обработчик, который отправляет сообщение ошибки, если клиентом не было
    введено числовое значение в диапазоне от 1 до 10 на запрос количества
    фотографий.

    """
    logger.info('Сообщение ошибки пользователю {user_name}. Введенное сообщение: {message_text}'.format(
        user_name=message.from_user.full_name,
        message_text=message.text))
    bot.send_message(message.from_user.id, 'Что-то не то. Пожалуйста, введите числовое значение от 1 до 10')


@bot.callback_query_handler(func=lambda call: call.data != 'get_location', state=CommonStates.hotel)
@logger.catch
def hotel_id_handler(call: CallbackQuery) -> None:
    """
    Обработчик, куда приходит id отеля. Далее обработчик получает краткую информацию об отеле
    из API-запроса и отправляет его клиенту с inline-кнопкой для запроса клиентом геоданных этого отеля.

    """
    one_minute_message_id = bot.send_message(call.from_user.id, 'Минуточку... готовлю результат...').message_id
    hotel_info = get_hotel_info_handler(hotel_id=call.data)
    with bot.retrieve_data(call.from_user.id) as search_data:
        chat_id = search_data['chat_id']

    bot.delete_message(chat_id, one_minute_message_id)

    if isinstance(hotel_info, dict):
        with bot.retrieve_data(call.from_user.id) as search_data:
            search_data['hotel_info'] = hotel_info
            city_info = search_data['city_info']
            selected_region = search_data['region_name']

        logger.info('Отправка пользователю {user_name} подробной информации об отеле {hotel_name}'.format(
            user_name=call.from_user.full_name,
            hotel_name=hotel_info['name']))
        map_image_url = hotel_info['map_image']
        hotel_description = hotels_full_description_maker(hotel_info=hotel_info)
        bot.send_photo(chat_id,
                       photo=map_image_url,
                       caption=hotel_description,
                       parse_mode='html',
                       reply_markup=location_markup())
        logger.info('Добавление записи текущего поиска пользователя {} в базу данных'.format(call.from_user.full_name))

        with db:
            SearchHistory.create(user_id=call.from_user.id,
                                 user_name=call.from_user.full_name,
                                 datetime_of_search=datetime.now(),
                                 city_name=city_info['city'],
                                 region=selected_region,
                                 hotel_name=hotel_info['name'],
                                 hotel_id=int(call.data))
    else:
        logger.info('Отправка пользователю {user_name} сообщения об ошибке'.format(
            user_name=call.from_user.full_name))
        bot.send_message(call.from_user.id, hotel_info)


@bot.callback_query_handler(func=lambda call: call.data == 'get_location', state=CommonStates.hotel)
@logger.catch
def location_sender(call: CallbackQuery) -> None:
    """
    Обработчик, который отправляет клиенту геолокацию отеля.

    """
    with bot.retrieve_data(call.from_user.id) as search_data:
        hotel_info = search_data['hotel_info']
        chat_id = search_data['chat_id']

    logger.info('Отправка пользователю {user_name} геолокации отеля {hotel_name}'.format(
        user_name=call.from_user.full_name,
        hotel_name=hotel_info['name']))
    bot.send_location(chat_id,
                      latitude=hotel_info['latitude'],
                      longitude=hotel_info['longitude'])


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(IsAlpha())
bot.add_custom_filter(HotelsInRange())
bot.add_custom_filter(ImagesInRange())
bot.add_custom_filter(CityIsRu())
bot.add_custom_filter(IsPriceMin())
bot.add_custom_filter(IsPriceMax())
