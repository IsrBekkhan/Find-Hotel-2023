from typing import Dict


def description_maker(hotels_info: Dict, count: int) -> str:
    """
    Функция, возвращающая строку с краткой информацией об отеле.

    """
    if hotels_info['distance_unit'] == 'KILOMETER':
        unit = 'км'
    else:
        unit = 'миль'

    return '<b>{count}. {hotels_name}</b>\n'\
           '<i>Расстояние от центра города</i>: <b>{distance} {unit}</b>\n'\
           '<i>Цена номера</i>: <b>{price} {symbol}</b>'.format(count=count,
                                                                hotels_name=hotels_info['name'],
                                                                price=int(hotels_info['price']),
                                                                symbol=hotels_info['currency'],
                                                                distance=hotels_info['distance'],
                                                                unit=unit)
