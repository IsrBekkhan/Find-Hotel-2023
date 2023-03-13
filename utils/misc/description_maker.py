from typing import Dict


def description_maker(hotels_info: Dict, count: int, days: int) -> str:
    """
    Функция, возвращающая строку с краткой информацией об отеле.

    """
    total_price = days * int(hotels_info['price'])

    if hotels_info['distance_unit'] == 'KILOMETER':
        unit = 'км'
    else:
        unit = 'миль'

    return '<b>{count}. {hotels_name}</b>\n'\
           '<i>Расстояние от центра города</i>: <b>{distance} {unit}</b>\n'\
           '<i>Цена номера</i>: <b>{price} {symbol}</b>\n' \
           '<i>Итого за {days} день/дней</i>: <b>{total_price} {symbol}</b>\n' \
           '<i>Ссылка на WEB-страницу отеля: </i>: ' \
           '<b>https://www.hotels.com/h{hotels_id}.Hotel-Information</b>'.format(count=count,
                                                                                 hotels_name=hotels_info['name'],
                                                                                 price=int(hotels_info['price']),
                                                                                 symbol=hotels_info['currency'],
                                                                                 distance=hotels_info['distance'],
                                                                                 unit=unit,
                                                                                 days=days,
                                                                                 total_price=total_price,
                                                                                 hotels_id=hotels_info['id'])
