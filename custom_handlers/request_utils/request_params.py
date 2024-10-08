from datetime import date
from typing import Tuple, Dict
from loguru import logger


def date_unwrapper(date_object: date) -> Tuple:
    """
    Функция, которая возвращает день, месяц и год из объекта дата.

    """
    date_list = str(date_object).split('-')
    return int(date_list[2]), int(date_list[1]), int(date_list[0])


@logger.catch
def querystring_setter(city: str, language: str = 'ru_RU') -> Dict:
    """
    Функия, возвращающая словарь с параметрами для GET-запроса.

    """
    logger.info('Формирование параметров запроса: {}'.format(city))
    return {
        "q": city,
        "locale": language,
        "langid": "1033",
        "siteid": "300000001"
    }


@logger.catch
def payload_setter(city_id: str,
                   check_in: date,
                   check_out: date,
                   min_price: int,
                   max_price: int,
                   sort_by: str,
                   language: str = 'ru_RU',
                   currency: str = 'USD',
                   ) -> Dict:
    """
    Функия, возвращающая словарь с параметрами для POST-запроса.

    """
    logger.info('Формирование параметров запроса: {}'.format(city_id))
    check_in_day, check_in_month, check_in_year = date_unwrapper(date_object=check_in)
    check_out_day, check_out_month, check_out_year = date_unwrapper(date_object=check_out)
    return {
        "currency": currency,
        "eapid": 1,
        "locale": language,
        "siteId": 300000001,
        "destination": {"regionId": city_id},
        "checkInDate": {
            "day": check_in_day,
            "month": check_in_month,
            "year": check_in_year
        },
        "checkOutDate": {
            "day": check_out_day,
            "month": check_out_month,
            "year": check_out_year
        },
        "rooms": [
            {
                "adults": 2,
                "children": [{"age": 5}, {"age": 7}]
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": sort_by,
        "filters": {"price": {
            "max": max_price,
            "min": min_price
        }}
    }


@logger.catch
def payload_for_detail_setter(hotel_id: str, lang: str = 'ru_RU') -> Dict:
    """
    Функия, возвращающая словарь с параметрами для POST-запроса.

    """
    logger.info('Формирование параметров запроса: {}'.format(hotel_id))
    return {
        "currency": "USD",
        "eapid": 1,
        "locale": lang,
        "siteId": 300000001,
        "propertyId": hotel_id
    }
